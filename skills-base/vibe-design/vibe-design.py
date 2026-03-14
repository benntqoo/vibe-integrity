#!/usr/bin/env python3
"""
Vibe Design - AI-assisted requirement clarification and design helper
=========================================================================

This skill performs:
1. Interactive requirement clarification using Socratic questioning
2. Automatic decision recording to .vibe-integrity/ YAML files
3. Design summary document generation

Usage:
    python vibe-design.py --clarify "Implement user login"
    python vibe-design.py --interactive
    python vibe-design.py --topic "payment-system"
"""

import argparse
import json
import os
import sys
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import re

# === Configuration ===
SKILLS_BASE = Path(__file__).parent
VIBE_DIR = Path(".vibe-integrity")
DOCS_PLANS_DIR = Path("docs/plans")

# Decision type mappings to YAML files
DECISION_FILE_MAP = {
    "database": "tech-records.yaml",
    "architecture": "tech-records.yaml",
    "frontend": "tech-records.yaml",
    "backend": "tech-records.yaml",
    "security": "tech-records.yaml",
    "performance": "tech-records.yaml",
    "integration": "dependency-graph.yaml",
    "module": "dependency-graph.yaml",
    "dependency": "dependency-graph.yaml",
    "schema": "schema-evolution.yaml",
    "data_model": "schema-evolution.yaml",
    "structure": "module-map.yaml",
    "risk": "risk-zones.yaml",
    "scope": "project.yaml",
}


@dataclass
class ClarificationQuestion:
    """A single clarification question"""
    id: str
    category: str
    question: str
    context: str
    priority: int  # 1-5, 1 is highest


@dataclass
class DesignDecision:
    """A captured design decision"""
    id: str
    date: str
    category: str
    title: str
    decision: str
    reason: str
    impact: str
    status: str = "completed"
    source_question: Optional[str] = None


@dataclass
class ClarificationSession:
    """Active clarification session"""
    session_id: str
    start_time: str
    user_input: str
    questions_asked: List[str] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    current_phase: str = "initial"
    topic: Optional[str] = None


class VibeDesign:
    """Main vibe-design skill implementation"""
    
    def __init__(self):
        self.session: Optional[ClarificationSession] = None
        self.vibe_writer_path = SKILLS_BASE / "vibe-integrity-writer" / "vibe-integrity-writer.py"
        
    # === Question Bank (Socratic-style) ===
    
    QUESTION_TEMPLATES = {
        "initial": [
            ClarificationQuestion(
                id="q1",
                category="scope",
                question="What is the core problem this feature solves?",
                context="Understanding the fundamental purpose",
                priority=1
            ),
            ClarificationQuestion(
                id="q2", 
                category="scope",
                question="Who are the primary users of this feature?",
                context="Identifying user segments",
                priority=1
            ),
            ClarificationQuestion(
                id="q3",
                category="scope",
                question="What is the expected outcome or deliverable?",
                context="Defining success criteria",
                priority=1
            ),
        ],
        "functional": [
            ClarificationQuestion(
                id="q4",
                category="functional",
                question="What are the key functional requirements?",
                context="Core features needed",
                priority=1
            ),
            ClarificationQuestion(
                id="q5",
                category="functional",
                question="What user interactions or flows are required?",
                context="User journey mapping",
                priority=2
            ),
            ClarificationQuestion(
                id="q6",
                category="functional",
                question="What data needs to be stored or processed?",
                context="Data requirements",
                priority=2
            ),
            ClarificationQuestion(
                id="q7",
                category="functional",
                question="What are the edge cases or error scenarios?",
                context="Boundary conditions",
                priority=3
            ),
        ],
        "technical": [
            ClarificationQuestion(
                id="q8",
                category="technical",
                question="Are there existing components this should integrate with?",
                context="Integration points",
                priority=2
            ),
            ClarificationQuestion(
                id="q9",
                category="technical",
                question="What are the performance expectations?",
                context="SLAs, latency, throughput",
                priority=2
            ),
            ClarificationQuestion(
                id="q10",
                category="technical",
                question="Are there security or compliance requirements?",
                context="Authentication, authorization, data protection",
                priority=2
            ),
        ],
        "constraints": [
            ClarificationQuestion(
                id="q11",
                category="constraints",
                question="What is the timeline or deadline?",
                context="Schedule constraints",
                priority=2
            ),
            ClarificationQuestion(
                id="q12",
                category="constraints",
                question="What is the budget or resource constraint?",
                context="Resource limitations",
                priority=3
            ),
            ClarificationQuestion(
                id="q13",
                category="constraints",
                question="Are there existing technical decisions that constrain this?",
                context="Architectural decisions",
                priority=2
            ),
        ],
    }
    
    def start_session(self, user_input: str, topic: Optional[str] = None) -> ClarificationSession:
        """Start a new clarification session"""
        self.session = ClarificationSession(
            session_id=f"session-{uuid.uuid4().hex[:8]}",
            start_time=datetime.now().isoformat(),
            user_input=user_input,
            topic=topic or self._extract_topic(user_input)
        )
        return self.session
    
    def _extract_topic(self, text: str) -> str:
        """Extract topic from user input"""
        # Simple extraction - take first few words
        words = re.findall(r'\w+', text.lower())
        return "-".join(words[:3]) if words else "unknown"
    
    def get_next_question(self) -> Optional[ClarificationQuestion]:
        """Get next question based on current phase"""
        if not self.session:
            return None
            
        # Determine phase
        if self.session.current_phase == "initial" and len(self.session.questions_asked) >= 3:
            self.session.current_phase = "functional"
        elif self.session.current_phase == "functional" and len(self.session.questions_asked) >= 7:
            self.session.current_phase = "technical"
        elif self.session.current_phase == "technical" and len(self.session.questions_asked) >= 10:
            self.session.current_phase = "constraints"
            
        phase_questions = self.QUESTION_TEMPLATES.get(self.session.current_phase, [])
        
        # Find next unanswered question
        for q in phase_questions:
            if q.id not in self.session.questions_asked:
                return q
                
        return None
    
    def record_answer(self, question_id: str, answer: str):
        """Record user's answer to a question"""
        if self.session:
            self.session.questions_asked.append(question_id)
            
    def add_decision(self, category: str, title: str, decision: str, 
                     reason: str, impact: str = "medium") -> DesignDecision:
        """Add a design decision"""
        decision_id = f"{category.upper()}-{len(self.session.decisions) + 1:03d}"
        
        decision_obj = DesignDecision(
            id=decision_id,
            date=datetime.now().strftime("%Y-%m-%d"),
            category=category,
            title=title,
            decision=decision,
            reason=reason,
            impact=impact,
            status="completed"
        )
        
        if self.session:
            self.session.decisions.append(asdict(decision_obj))
            
        return decision_obj
    
    def write_decision_to_yaml(self, decision: DesignDecision) -> bool:
        """Write decision to appropriate .vibe-integrity/ YAML file"""
        target_file = DECISION_FILE_MAP.get(decision.category, "tech-records.yaml")
        target_path = VIBE_DIR / target_file
        
        if not target_path.exists():
            print(f"[WARN] Target file does not exist: {target_path}")
            print(f"[INFO] Creating directory and file structure...")
            target_path.parent.mkdir(parents=True, exist_ok=True)
            # Create minimal structure
            if target_file == "tech-records.yaml":
                target_path.write_text("records: []\n")
            elif target_file == "dependency-graph.yaml":
                target_path.write_text("modules: {}\n")
            elif target_file == "schema-evolution.yaml":
                target_path.write_text("tables: []\n")
            elif target_file == "risk-zones.yaml":
                target_path.write_text("zones: []\n")
            elif target_file == "project.yaml":
                target_path.write_text("name: unknown\nversion: 0.0.1\n")
        
        # Use vibe-integrity-writer if available
        if self.vibe_writer_path.exists():
            return self._write_via_writer(decision, target_file)
        else:
            return self._write_direct(decision, target_path)
    
    def _write_via_writer(self, decision: DesignDecision, target_file: str) -> bool:
        """Use vibe-integrity-writer for safe updates"""
        import subprocess
        
        data_json = json.dumps(asdict(decision))
        
        cmd = [
            sys.executable,
            str(self.vibe_writer_path),
            "--target", target_file,
            "--operation", "add_record",
            "--data", data_json
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"[OK] Decision {decision.id} written to {target_file}")
                return True
            else:
                print(f"[WARN] Writer failed: {result.stderr}")
                return self._write_direct(decision, VIBE_DIR / target_file)
        except Exception as e:
            print(f"[WARN] Writer error: {e}")
            return self._write_direct(decision, VIBE_DIR / target_file)
    
    def _write_direct(self, decision: DesignDecision, target_path: Path) -> bool:
        """Direct YAML update (fallback)"""
        import yaml
        
        try:
            # Read existing
            if target_path.exists():
                with open(target_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
            else:
                data = {}
            
            # Add decision based on file type
            if "records" in data:
                data["records"].append(asdict(decision))
            elif "modules" in data:
                data["modules"][decision.id] = asdict(decision)
            elif "zones" in data:
                data["zones"].append(asdict(decision))
            else:
                # Generic append
                key = list(data.keys())[0] if data else "items"
                if isinstance(data.get(key), list):
                    data[key].append(asdict(decision))
            
            # Write back
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True)
            
            print(f"[OK] Decision {decision.id} written directly to {target_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Direct write failed: {e}")
            return False
    
    def generate_design_summary(self, output_path: Optional[Path] = None) -> Path:
        """Generate design summary markdown document"""
        if not self.session:
            raise ValueError("No active session")
            
        if output_path is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
            output_path = DOCS_PLANS_DIR / f"{date_str}-{self.session.topic}-design.md"
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build markdown
        md = []
        md.append(f"# Design Summary: {self.session.topic}")
        md.append("")
        md.append(f"**Session**: {self.session.session_id}")
        md.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Original Request")
        md.append("")
        md.append(f"> {self.session.user_input}")
        md.append("")
        md.append("---")
        md.append("")
        
        # Questions asked
        md.append("## Clarification Process")
        md.append("")
        for i, q_id in enumerate(self.session.questions_asked, 1):
            # Find question text
            for phase, questions in self.QUESTION_TEMPLATES.items():
                for q in questions:
                    if q.id == q_id:
                        md.append(f"{i}. **{q.question}** ({q.category})")
                        break
        md.append("")
        md.append("---")
        md.append("")
        
        # Decisions
        md.append("## Design Decisions")
        md.append("")
        if self.session.decisions:
            for d in self.session.decisions:
                md.append(f"### {d['id']}: {d['title']}")
                md.append("")
                md.append(f"**Category**: {d['category']}")
                md.append(f"**Decision**: {d['decision']}")
                md.append(f"**Reason**: {d['reason']}")
                md.append(f"**Impact**: {d['impact']}")
                md.append("")
        else:
            md.append("*No decisions recorded yet.*")
            md.append("")
        md.append("---")
        md.append("")
        
        # Next steps
        md.append("## Next Steps")
        md.append("")
        md.append("1. Review design decisions with stakeholders")
        md.append("2. Create detailed technical specification")
        md.append("3. Begin implementation using SDD workflow")
        md.append("")
        
        # Write file
        output_path.write_text("\n".join(md), encoding='utf-8')
        print(f"[OK] Design summary written to: {output_path}")
        
        return output_path
    
    def run_interactive(self):
        """Run interactive clarification session"""
        print("\n" + "="*60)
        print("Vibe Design - Interactive Requirement Clarification")
        print("="*60)
        print()
        
        # Get initial input
        if not self.session:
            user_input = input("What would you like to build or implement?\n> ").strip()
            if not user_input:
                print("[ERROR] No input provided")
                return
            self.start_session(user_input)
        
        print(f"\n[Session: {self.session.session_id}]")
        print(f"Topic: {self.session.topic}")
        print()
        
        # Question loop
        while True:
            question = self.get_next_question()
            if not question:
                break
                
            print(f"\n[{question.category.upper()}] {question.question}")
            print(f"   Context: {question.context}")
            answer = input("> ").strip()
            
            self.record_answer(question.id, answer)
            
            # Check if user made a decision
            if any(keyword in answer.lower() for keyword in ["use ", "choose ", "select ", "will ", "going to"]):
                # Extract potential decision
                category = self._infer_category(question.category)
                self.add_decision(
                    category=category,
                    title=f"Decision from: {question.question}",
                    decision=answer,
                    reason=f"Answer to: {question.question}",
                    impact="medium"
                )
            
            # Check for continue signal
            if len(self.session.questions_asked) >= 5:
                cont = input("\nContinue clarifying? (y/n): ").strip().lower()
                if cont != 'y':
                    break
        
        # Summary
        print("\n" + "="*60)
        print("Session Complete!")
        print("="*60)
        
        if self.session.decisions:
            print(f"\nDecisions captured: {len(self.session.decisions)}")
            for d in self.session.decisions:
                print(f"  - {d['id']}: {d['title']}")
        
        # Generate summary
        summary_path = self.generate_design_summary()
        print(f"\nDesign summary: {summary_path}")
        
        return self.session
    
    def _infer_category(self, question_category: str) -> str:
        """Infer decision category from question"""
        mapping = {
            "functional": "architecture",
            "technical": "technical",
            "constraints": "scope",
            "scope": "scope"
        }
        return mapping.get(question_category, "architecture")


def main():
    parser = argparse.ArgumentParser(
        description="Vibe Design - AI-assisted requirement clarification"
    )
    parser.add_argument(
        "--clarify",
        type=str,
        help="Start clarification with initial input"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--topic",
        type=str,
        help="Topic name for the design"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output path for design summary"
    )
    parser.add_argument(
        "--record-decision",
        type=str,
        help="Record a decision directly (JSON string)"
    )
    
    args = parser.parse_args()
    
    vibe = VibeDesign()
    
    if args.clarify:
        # Start with initial input
        session = vibe.start_session(args.clarify, args.topic)
        print(f"[OK] Session started: {session.session_id}")
        print(f"[INFO] Topic: {session.topic}")
        
        # Get first question
        q = vibe.get_next_question()
        if q:
            print(f"\n[Q1] {q.question}")
            print(f"    ({q.category})")
            
    elif args.interactive:
        # Full interactive mode
        vibe.run_interactive()
        
    elif args.record_decision:
        # Record a decision directly
        try:
            decision_data = json.loads(args.record_decision)
            decision = vibe.add_decision(**decision_data)
            vibe.write_decision_to_yaml(decision)
            print(f"[OK] Decision recorded: {decision.id}")
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON: {e}")
            sys.exit(1)
            
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
