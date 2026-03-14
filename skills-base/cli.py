#!/usr/bin/env python3
"""
Skills Base - Unified CLI
==========================

Unified command-line interface for all skills-base and skills-sdd skills.

Usage:
    python cli.py <command> [options]
    
Commands:
    vibe-guard      - Run completion integrity check
    vibe-design     - Start requirement clarification
    vibe-debug      - Start debugging session
    vibe-init       - Initialize .vibe-integrity/ directory
    validate        - Run validation
    trigger         - Manage triggers
    bus             - Skill bus operations
    list            - List available skills
    help            - Show help

Examples:
    python cli.py vibe-guard --check
    python cli.py vibe-design --clarify "Implement login"
    python cli.py vibe-debug --analyze "login fails"
    python cli.py list --category completion-guard
    python cli.py validate --all
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

# === Configuration ===
SKILLS_BASE = Path(__file__).parent
SKILLS_SDD = Path(__file__).parent.parent / "skills-sdd"
REGISTRY = SKILLS_BASE / "skill-registry.json"


# === Registry ===

def load_registry() -> dict:
    """Load skill registry"""
    if REGISTRY.exists():
        with open(REGISTRY, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"skills": [], "workflows": {}}


def list_skills(category: Optional[str] = None, detailed: bool = False):
    """List available skills"""
    registry = load_registry()
    skills = registry.get("skills", [])
    
    if category:
        skills = [s for s in skills if s.get("category") == category]
    
    if detailed:
        print(f"\nAvailable Skills ({len(skills)}):\n")
        for s in skills:
            print(f"  {s.get('name'):20} [{s.get('category')}]")
            print(f"    {s.get('description', '')}")
            if s.get('implementation'):
                print(f"    → {s.get('implementation')}")
            print()
    else:
        for s in skills:
            print(f"{s.get('name'):20} [{s.get('category')}]")


def list_workflows():
    """List available workflows"""
    registry = load_registry()
    workflows = registry.get("workflows", {})
    
    print("\nAvailable Workflows:\n")
    for name, info in workflows.items():
        print(f"  {name}: {info.get('description', '')}")
        print(f"    Skills: {' → '.join(info.get('skills', []))}")
        print()


# === Commands ===

def cmd_vibe_guard(args):
    """Run vibe-guard"""
    script = SKILLS_BASE / "vibe-guard" / "validate-vibe-guard.py"
    
    cmd = [sys.executable, str(script)]
    
    if args.check:
        cmd.append("--check")
    if args.mode:
        cmd.extend(["--mode", args.mode])
    if args.category:
        cmd.extend(["--category", args.category])
    
    result = subprocess.run(cmd)
    return result.returncode


def cmd_vibe_design(args):
    """Run vibe-design"""
    script = SKILLS_BASE / "vibe-design" / "vibe-design.py"
    
    if args.interactive:
        cmd = [sys.executable, str(script), "--interactive"]
    elif args.clarify:
        cmd = [sys.executable, str(script), "--clarify", args.clarify]
        if args.topic:
            cmd.extend(["--topic", args.topic])
    elif args.record_decision:
        cmd = [sys.executable, str(script), "--record-decision", args.record_decision]
    else:
        script.parent / "vibe-design.py"
        print("Error: Specify --interactive, --clarify, or --record-decision")
        return 1
    
    result = subprocess.run(cmd)
    return result.returncode


def cmd_vibe_debug(args):
    """Run vibe-integrity-debug"""
    script = SKILLS_BASE / "vibe-integrity-debug" / "vibe_integrity_debug.py"
    
    if args.interactive:
        cmd = [sys.executable, str(script), "--interactive"]
    elif args.analyze:
        cmd = [sys.executable, str(script), "--analyze", args.analyze]
    elif args.record_risk:
        cmd = [sys.executable, str(script), "--record-risk", args.record_risk]
    else:
        print("Error: Specify --interactive, --analyze, or --record-risk")
        return 1
    
    result = subprocess.run(cmd)
    return result.returncode


def cmd_vibe_init(args):
    """Initialize .vibe-integrity/ directory"""
    vibe_dir = Path(".vibe-integrity")
    
    if vibe_dir.exists():
        print(f"[INFO] {vibe_dir} already exists")
    else:
        vibe_dir.mkdir(parents=True)
        print(f"[OK] Created {vibe_dir}")
    
    # Create template files
    template_dir = SKILLS_BASE / "vibe-integrity" / "template"
    
    if template_dir.exists():
        for template in template_dir.glob("*.schema.json"):
            target = vibe_dir / template.stem.replace(".schema", "") + ".yaml"
            if not target.exists():
                # Create from template
                import yaml
                data = _schema_to_yaml_template(template)
                target.write_text(data, encoding='utf-8')
                print(f"[OK] Created {target}")
    
    # Create .sdd-spec if needed
    sdd_spec = Path(".sdd-spec")
    if not sdd_spec.exists():
        sdd_spec.mkdir(parents=True)
        print(f"[OK] Created {sdd_spec}")
    
    print("\n[OK] Initialization complete!")
    return 0


def _schema_to_yaml_template(schema_path: Path) -> str:
    """Convert JSON schema to YAML template"""
    import yaml
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    
    # Extract example from schema
    props = schema.get("properties", {})
    
    # Build minimal template
    template = {}
    
    for key, value in props.items():
        if value.get("type") == "array":
            template[key] = []
        elif value.get("type") == "object":
            template[key] = {}
        else:
            template[key] = f"<{key}>"
    
    return yaml.dump(template, default_flow_style=False)


def cmd_validate(args):
    """Run validation"""
    if args.all:
        # Run all validations
        scripts = [
            SKILLS_BASE / "vibe-integrity" / "validate-vibe-integrity.py",
            SKILLS_BASE / "vibe-guard" / "validate-vibe-guard.py"
        ]
        
        for script in scripts:
            if script.exists():
                print(f"\n[Running] {script.name}")
                result = subprocess.run([sys.executable, str(script)])
                
                if result.returncode != 0:
                    print(f"[FAIL] {script.name} failed")
                    return result.returncode
        
        print("\n[OK] All validations passed")
        return 0
        
    elif args.integrity:
        script = SKILLS_BASE / "vibe-integrity" / "validate-vibe-integrity.py"
        result = subprocess.run([sys.executable, str(script)])
        return result.returncode
        
    else:
        print("Error: Specify --all or --integrity")
        return 1


def cmd_trigger(args):
    """Trigger management"""
    script = SKILLS_BASE / "vibe-guard" / "trigger-manager.py"
    
    cmd = [sys.executable, str(script)]
    
    if args.watch:
        cmd.append("--watch")
    elif args.daemon:
        cmd.append("--daemon")
        if args.interval:
            cmd.extend(["--interval", str(args.interval)])
    elif args.webhook:
        cmd.append("--webhook-server")
    elif args.check_phrase:
        cmd.extend(["--check-phrase", args.check_phrase])
    
    result = subprocess.run(cmd)
    return result.returncode


def cmd_bus(args):
    """Skill bus operations"""
    script = SKILLS_BASE / "skill-bus.py"
    
    cmd = [sys.executable, str(script)]
    
    if args.list_skills:
        cmd.append("--list")
        if args.category:
            cmd.extend(["--category", args.category])
    elif args.history:
        cmd.append("--history")
    elif args.call:
        cmd.extend(["--call", args.call])
        if args.operation:
            cmd.extend(["--operation", args.operation])
        if args.payload:
            cmd.extend(["--payload", args.payload])
    
    result = subprocess.run(cmd)
    return result.returncode


def cmd_sdd(args):
    """SDD workflow commands"""
    if args.orchestrate:
        # Run SDD orchestrator
        script = SKILLS_SDD / "sdd-orchestrator" / "validate-sdd.py"
        
        if not script.exists():
            print(f"[ERROR] SDD orchestrator not found: {script}")
            return 1
        
        cmd = [sys.executable, str(script)]
        
        if args.validate:
            cmd.append("--validate")
        
        result = subprocess.run(cmd)
        return result.returncode
    
    else:
        print("SDD commands:")
        print("  --orchestrate    Run SDD orchestrator")
        print("  --validate       Validate SDD state")
        return 0


# === Main ===

def main():
    parser = argparse.ArgumentParser(
        description="Skills Base - Unified CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list
  %(prog)s vibe-guard --check
  %(prog)s vibe-design --clarify "Implement login"
  %(prog)s vibe-debug --analyze "login fails"
  %(prog)s validate --all
  %(prog)s trigger --watch
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # list
    list_parser = subparsers.add_parser("list", help="List available skills")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--detailed", action="store_true", help="Show details")
    list_parser.add_argument("--workflows", action="store_true", help="List workflows")
    
    # vibe-guard
    guard_parser = subparsers.add_parser("vibe-guard", help="Run vibe-guard")
    guard_parser.add_argument("--check", action="store_true", help="Run check")
    guard_parser.add_argument("--mode", choices=["vibe", "standard", "strict"], help="Mode")
    guard_parser.add_argument("--category", help="Check category")
    
    # vibe-design
    design_parser = subparsers.add_parser("vibe-design", help="Run vibe-design")
    design_parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    design_parser.add_argument("--clarify", type=str, help="Start with input")
    design_parser.add_argument("--topic", type=str, help="Topic name")
    design_parser.add_argument("--record-decision", type=str, help="Record decision (JSON)")
    
    # vibe-debug
    debug_parser = subparsers.add_parser("vibe-debug", help="Run vibe-integrity-debug")
    debug_parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    debug_parser.add_argument("--analyze", type=str, help="Analyze issue")
    debug_parser.add_argument("--record-risk", type=str, help="Record risk (JSON)")
    
    # vibe-init
    init_parser = subparsers.add_parser("vibe-init", help="Initialize project")
    
    # validate
    val_parser = subparsers.add_parser("validate", help="Run validation")
    val_parser.add_argument("--all", action="store_true", help="Run all validations")
    val_parser.add_argument("--integrity", action="store_true", help="Validate integrity")
    
    # trigger
    trig_parser = subparsers.add_parser("trigger", help="Trigger management")
    trig_parser.add_argument("--watch", action="store_true", help="Watch for triggers")
    trig_parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    trig_parser.add_argument("--webhook", action="store_true", help="Start webhook server")
    trig_parser.add_argument("--interval", type=int, default=60, help="Check interval")
    trig_parser.add_argument("--check-phrase", type=str, help="Check phrase")
    
    # bus
    bus_parser = subparsers.add_parser("bus", help="Skill bus operations")
    bus_parser.add_argument("--list-skills", action="store_true", help="List skills")
    bus_parser.add_argument("--history", action="store_true", help="Show history")
    bus_parser.add_argument("--call", type=str, help="Call skill")
    bus_parser.add_argument("--operation", type=str, help="Operation")
    bus_parser.add_argument("--payload", type=str, help="JSON payload")
    bus_parser.add_argument("--category", help="Filter category")
    
    # sdd
    sdd_parser = subparsers.add_parser("sdd", help="SDD workflow")
    sdd_parser.add_argument("--orchestrate", action="store_true", help="Run orchestrator")
    sdd_parser.add_argument("--validate", action="store_true", help="Validate state")
    
    args = parser.parse_args()
    
    # Execute command
    if args.command == "list":
        if getattr(args, "workflows", False):
            list_workflows()
        else:
            list_skills(args.category, getattr(args, "detailed", False))
            
    elif args.command == "vibe-guard":
        return cmd_vibe_guard(args)
        
    elif args.command == "vibe-design":
        return cmd_vibe_design(args)
        
    elif args.command == "vibe-debug":
        return cmd_vibe_debug(args)
        
    elif args.command == "vibe-init":
        return cmd_vibe_init(args)
        
    elif args.command == "validate":
        return cmd_validate(args)
        
    elif args.command == "trigger":
        return cmd_trigger(args)
        
    elif args.command == "bus":
        return cmd_bus(args)
        
    elif args.command == "sdd":
        return cmd_sdd(args)
        
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
