#!/usr/bin/env python3
"""
Agent Knowledge Cube — CLI

Usage:
  cube list roles [--category <cat>]
  cube list workflows
  cube list stages <workflow>
  cube list categories
  cube knowledge <role> <stage>
  cube agent <role> <workflow> [--stages s1,s2,...]
  cube find [--role <r>] [--workflow <w>]
  cube stats
  cube viz <role> [--workflow <w>]
"""

import argparse
import sys
from pathlib import Path
from .loader import Cube


def find_cube_root() -> Path:
    """Find the cube root directory by looking for _cube_index.yaml."""
    # Check common locations
    candidates = [
        Path.cwd(),
        Path.cwd() / "agent-knowledge-cube",
        Path.home() / "agent-knowledge-cube",
        Path(__file__).resolve().parent.parent,
    ]
    for c in candidates:
        if (c / "_cube_index.yaml").exists():
            return c
    raise FileNotFoundError(
        "Cube root not found. Run from the repo directory or pass --path."
    )


def main():
    parser = argparse.ArgumentParser(
        description="Agent Knowledge Cube — 3D Knowledge Constraint Framework"
    )
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Path to cube root directory",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    list_parser = subparsers.add_parser("list", help="List resources")
    list_parser.add_argument("resource", choices=["roles", "workflows", "stages", "categories"])
    list_parser.add_argument("workflow", nargs="?", help="Workflow name (for stages)")

    # knowledge (single stage)
    know_parser = subparsers.add_parser("knowledge", help="Get knowledge for (role, stage)")
    know_parser.add_argument("role", type=str)
    know_parser.add_argument("stage", type=str)

    # agent (multi-stage)
    agent_parser = subparsers.add_parser("agent", help="Get all knowledge for an agent")
    agent_parser.add_argument("role", type=str)
    agent_parser.add_argument("workflow", type=str)
    agent_parser.add_argument("--stages", type=str, help="Comma-separated stage IDs")

    # find
    find_parser = subparsers.add_parser("find", help="Find cube coordinates")
    find_parser.add_argument("--role", type=str)
    find_parser.add_argument("--workflow", type=str)

    # stats
    subparsers.add_parser("stats", help="Show cube statistics")

    # viz
    viz_parser = subparsers.add_parser("viz", help="Visualize knowledge coverage for a role")
    viz_parser.add_argument("role", type=str)
    viz_parser.add_argument("--workflow", type=str)

    # optimize
    opt_parser = subparsers.add_parser("optimize", help="Weighted optimization: Score = W1×X + W2×Y + W3×Z")
    opt_parser.add_argument("goal", type=str, help="Natural language goal description")
    opt_parser.add_argument("--top-k", type=int, default=3, help="Number of results (default: 3)")
    opt_parser.add_argument("--mode", choices=["heuristic", "llm"], default="heuristic",
                            help="Optimization mode: heuristic (keyword-based) or llm (calls LLM)")
    opt_parser.add_argument("--roles", type=str, help="Comma-separated role filter")
    opt_parser.add_argument("--workflows", type=str, help="Comma-separated workflow filter")
    opt_parser.add_argument("--weights", action="store_true", help="Show only the optimal weights")

    # compare
    cmp_parser = subparsers.add_parser("compare", help="Compare heuristic vs LLM optimization")
    cmp_parser.add_argument("goal", type=str, help="Natural language goal description")

    args = parser.parse_args()

    try:
        root = Path(args.path) if args.path else find_cube_root()
        cube = Cube.load(root)
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    if args.command == "list":
        _handle_list(cube, args)
    elif args.command == "knowledge":
        _handle_knowledge(cube, args)
    elif args.command == "agent":
        _handle_agent(cube, args)
    elif args.command == "find":
        _handle_find(cube, args)
    elif args.command == "stats":
        _handle_stats(cube)
    elif args.command == "viz":
        _handle_viz(cube, args)
    elif args.command == "optimize":
        _handle_optimize(cube, args)
    elif args.command == "compare":
        _handle_compare(cube, args)


def _handle_list(cube: Cube, args):
    if args.resource == "roles":
        roles = cube.list_roles()
        if not roles:
            print("No roles loaded.")
            return
        print(f"\n{'Name':<25} {'Category':<18} {'Description'}")
        print("-" * 80)
        for r in roles:
            desc = r["description"][:50].replace("\n", " ")
            print(f"{r['name']:<25} {r['category']:<18} {desc}")

    elif args.resource == "workflows":
        wfs = cube.list_workflows()
        if not wfs:
            print("No workflows loaded.")
            return
        print(f"\n{'Name':<30} {'Stages':<8} {'Description'}")
        print("-" * 75)
        for w in wfs:
            desc = w["description"][:50].replace("\n", " ")
            print(f"{w['name']:<30} {w['stages']:<8} {desc}")

    elif args.resource == "stages":
        if not args.workflow:
            print("❌ Usage: cube list stages <workflow>")
            return
        stages = cube.list_stages(args.workflow)
        if not stages:
            print(f"No stages found for workflow: {args.workflow}")
            return
        print(f"\nStages for '{args.workflow}':")
        print("-" * 60)
        for s in stages:
            roles = ", ".join(s["roles"])
            print(f"  {s['id']:<30} roles: [{roles}]")

    elif args.resource == "categories":
        cats = cube.list_categories()
        print("\nRole Categories:")
        for c in cats:
            count = len(cube.list_roles(category=c))
            print(f"  {c:<20} ({count} roles)")


def _handle_knowledge(cube: Cube, args):
    slices = cube.get_knowledge(args.role, args.stage)
    if not slices:
        print(f"No knowledge found for (role={args.role}, stage={args.stage})")
        return
    print(f"\nKnowledge for '{args.role}' @ '{args.stage}':")
    print("=" * 60)
    for s in slices:
        print(f"\n📄 {s['path']}")
        print("-" * 40)
        # Show first 20 lines
        lines = s["content"].splitlines()
        for line in lines[:20]:
            print(line)
        if len(lines) > 20:
            print(f"... ({len(lines) - 20} more lines)")


def _handle_agent(cube: Cube, args):
    stages = args.stages.split(",") if args.stages else None
    text = cube.get_knowledge_for_agent(args.role, args.workflow, stages)
    if not text:
        print(f"No knowledge found for agent (role={args.role}, workflow={args.workflow})")
        return
    print(text)


def _handle_find(cube: Cube, args):
    entries = cube.find_coordinates(role=args.role, workflow=args.workflow)
    if not entries:
        print("No matching entries.")
        return
    print(f"\nFound {len(entries)} entries:")
    print("-" * 70)
    for e in entries:
        z_list = ", ".join(e.get("z", []))
        print(f"  x={e['x']:<25} y={e['y']:<40}")
        print(f"  z=[{z_list}]")
        print()


def _handle_stats(cube: Cube):
    s = cube.stats()
    print("\n📊 Agent Knowledge Cube — Statistics")
    print("=" * 45)
    print(f"  Version:                   v{s['version']}")
    print(f"  Index entries:             {s['index_entries']}")
    print(f"  Unique roles:              {s['unique_roles']}")
    print(f"  Unique workflows:          {s['unique_workflows']}")
    print(f"  Total knowledge refs:      {s['total_knowledge_refs']}")
    print(f"  Loaded role definitions:   {s['loaded_roles']}")
    print(f"  Loaded workflow defs:      {s['loaded_workflows']}")
    print(f"  Loaded knowledge files:    {s['loaded_knowledge_files']}")
    print()


def _handle_viz(cube: Cube, args):
    """Simple ASCII visualization of a role's knowledge coverage."""
    entries = cube.find_coordinates(role=args.role)
    if not entries:
        print(f"No cube entries for role: {args.role}")
        return

    role_info = cube.get_role_info(args.role)
    display = role_info["display"] if role_info else args.role

    print(f"\n🧊 Knowledge Cube — Role: {display} ({args.role})")
    print("=" * 60)

    # Group by workflow
    by_workflow: dict = {}
    for e in entries:
        wf_name = e["y"].split(":")[0]
        by_workflow.setdefault(wf_name, []).append(e)

    for wf_name, wf_entries in sorted(by_workflow.items()):
        wf_info = cube.get_workflow_info(wf_name)
        wf_display = wf_info["display"] if wf_info else wf_name
        print(f"\n  📋 {wf_display}")
        print(f"  {'─' * 50}")

        for e in wf_entries:
            stage_id = e["y"].split(":")[1] if ":" in e["y"] else e["y"]
            z_count = len(e.get("z", []))
            z_files = ", ".join(str(z) for z in e.get("z", [])[:3])
            if z_count > 3:
                z_files += f" ... (+{z_count - 3})"
            print(f"    ├─ {stage_id:<30} 📄 {z_count} files")
            print(f"    └─ Total: {len(wf_entries)} stages")


def _handle_optimize(cube: Cube, args):
    """Weighted optimization: find best (x, y, z) for a goal."""
    from .optimizer import WeightedOptimizer

    optimizer = WeightedOptimizer(cube)

    roles = args.roles.split(",") if args.roles else None
    workflows = args.workflows.split(",") if args.workflows else None

    # Just show weights
    if args.weights:
        weights = optimizer.optimize_weights(args.goal, mode=args.mode, available_roles=roles, available_workflows=workflows)
        print(f"\n🎯 Goal: {args.goal}")
        print(f"📊 Optimal weights ({args.mode} mode):")
        print(f"   W1 (Role):     {weights['W1']:.2f}")
        print(f"   W2 (Workflow): {weights['W2']:.2f}")
        print(f"   W3 (Knowledge):{weights['W3']:.2f}")
        return

    # Full optimization
    results = optimizer.optimize(args.goal, top_k=args.top_k, mode=args.mode,
                                 available_roles=roles, available_workflows=workflows)

    print(f"\n🎯 Goal: {args.goal}")
    print(f"📊 Mode: {args.mode} | Top-{args.top_k} results")
    print("=" * 70)

    for i, r in enumerate(results, 1):
        print(f"\n  #{i}  Score: {r.score:.4f}  |  {r.role} @ {r.stage_name}")
        print(f"      {'─' * 55}")
        for dim, score in r.scores.items():
            print(f"      {dim:<45} {score:.4f}")
        print(f"      Knowledge: {', '.join(r.knowledge_paths[:3])}")
        if len(r.knowledge_paths) > 3:
            print(f"                 ... +{len(r.knowledge_paths) - 3} more")


def _handle_compare(cube: Cube, args):
    """Compare heuristic vs LLM optimization."""
    from .optimizer import WeightedOptimizer

    optimizer = WeightedOptimizer(cube)

    print(f"\n🎯 Goal: {args.goal}")
    print("=" * 70)

    for mode in ["heuristic", "llm"]:
        print(f"\n📊 Mode: {mode}")
        print(f"{'─' * 50}")
        results = optimizer.optimize(args.goal, top_k=3, mode=mode)
        for i, r in enumerate(results, 1):
            print(f"  #{i}  {r.score:.4f}  |  {r.role} @ {r.stage_name}")
            for dim, score in r.scores.items():
                print(f"      {dim:<50} {score:.4f}")
        print()


if __name__ == "__main__":
    main()
