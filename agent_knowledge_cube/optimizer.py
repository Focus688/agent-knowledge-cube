"""
Weighted Knowledge Optimizer

扩展 Cube 的第二种思路：用权重动态调参，不再硬查表。

Score = W1 × RoleFit(x) + W2 × WorkflowEff(y) + W3 × KnowledgeRel(z)

W1:W2:W3 由 LLM 根据目标 G 动态输出，让三个维度按场景协商。
"""

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from urllib import request
from .loader import Cube


@dataclass
class WeightedResult:
    """A scored (x, y, z) combination."""
    role: str
    stage: str  # full stage key like "software-development:implementation"
    stage_name: str
    knowledge_paths: List[str]
    score: float
    scores: Dict[str, float] = field(default_factory=dict)  # individual W*x scores


@dataclass
class OptimizationConfig:
    """LLM configuration for weight optimization."""
    api_endpoint: str = "https://api.deepseek.com/v1/chat/completions"
    api_key: Optional[str] = None
    model: str = "deepseek-chat"
    temperature: float = 0.1  # low temp for deterministic weights
    max_tokens: int = 512

    @classmethod
    def from_env(cls) -> "OptimizationConfig":
        """Auto-configure from environment variables."""
        return cls(
            api_endpoint=os.environ.get(
                "OPTIMIZER_API_ENDPOINT",
                os.environ.get("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
            ).rstrip("/") + "/chat/completions",
            api_key=os.environ.get(
                "OPTIMIZER_API_KEY",
                os.environ.get("OPENAI_API_KEY", "")
            ),
            model=os.environ.get(
                "OPTIMIZER_MODEL",
                os.environ.get("LLM_MODEL", "deepseek-chat")
            ),
        )


# ── Default heuristic weights (no LLM needed) ────────────

DEFAULT_WEIGHT_PROFILES: Dict[str, Dict[str, float]] = {
    "incident":         {"W1": 0.20, "W2": 0.65, "W3": 0.15},  # 故障：流程优先
    "compliance":       {"W1": 0.25, "W2": 0.15, "W3": 0.60},  # 合规：知识优先
    "strategy":         {"W1": 0.55, "W2": 0.25, "W3": 0.20},  # 战略：角色经验优先
    "execution":        {"W1": 0.30, "W2": 0.40, "W3": 0.30},  # 执行：均衡
    "customer-facing":  {"W1": 0.35, "W2": 0.45, "W3": 0.20},  # 客户面对面：流程+角色
    "research":         {"W1": 0.40, "W2": 0.15, "W3": 0.45},  # 研究：角色+知识
}

DEFAULT_WEIGHTS = {"W1": 0.33, "W2": 0.33, "W3": 0.34}  # fallback 均衡


class WeightedOptimizer:
    """Weighted optimization layer on top of the Cube.

    Two modes:
      - heuristic:  use predefined weight profiles (no LLM call)
      - llm:        call LLM to generate optimal weights for the goal
    """

    def __init__(
        self,
        cube: Cube,
        config: Optional[OptimizationConfig] = None,
    ):
        self.cube = cube
        self.config = config or OptimizationConfig.from_env()

    # ── Public API ────────────────────────────────────────

    def optimize_weights(
        self,
        goal: str,
        mode: str = "heuristic",
        available_roles: Optional[List[str]] = None,
        available_workflows: Optional[List[str]] = None,
    ) -> Dict[str, float]:
        """Get optimal W1:W2:W3 weights for a goal.

        Args:
            goal: Natural language description of the objective
            mode: "heuristic" (no LLM) or "llm" (calls LLM)
            available_roles: Limit role candidates
            available_workflows: Limit workflow candidates

        Returns:
            {"W1": float, "W2": float, "W3": float}
        """
        if mode == "llm":
            return self._llm_optimize(goal, available_roles, available_workflows)
        else:
            return self._heuristic_weights(goal)

    def optimize(
        self,
        goal: str,
        top_k: int = 3,
        mode: str = "heuristic",
        available_roles: Optional[List[str]] = None,
        available_workflows: Optional[List[str]] = None,
    ) -> List[WeightedResult]:
        """Get top-k (x, y, z) combinations scored for a goal.

        This is the main entry point: given a goal, find the best
        role, workflow stage, and knowledge slice combination.

        Args:
            goal: Natural language description
            top_k: Number of results to return
            mode: "heuristic" or "llm"
            available_roles: Limit to specific roles
            available_workflows: Limit to specific workflows

        Returns:
            List of WeightedResult sorted by score descending
        """
        # Step 1: Get weights
        weights = self.optimize_weights(goal, mode, available_roles, available_workflows)

        # Step 2: Get candidates
        candidates = self._get_candidates(
            role_filter=available_roles,
            workflow_filter=available_workflows,
        )

        # Step 3: Score each candidate
        scored = []
        for role_name, stage_key, stage_name, z_paths in candidates:
            scores = self._score_candidate(
                role_name, stage_key, stage_name, z_paths, goal, weights
            )
            total = sum(scores.values())
            scored.append(WeightedResult(
                role=role_name,
                stage=stage_key,
                stage_name=stage_name,
                knowledge_paths=z_paths,
                score=total,
                scores=scores,
            ))

        # Step 4: Sort and return top_k
        scored.sort(key=lambda r: r.score, reverse=True)
        return scored[:top_k]

    def compare_modes(
        self,
        goal: str,
        top_k: int = 3,
    ) -> Dict[str, List[WeightedResult]]:
        """Compare heuristic vs LLM optimization for the same goal."""
        return {
            "heuristic": self.optimize(goal, top_k, mode="heuristic"),
            "llm": self.optimize(goal, top_k, mode="llm"),
        }

    # ── Heuristic mode ────────────────────────────────────

    def _heuristic_weights(self, goal: str) -> Dict[str, float]:
        """Match goal keywords to predefined weight profiles."""
        goal_lower = goal.lower()

        for keyword, profile in DEFAULT_WEIGHT_PROFILES.items():
            if keyword in goal_lower:
                return profile

        # Fuzzy matching by keywords
        emergency_keywords = ["故障", "中断", "宕机", "紧急", "incident", "outage", "p0", "崩溃", "不可用", "事故"]
        compliance_keywords = ["合规", "审计", "法规", "compliance", "audit", "gdpr", "soc2", "安全", "隐私"]
        strategy_keywords = ["战略", "规划", "路线图", "strategy", "roadmap", "立项", "方向", "定义", "决策", "确定"]
        incident_keywords = ["投诉", "响应慢", "太慢", "优化", "改进", "流程", "效率"]
        customer_keywords = ["客户", "customer", "support", "服务", "售后"]

        for keywords, profile in [
            (emergency_keywords, DEFAULT_WEIGHT_PROFILES["incident"]),
            (compliance_keywords, DEFAULT_WEIGHT_PROFILES["compliance"]),
            (strategy_keywords, DEFAULT_WEIGHT_PROFILES["strategy"]),
            (incident_keywords, DEFAULT_WEIGHT_PROFILES["incident"]),
            (customer_keywords, DEFAULT_WEIGHT_PROFILES["customer-facing"]),
        ]:
            if any(k in goal_lower for k in keywords):
                return profile

        return dict(DEFAULT_WEIGHTS)

    # ── LLM mode ──────────────────────────────────────────

    def _llm_optimize(
        self,
        goal: str,
        available_roles: Optional[List[str]] = None,
        available_workflows: Optional[List[str]] = None,
    ) -> Dict[str, float]:
        """Call LLM to get optimal weights."""
        if not self.config.api_key:
            print("⚠️  No LLM API key configured. Falling back to heuristic mode.")
            return self._heuristic_weights(goal)

        roles_context = ""
        if available_roles:
            roles_context = f"\n可用角色: {', '.join(available_roles)}"

        workflows_context = ""
        if available_workflows:
            workflows_context = f"\n可用工作流: {', '.join(available_workflows)}"

        prompt = f"""你是一个 AI Agent 知识约束系统的权重优化器。

目标: {goal}{roles_context}{workflows_context}

请分析这个目标，输出三个维度的最佳权重（0.0~1.0，和为1.0）：

W1 = 角色匹配权重 — 这个目标多大程度上依赖特定角色的专业经验？
W2 = 工作流效率权重 — 这个目标多大程度上依赖流程的执行顺序？
W3 = 知识库相关性权重 — 这个目标多大程度上依赖特定知识领域？

只需要输出 JSON，不要其他内容：
{{"W1": 0.xx, "W2": 0.xx, "W3": 0.xx, "reasoning": "一句话解释为什么"}}"""

        try:
            response = self._call_llm(prompt)
            data = json.loads(response)
            return {
                "W1": float(data.get("W1", DEFAULT_WEIGHTS["W1"])),
                "W2": float(data.get("W2", DEFAULT_WEIGHTS["W2"])),
                "W3": float(data.get("W3", DEFAULT_WEIGHTS["W3"])),
            }
        except Exception as e:
            print(f"⚠️  LLM optimization failed: {e}. Falling back to heuristic.")
            return self._heuristic_weights(goal)

    def _call_llm(self, prompt: str) -> str:
        """Call OpenAI-compatible API."""
        payload = json.dumps({
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": "You are a weight optimizer. Output only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }).encode()

        req = request.Request(
            self.config.api_endpoint,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]

    # ── Candidate scoring ─────────────────────────────────

    def _get_candidates(
        self,
        role_filter: Optional[List[str]] = None,
        workflow_filter: Optional[List[str]] = None,
    ) -> List[Tuple[str, str, str, List[str]]]:
        """Get all (role, stage_key, stage_name, z_paths) from the cube index."""
        candidates = []
        for entry in self.cube._index:
            role = entry.get("x", "")
            stage_key = entry.get("y", "")
            z_paths = entry.get("z", [])

            if role_filter and role not in role_filter:
                continue
            if workflow_filter and not any(stage_key.startswith(f"{wf}:") for wf in workflow_filter):
                continue

            # Get stage display name
            wf_name = stage_key.split(":")[0] if ":" in stage_key else ""
            stage_id = stage_key.split(":")[1] if ":" in stage_key else stage_key
            wf_info = self.cube.get_workflow_info(wf_name)
            stage_name = stage_id
            if wf_info:
                for s in wf_info.get("stages", []):
                    if s.get("id") == stage_id:
                        stage_name = s.get("name", stage_id)
                        break

            candidates.append((role, stage_key, stage_name, z_paths))

        return candidates

    def _score_candidate(
        self,
        role: str,
        stage_key: str,
        stage_name: str,
        z_paths: List[str],
        goal: str,
        weights: Dict[str, float],
    ) -> Dict[str, float]:
        """Score a single (x, y, z) candidate against the goal.

        Returns individual dimension scores already weighted.
        """
        goal_lower = goal.lower()

        # RoleFit: how well does this role match the goal?
        role_info = self.cube.get_role_info(role)
        role_text = ""
        if role_info:
            role_text = (role_info.get("description", "") + " " +
                        " ".join(role_info.get("skills", [])) + " " +
                        role_info.get("display", role))
        role_text = role_text.lower()

        # Chinese-aware matching: count characters from goal that appear in role text
        match_count = sum(1 for c in goal_lower if c in role_text)
        role_score = min(match_count / max(len(goal_lower), 1), 1.0)

        # WorkflowEff: how relevant is this stage to the goal?
        stage_text = f"{stage_name} {stage_key}".lower()
        wf_match = sum(1 for c in goal_lower if c in stage_text)
        workflow_score = min(wf_match / max(len(goal_lower), 1), 1.0)

        # KnowledgeRel: how relevant is the knowledge content?
        knowledge_text = ""
        for z_path in z_paths:
            content = self.cube._knowledge.get(z_path, "")
            knowledge_text += content[:500].lower() + " "
        kb_match = sum(1 for c in goal_lower if c in knowledge_text)
        knowledge_score = min(kb_match / max(len(goal_lower), 1), 1.0)

        return {
            f"W1×RoleFit({role})": round(weights["W1"] * role_score, 4),
            f"W2×WorkflowEff({stage_key})": round(weights["W2"] * workflow_score, 4),
            f"W3×KnowledgeRel": round(weights["W3"] * knowledge_score, 4),
        }
