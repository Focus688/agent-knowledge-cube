"""
Agent Knowledge Cube — Core Library

A structured framework that constrains AI Agents along three dimensions:
  X — Role (who)
  Y — Workflow (how)
  Z — Knowledge (with what)

Each (x, y) coordinate maps to a precise knowledge slice, enabling:
- Role-isolated knowledge access (no collision)
- Surgical context injection (no token waste)
- Deterministic agent boundaries (no prompt leakage)
"""

from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import yaml


class Cube:
    """The master index that maps (role, stage) → knowledge slices."""

    def __init__(self, base_path: Path):
        self.base_path = Path(base_path).resolve()
        self._index: List[Dict] = []
        self._roles: Dict[str, Dict] = {}
        self._workflows: Dict[str, Dict] = {}
        self._knowledge: Dict[str, str] = {}

    @classmethod
    def load(cls, base_path: str | Path) -> "Cube":
        """Load a cube from a directory containing X_roles/, Y_workflows/,
        Z_knowledge/, and _cube_index.yaml."""
        cube = cls(Path(base_path))
        cube._load_index()
        cube._load_roles()
        cube._load_workflows()
        cube._load_knowledge()
        return cube

    def _load_index(self):
        index_path = self.base_path / "_cube_index.yaml"
        if not index_path.exists():
            raise FileNotFoundError(f"Cube index not found: {index_path}")
        with open(index_path) as f:
            data = yaml.safe_load(f)
        self._index = data.get("cube", [])
        self._version = data.get("version", "1.0")

    def _load_roles(self):
        roles_dir = self.base_path / "X_roles"
        if not roles_dir.exists():
            return
        for yaml_file in sorted(roles_dir.rglob("*.yaml")):
            with open(yaml_file) as f:
                role_data = yaml.safe_load(f)
            if role_data and "name" in role_data:
                self._roles[role_data["name"]] = role_data

    def _load_workflows(self):
        workflows_dir = self.base_path / "Y_workflows"
        if not workflows_dir.exists():
            return
        for yaml_file in sorted(workflows_dir.glob("*.yaml")):
            with open(yaml_file) as f:
                wf_data = yaml.safe_load(f)
            if wf_data and "name" in wf_data:
                self._workflows[wf_data["name"]] = wf_data

    def _load_knowledge(self):
        knowledge_dir = self.base_path / "Z_knowledge"
        if not knowledge_dir.exists():
            return
        for md_file in sorted(knowledge_dir.rglob("*.md")):
            rel_path = md_file.relative_to(knowledge_dir)
            with open(md_file) as f:
                self._knowledge[str(rel_path)] = f.read()

    # ── Query API ──────────────────────────────────────────────

    def get_knowledge(
        self, role: str, stage: str, include_optional: bool = False
    ) -> List[Dict[str, str]]:
        """Get knowledge slices for a (role, stage) coordinate.

        Returns a list of dicts: [{"path": "...", "content": "..."}]
        """
        results = []
        for entry in self._index:
            if entry.get("x") == role and entry.get("y") == stage:
                for z_path in entry.get("z", []):
                    content = self._get_slice_content(z_path)
                    if content is not None:
                        results.append({"path": z_path, "content": content})
        return results

    def get_knowledge_text(
        self, role: str, stage: str, separator: str = "\n\n---\n\n"
    ) -> str:
        """Get concatenated knowledge text for a (role, stage) coordinate."""
        slices = self.get_knowledge(role, stage)
        if not slices:
            return ""
        texts = []
        for s in slices:
            header = f"# {s['path']}\n"
            texts.append(header + s["content"])
        return separator.join(texts)

    def get_knowledge_for_agent(
        self, role: str, workflow: str, stages: Optional[List[str]] = None
    ) -> str:
        """Get all knowledge an agent needs across multiple workflow stages.

        This is the primary API for agent context injection.
        """
        wf = self._workflows.get(workflow)
        if not wf:
            return ""
        if stages is None:
            stages = [s["id"] for s in wf.get("stages", [])]

        all_texts = []
        for stage_id in stages:
            stage_key = f"{workflow}:{stage_id}"
            text = self.get_knowledge_text(role, stage_key)
            if text:
                stage_name = self._get_stage_name(workflow, stage_id)
                header = f"## {stage_name} ({stage_key})"
                all_texts.append(header + "\n\n" + text)
        return "\n\n".join(all_texts)

    def get_role_info(self, role: str) -> Optional[Dict]:
        """Get role definition metadata."""
        return self._roles.get(role)

    def get_workflow_info(self, workflow: str) -> Optional[Dict]:
        """Get workflow definition."""
        return self._workflows.get(workflow)

    def list_roles(self, category: Optional[str] = None) -> List[Dict]:
        """List all available roles, optionally filtered by category."""
        results = []
        for name, data in self._roles.items():
            if category and data.get("category") != category:
                continue
            results.append({
                "name": name,
                "display": data.get("display", name),
                "category": data.get("category", ""),
                "description": data.get("description", ""),
            })
        return results

    def list_workflows(self) -> List[Dict]:
        """List all available workflows."""
        return [
            {
                "name": w["name"],
                "display": w.get("display", w["name"]),
                "description": w.get("description", ""),
                "stages": len(w.get("stages", [])),
            }
            for w in self._workflows.values()
        ]

    def list_stages(self, workflow: str) -> List[Dict]:
        """List all stages in a workflow."""
        wf = self._workflows.get(workflow)
        if not wf:
            return []
        return [
            {
                "id": s["id"],
                "name": s.get("name", s["id"]),
                "roles": s.get("roles", []),
            }
            for s in wf.get("stages", [])
        ]

    def list_categories(self) -> List[str]:
        """List role categories."""
        cats: Set[str] = set()
        for r in self._roles.values():
            cats.add(r.get("category", "uncategorized"))
        return sorted(cats)

    def find_coordinates(
        self, role: Optional[str] = None, workflow: Optional[str] = None
    ) -> List[Dict]:
        """Find all (x, y, z) entries matching optional filters."""
        results = []
        for entry in self._index:
            if role and entry.get("x") != role:
                continue
            if workflow and not entry.get("y", "").startswith(f"{workflow}:"):
                continue
            results.append(entry)
        return results

    def stats(self) -> Dict:
        """Get cube statistics."""
        unique_roles = set(e["x"] for e in self._index if "x" in e)
        unique_workflows = set(
            e["y"].split(":")[0] for e in self._index if "y" in e and ":" in e["y"]
        )
        total_z_refs = sum(len(e.get("z", [])) for e in self._index)
        return {
            "version": self._version,
            "index_entries": len(self._index),
            "unique_roles": len(unique_roles),
            "unique_workflows": len(unique_workflows),
            "total_knowledge_refs": total_z_refs,
            "loaded_roles": len(self._roles),
            "loaded_workflows": len(self._workflows),
            "loaded_knowledge_files": len(self._knowledge),
        }

    # ── Internal helpers ───────────────────────────────────────

    def _get_slice_content(self, z_path: str) -> Optional[str]:
        """Resolve a knowledge path (e.g. 'engineering/code-standards.md')
        to its content."""
        # Try exact match first
        if z_path in self._knowledge:
            return self._knowledge[z_path]
        # Try relative to Z_knowledge
        full_path = self.base_path / "Z_knowledge" / z_path
        if full_path.exists():
            with open(full_path) as f:
                return f.read()
        return None

    def _get_stage_name(self, workflow: str, stage_id: str) -> str:
        wf = self._workflows.get(workflow, {})
        for s in wf.get("stages", []):
            if s.get("id") == stage_id:
                return s.get("name", stage_id)
        return stage_id
