# 🧊 Agent Knowledge Cube

**三维知识约束框架 — 3D Knowledge Constraint Framework**

```
          Z (Knowledge Base)
          ↑  用什么做
          |
          |            Y (Workflow)
          |            ←────────── 怎么做
          |
          |         ┌────┬────┬────┐
          |         │    │    │    │
          |         ├────┼────┼────┤
          |         │    │ ●  │    │  ← (x, y, z) 交叉点
          |         ├────┼────┼────┤
          |         │    │    │    │
          |         └────┴────┴────┘
          +─────────────────────────→
                 X (Role)  谁做
```

## The Concept

A structured framework that constrains AI Agents along three orthogonal dimensions:

| Axis | Question | Meaning |
|------|----------|---------|
| **X — Role** | 谁做 (Who) | The agent's professional persona, behavioral boundary, responsibility scope |
| **Y — Workflow** | 怎么做 (How) | The process orchestration — sequence, handoff, parallel execution |
| **Z — Knowledge** | 用什么做 (With What) | The knowledge base slice accessible to each (x, y) coordinate |

Every point (x, y, z) in this cube defines a **knowledge slice**: what a specific role needs to know at a specific workflow stage.

## The Problem

Current multi-agent systems suffer from three fundamental design flaws:

### ❌ Role Collision
Multiple agents in the same workflow talk over each other because their knowledge boundaries overlap. Customer service and technical support both access the same docs — they contradict each other.

### ❌ Firehose Knowledge
Every agent gets the entire knowledge base dumped into context. Token waste, hallucination risk, no precision.

### ❌ Prompt-Based Constraints
We try to solve boundary problems with prose ("you are a helpful assistant who does NOT handle refunds..."). Prompts are soft constraints — they leak.

## The Solution

**Hard constraints through structure.**

Instead of telling an agent what NOT to do, give it only what it CAN see.

```
Agent_A = (x=客服,  y=售后流程, z=客服知识子集)
Agent_B = (x=技术,  y=售后流程, z=技术知识子集)
```

Agent_A literally cannot access Agent_B's knowledge. Not because we told it not to — **because the knowledge isn't there**. This is the same principle as database column-level security: enforce at the storage layer, not the application layer.

## Why This Matters

### 🧠 For AI Engineers
- **Token efficiency**: Each agent loads only its (x, y, z) slice → 60-80% context reduction
- **Deterministic boundaries**: Knowledge isolation prevents role drift and hallucination chains
- **Observable constraints**: The cube is inspectable — you can see exactly what any agent can access

### 🏢 For Organizations
- **Enterprise knowledge management**: Map your org chart (X) × processes (Y) × knowledge domains (Z)
- **Onboarding**: New agents (or humans) query their (x, y) coordinates and get the exact knowledge they need
- **Cross-industry pattern**: Same workflow Y, different roles X, different knowledge Z — the framework is domain-agnostic

### 🤖 For Multi-Agent Systems
- **Constitutional architecture**: The cube acts as a "constitution" — not a prompt, but a structural constraint
- **Surgical context injection**: Each agent gets only what's relevant to its role and current workflow step
- **Graceful degradation**: If an agent fails, its (x, y, z) can be re-assigned without retraining

## Project Structure

```
agent-knowledge-cube/
│
├── X_roles/                  # 角色目录 — All possible agent personas
│   ├── product-manager.yaml
│   ├── software-engineer.yaml
│   ├── sales.yaml
│   ├── customer-support.yaml
│   └── ...
│
├── Y_workflows/              # 工作流目录 — Process orchestrations
│   ├── software-development.yaml   # 需求→设计→编码→测试→部署
│   ├── customer-service.yaml       # 受理→诊断→解决→反馈
│   ├── marketing-campaign.yaml     # 策略→创意→执行→分析
│   └── ...
│
├── Z_knowledge/              # 知识库切片 — Knowledge domains & slices
│   ├── tech-stack.md
│   ├── product-specs/
│   ├── sop/
│   └── ...
│
├── _cube_index.yaml          # 三维索引矩阵 — The master index
│   # Maps every (x, y) → z slice(s)
│   # e.g. (engineer, code-review) → [code-standards.md, review-checklist.md]
│
├── experiments/              # 实验场 — Run experiments
│   ├── 001-customer-support-cube/
│   └── 002-dev-team-cube/
│
└── README.md
```

## Getting Started

This is a **concept-first** repository. We're defining the specification before the implementation.

### 1. Define Your Roles (X)

```yaml
# X_roles/software-engineer.yaml
name: software-engineer
display: 软件工程师
description: >
  Writes, reviews, and maintains production code.
  Responsible for implementation quality and technical decisions.
constraints:
  cannot: ["approve budget", "set product roadmap"]
  must_follow: ["code-standards", "review-process"]
```

### 2. Define Your Workflow (Y)

```yaml
# Y_workflows/software-development.yaml
stages:
  - name: requirements-analysis
    roles: [product-manager, software-engineer]
    knowledge_slice: [product-specs, architecture-guide]
  - name: implementation
    roles: [software-engineer]
    knowledge_slice: [tech-stack, code-standards]
  - name: code-review
    roles: [software-engineer, qa-engineer]
    knowledge_slice: [review-checklist, testing-guide]
```

### 3. Slice Your Knowledge (Z)

Slice your knowledge base so each (x, y) coordinate points to exactly what's needed — nothing more, nothing less.

### 4. The Cube Index

```yaml
# _cube_index.yaml
cube:
  - x: software-engineer
    y: implementation
    z: [tech-stack/coding-guide.md, code-standards/python.md]
  - x: software-engineer
    y: code-review
    z: [code-standards/review-checklist.md, testing-guide.md]
  - x: product-manager
    y: requirements-analysis
    z: [product-specs/current.md, roadmap.md]
```

## Related Work

| Project | Roles (X) | Workflow (Y) | Knowledge (Z) | Notes |
|---------|-----------|-------------|---------------|-------|
| **MetaGPT** | ✅ Strong | ✅ SOP-based | ❌ None | Role→Pipeline only |
| **CrewAI** | ✅ YAML-defined | ✅ Task chains | ❌ External RAG | No knowledge isolation |
| **ChatDev** | ✅ Org roles | ✅ Phased | ❌ None | Software only |
| **LangGraph** | ❌ None | ✅ DAG/Graph | ❌ Up to you | Lowest-level flexibility |
| **OpenPersona** | ✅ Lifecycle | ❌ None | ❌ None | Role definition only |
| **WeKnora** | ❌ None | ❌ None | ✅ RAG+Wiki | Knowledge only |
| **sibyl** | ✅ Role graphs | ❌ None | ✅ Graph | Closest to Z-axis isolation |
| **✨ This Project** | **✅** | **✅** | **✅** | **All three, integrated** |

## Roadmap

- [ ] Phase 1: Concept & specification (we are here)
- [ ] Phase 2: Taxonomy — build comprehensive X/Y/Z catalogs
- [ ] Phase 3: Reference implementation — Python library for cube-indexed agent constraints
- [ ] Phase 4: Framework adapters — CrewAI / LangGraph / MetaGPT integration
- [ ] Phase 5: Visualizer — 3D cube browser for knowledge slices

## License

MIT

## Contribute

This is an open concept. If you've felt the pain of agent role collision or prompt-bloated systems, this space is for you.
