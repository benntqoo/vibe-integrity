from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path


EXPECTED_SKILLS = [
    "spec-architect",
    "spec-to-codebase",
    "spec-contract-diff",
    "spec-driven-test",
    "spec-traceability",
    "sdd-release-guard",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_file(path: Path) -> None:
    if not path.exists():
        raise RuntimeError(f"Missing file: {path}")


def pick_schema_states(schema: dict) -> list[str]:
    states = schema.get("$defs", {}).get("state", {}).get("enum", [])
    if states:
        return states
    return schema.get("enums", {}).get("state", {}).get("items", {}).get("enum", [])


def parse_paths(raw_values: list[str]) -> list[Path]:
    paths: list[Path] = []
    for raw in raw_values:
        for part in raw.split(os.pathsep):
            value = part.strip()
            if value:
                paths.append(Path(value).resolve())
    return paths


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []
    for path in paths:
        key = str(path).lower()
        if key not in seen:
            seen.add(key)
            out.append(path)
    return out


def find_orchestrator_path(skills_paths: list[Path]) -> Path | None:
    for skills_path in skills_paths:
        candidate = skills_path / "sdd-orchestrator"
        if (candidate / "sdd-machine-schema.json").exists() and (candidate / "sdd-gate-checklist.json").exists():
            return candidate
        for schema_candidate in skills_path.rglob("sdd-machine-schema.json"):
            parent = schema_candidate.parent
            if parent.name != "sdd-orchestrator":
                continue
            if (parent / "sdd-gate-checklist.json").exists():
                return parent
    return None


def find_skill_file(skills_paths: list[Path], skill: str, recursive: bool) -> Path:
    direct_candidates: list[Path] = []
    recursive_candidates: list[Path] = []
    for skills_path in skills_paths:
        direct = skills_path / skill / "SKILL.md"
        if direct.exists():
            direct_candidates.append(direct)
        if recursive:
            for candidate in skills_path.rglob("SKILL.md"):
                if candidate.parent.name == skill:
                    recursive_candidates.append(candidate)
    all_candidates = direct_candidates + recursive_candidates
    if not all_candidates:
        raise RuntimeError(f"SKILL.md not found for {skill} in: {', '.join(str(p) for p in skills_paths)}")
    return sorted(all_candidates, key=lambda p: (len(p.parts), str(p)))[0]


def load_config(config_path: Path | None) -> dict:
    if config_path is None:
        return {}
    ensure_file(config_path)
    return read_json(config_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=os.environ.get("SDD_VALIDATE_CONFIG"))
    parser.add_argument("--root-path")
    parser.add_argument("--skills-path", action="append")
    parser.add_argument("--orchestrator-path")
    parser.add_argument("--schema-path")
    parser.add_argument("--checklist-path")
    parser.add_argument("--recursive-search", choices=["true", "false"])
    args = parser.parse_args()

    config_path = Path(args.config).resolve() if args.config else None
    config = load_config(config_path)

    root_raw = args.root_path or os.environ.get("SDD_ROOT_PATH") or config.get("root_path") or str(Path(__file__).resolve().parents[2])
    root_path = Path(root_raw).resolve()

    skills_raw_values: list[str] = []
    if args.skills_path:
        skills_raw_values.extend(args.skills_path)
    if os.environ.get("SDD_SKILLS_PATHS"):
        skills_raw_values.append(os.environ["SDD_SKILLS_PATHS"])
    if isinstance(config.get("skills_paths"), list):
        skills_raw_values.extend(str(item) for item in config["skills_paths"])
    if not skills_raw_values:
        skills_raw_values.append(str(root_path / "skills"))
    skills_paths = unique_paths(parse_paths(skills_raw_values))

    orchestrator_raw = args.orchestrator_path or os.environ.get("SDD_ORCHESTRATOR_PATH") or config.get("orchestrator_path")
    orchestrator_path = Path(orchestrator_raw).resolve() if orchestrator_raw else find_orchestrator_path(skills_paths)
    if orchestrator_path is None:
        raise RuntimeError("Unable to resolve sdd-orchestrator path from configured skills paths")

    if orchestrator_path.parent not in skills_paths:
        skills_paths = unique_paths(skills_paths + [orchestrator_path.parent])

    schema_raw = args.schema_path or os.environ.get("SDD_SCHEMA_PATH") or config.get("schema_path")
    checklist_raw = args.checklist_path or os.environ.get("SDD_CHECKLIST_PATH") or config.get("checklist_path")
    schema_path = Path(schema_raw).resolve() if schema_raw else orchestrator_path / "sdd-machine-schema.json"
    checklist_path = Path(checklist_raw).resolve() if checklist_raw else orchestrator_path / "sdd-gate-checklist.json"

    recursive_raw = args.recursive_search or os.environ.get("SDD_RECURSIVE_SEARCH")
    if recursive_raw is None and config.get("recursive_search") is not None:
        recursive_raw = "true" if config.get("recursive_search") else "false"
    recursive_search = False if recursive_raw == "false" else True

    ensure_file(schema_path)
    ensure_file(checklist_path)

    schema = read_json(schema_path)
    checklist = read_json(checklist_path)

    for skill in EXPECTED_SKILLS:
        skill_file = find_skill_file(skills_paths, skill, recursive_search)
        content = skill_file.read_text(encoding="utf-8")
        if not re.search(r"sdd-machine-schema\.json", content):
            raise RuntimeError(f"{skill_file} missing schema reference")
        if not re.search(r"sdd-gate-checklist\.json", content):
            raise RuntimeError(f"{skill_file} missing checklist reference")
        if "## Invocation Alignment" not in content:
            raise RuntimeError(f"{skill_file} missing Invocation Alignment section")
        if "only state-transition entry" not in content:
            raise RuntimeError(f"{skill_file} missing orchestrator-first rule")
        if "must not promote state" not in content:
            raise RuntimeError(f"{skill_file} missing direct invocation guard")

    checklist_skills = checklist.get("skills", {}).keys()
    missing_in_checklist = [skill for skill in EXPECTED_SKILLS if skill not in checklist_skills]
    if missing_in_checklist:
        raise RuntimeError(f"Checklist missing skills: {', '.join(missing_in_checklist)}")

    state_flow = checklist.get("state_flow", [])
    if len(state_flow) < 2:
        raise RuntimeError("Invalid state_flow: requires at least 2 states")

    schema_states = pick_schema_states(schema)
    if not schema_states:
        raise RuntimeError("Schema state enum not found")
    if len(schema_states) != len(state_flow) or any(state not in state_flow for state in schema_states):
        raise RuntimeError("State enum mismatch between schema and checklist")

    for skill in EXPECTED_SKILLS:
        node = checklist["skills"][skill]
        if not node.get("entry_state") or not node.get("required_outputs") or not node.get("gate_checks"):
            raise RuntimeError(f"Checklist section incomplete for {skill}")

    print("SDD validation passed")
    print(f"Root: {root_path}")
    print("Skills paths:")
    for skills_path in skills_paths:
        print(f"- {skills_path}")
    print(f"Schema: {schema_path}")
    print(f"Checklist: {checklist_path}")


if __name__ == "__main__":
    main()
