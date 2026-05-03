# Agent Knowledge Cube — MVP Experiment

This experiment validates the core hypothesis:

> **Constraining an AI agent's knowledge by (role, workflow) coordinates produces more focused, conflict-free behavior than giving it unfettered access to the entire knowledge base.**

## Hypothesis

- **H0**: An agent with full knowledge access produces responses with role drift, contradictions, and token waste.
- **H1**: An agent with cube-sliced knowledge (only what its (x, y) coordinate needs) stays in role, produces precise responses, and consumes fewer tokens.

## Experiment Design

### Setup

```bash
# Install the cube library
pip install -e /path/to/agent-knowledge-cube

# Load the cube
python3
>>> from agent_knowledge_cube import Cube
>>> cube = Cube.load('.')
```

### Test 1: Knowledge Boundary Verification

Verify that role isolation works:

```python
# Engineer sees ONLY engineering knowledge
eng_text = cube.get_knowledge_text('software-engineer', 'software-development:implementation')
assert 'code-standards' in eng_text
assert 'contract' not in eng_text   # engineering doesn't see contract templates

# Customer support sees ONLY support knowledge
cs_text = cube.get_knowledge_text('customer-support-agent', 'customer-service:diagnose')
assert 'known-issues' in cs_text
assert 'deployment' not in cs_text  # support doesn't see deployment guides
```

**Expected result**: All assertions pass. Knowledge boundaries are enforced at the data layer,
not via prompts.

### Test 2: Token Efficiency Measurement

Compare context size between "full knowledge" and "cube-sliced" approaches:

```python
# Full knowledge: load everything
full_kb = "\n".join(cube._knowledge.values())
full_tokens = len(full_kb) / 4  # rough estimate

# Cube-sliced: only what the agent needs
sliced = cube.get_knowledge_for_agent('software-engineer', 'software-development')
sliced_tokens = len(sliced) / 4

print(f"Full KB:  ~{full_tokens:.0f} tokens")
print(f"Sliced:   ~{sliced_tokens:.0f} tokens")
print(f"Reduction: {100 - (sliced_tokens / full_tokens * 100):.0f}%")
```

**Expected result**: 60-90% token reduction depending on knowledge base size.

### Test 3: Role Conflict Detection

Simulate two agents in the same workflow accessing knowledge:

```python
# In a traditional setup, both agents load the full KB
# → Engineer might reference pricing, sales might suggest technical workarounds

# In cube setup:
sales_knowledge = cube.get_knowledge_for_agent('sales-representative', 'sales-pipeline')
cs_knowledge = cube.get_knowledge_for_agent('customer-support-agent', 'customer-service')

# Verify no overlap in forbidden domains
assert 'pricing' in sales_knowledge
assert 'pricing' not in cs_knowledge  # CS shouldn't discuss pricing
```

**Expected result**: Each agent's knowledge is strictly scoped to its role + workflow stage.

## Running the Experiment

```bash
# List all available roles
cube list roles

# List all workflows
cube list workflows

# Show stages in a workflow
cube list stages software-development

# Get knowledge for a specific coordinate
cube knowledge software-engineer software-development:implementation

# Get all knowledge for an agent across a workflow
cube agent software-engineer software-development

# Show cube statistics
cube stats
```

## Results Log

| Date | Test | Result | Notes |
|------|------|--------|-------|
| 2026-05-03 | Knowledge Boundary | ✅ Pass | Role isolation working at data layer |
| 2026-05-03 | Token Efficiency | ⏳ TBD | Need to measure with full load |
| 2026-05-03 | Role Conflict | ✅ Pass | No cross-domain knowledge leakage |

## What This Proves

1. **Hard constraints > soft prompts**: Knowledge isolation is structural, not textual
2. **Surgical injection > firehose**: Each agent gets only its (x, y) slice
3. **Deterministic boundaries**: The cube is inspectable — you can see exactly what any agent can access
4. **Framework-agnostic**: The cube is a specification, not a runtime — adapt it to CrewAI, LangGraph, or your own framework
