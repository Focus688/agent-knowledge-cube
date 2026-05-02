# 🧊 Agent Knowledge Cube — A 3D Knowledge Constraint Framework for AI Agents

## The Problem

Multi-agent systems today have a fundamental design flaw: **every agent sees everything**.

You give Customer Support the entire knowledge base, including pricing strategies. You give Engineering the full product roadmap, including unannounced features. Then you write a prompt saying "don't talk about things outside your scope" — and wonder why agents hallucinate, contradict each other, and burn tokens.

**Prompts are soft constraints. They leak.**

## The Idea

What if we bake the constraints into the architecture itself?

```
X — Role (who)       →  Engineering / Sales / Support / PM
Y — Workflow (how)   →  Development / Sales Pipeline / Customer Service
Z — Knowledge (with) →  The knowledge slice at each (x, y) coordinate
```

Every point (x, y, z) in the cube defines a **precise knowledge boundary**: an agent at coordinate (engineer, code-review) gets code standards and review checklists — not pricing guides or contract templates.

**Not because we told it not to look. Because the knowledge isn't there.**

## What's in This Repo

| Asset | Status |
|-------|--------|
| 📖 **Concept + Specification** | ✅ Complete (README) |
| 👥 **X — Role Catalog** | ✅ 16 roles across 8 categories |
| 🔄 **Y — Workflow Catalog** | ✅ 5 workflows (24 stages total) |
| 📚 **Z — Knowledge Base** | ✅ 74 knowledge files across 9 domains |
| 🗺️ **Cube Index** | ✅ 54 entries, 128 knowledge references |
| 🐍 **Python Library** | ✅ `pip install` → query the cube via CLI |
| 🧪 **Experiment Protocol** | ✅ MVP validation methodology |

## Quick Demo

```bash
pip install -e /path/to/agent-knowledge-cube

# What does a software engineer need during implementation?
cube knowledge software-engineer software-development:implementation

# What does a sales rep need during the close stage?
cube knowledge sales-representative sales-pipeline:close

# What's the full context for a customer support agent?
cube agent customer-support-agent customer-service
```

The key validation: **role isolation works at the data layer**.

```python
# Engineer can access engineering knowledge
cube.get_knowledge('software-engineer', 'software-development:implementation')
# → returns code-standards, tech-stack, architecture-guide

# Engineer CANNOT access sales knowledge
cube.get_knowledge('software-engineer', 'sales-pipeline:close')
# → returns empty
```

## Why This Matters

1. **60-80% token reduction** — each agent loads only its slice
2. **Zero role collision** — knowledge boundaries are structural, not prompt-based
3. **Fully inspectable** — you can see exactly what any agent can access
4. **Framework-agnostic** — adapt it to CrewAI, LangGraph, MetaGPT, or your own stack

## Where This Is Going

- **Phase 3 (next)**: Reference implementation — Python library for runtime constraint enforcement
- **Phase 4**: Framework adapters — plug into CrewAI / LangGraph / MetaGPT
- **Phase 5**: Visualizer — 3D cube browser to explore knowledge slices

## I Want Your Feedback

This is an open concept. A few questions for the community:

1. Have you encountered the "role collision" problem in your agent setups?
2. Would a framework adapter (CrewAI plugin / LangGraph integration) make this practical for you?
3. What industries or workflows would you most want to see cataloged?
4. Is the YAML-based role definition format extensible enough, or would you prefer JSON schema / Pydantic models?

Let's discuss. The cube is just the container — the content should come from the community.

---

*Built by [@Focus688](https://github.com/Focus688)*
