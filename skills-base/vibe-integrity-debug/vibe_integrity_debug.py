#!/usr/bin/env python3
"""
Vibe Integrity Debug - Systematic debugging helper
===================================================

This skill implements the four-phase debugging process:
1. Root Cause Investigation - Understand what and why the issue occurs
2. Pattern Analysis - Compare against working examples
3. Hypothesis and Testing - Form and test a single hypothesis
4. Implementation - Fix the root cause, not the symptom

Usage:
    python vibe_integrity_debug.py --analyze "login fails"
    python vibe_integrity_debug.py --issue "Error: cannot read property of undefined"
    python vibe_integrity_debug.py --phase investigation
"""

import argparse
import json
import os
import re
import sys
import subprocess
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import difflib

# === Configuration ===
SKILLS_BASE = Path(__file__).parent
VIBE_DIR = Path(".vibe-integrity")


# === Phase Enum ===
class Phase:
    INVESTIGATION = "investigation"
    ANALYSIS = "analysis"
    HYPOTHESIS = "hypothesis"
    IMPLEMENTATION = "implementation"


@dataclass
class InvestigationFinding:
    """Finding from root cause investigation"""
    type: str  # error_message, stack_trace, file_location, recent_change
    content: str
    severity: str  # critical, high, medium, low
    evidence: List[str] = field(default_factory=list)


@dataclass
class PatternMatch:
    """Pattern comparison result"""
    similar_file: str
    similarity: float
    differences: List[str] = field(default_factory=list)


@dataclass
class Hypothesis:
    """Testable hypothesis"""
    id: str
    statement: str
    evidence: List[str]
    test_method: str
    status: str = "untested"  # untested, confirmed, rejected


@dataclass
class DebugSession:
    """Active debugging session"""
    session_id: str
    issue_description: str
    start_time: str
    current_phase: str = Phase.INVESTIGATION
    investigation_findings: List[Dict[str, Any]] = field(default_factory=list)
    pattern_matches: List[Dict[str, Any]] = field(default_factory=list)
    hypothesis: Optional[Hypothesis] = None
    fix_applied: bool = False
    fix_verified: bool = False
    attempts: int = 0


class VibeIntegrityDebug:
    """Main debug skill implementation"""
    
    def __init__(self):
        self.session: Optional[DebugSession] = None
        self.vibe_writer_path = SKILLS_BASE / "vibe-integrity-writer" / "vibe-integrity-writer.py"
    
    # === Phase 1: Root Cause Investigation ===
    
    def investigate(self, issue_description: str) -> DebugSession:
        """Start investigation phase"""
        self.session = DebugSession(
            session_id=f"debug-{uuid.uuid4().hex[:8]}",
            issue_description=issue_description,
            start_time=datetime.now().isoformat()
        )
        
        print("\n" + "="*60)
        print(f"PHASE 1: ROOT CAUSE INVESTIGATION")
        print("="*60)
        print(f"Issue: {issue_description}")
        print()
        
        # Step 1: Check for error messages
        self._investigate_error_patterns()
        
        # Step 2: Check recent changes
        self._investigate_recent_changes()
        
        # Step 3: Check relevant .vibe-integrity/ files
        self._investigate_project_context()
        
        return self.session
    
    def _investigate_error_patterns(self):
        """Look for error patterns in output"""
        findings = []
        
        # Check common error indicators
        error_patterns = [
            (r"Error[:\s]", "error_message", "high"),
            (r"Exception", "error_message", "high"),
            (r"Traceback", "stack_trace", "critical"),
            (r"Cannot read property", "null_reference", "critical"),
            (r"undefined is not a function", "type_error", "high"),
            (r"failed", "failure", "medium"),
            (r"ENOENT|no such file", "file_not_found", "high"),
        ]
        
        print("[1] Looking for error patterns...")
        # In real use, this would parse actual error output
        findings.append({
            "type": "investigation_started",
            "content": f"Investigating: {self.session.issue_description}",
            "severity": "info",
            "timestamp": datetime.now().isoformat()
        })
        
        self.session.investigation_findings.extend(findings)
        return findings
    
    def _investigate_recent_changes(self):
        """Check recent git changes"""
        print("[2] Checking recent changes...")
        
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                findings = {
                    "type": "recent_commits",
                    "content": "Git history available",
                    "severity": "info",
                    "evidence": result.stdout.strip().split('\n')[:5]
                }
                self.session.investigation_findings.append(findings)
                print(f"    Found {len(findings.get('evidence', []))} recent commits")
        except Exception as e:
            print(f"    [WARN] Could not check git: {e}")
    
    def _investigate_project_context(self):
        """Check .vibe-integrity/ for context"""
        print("[3] Checking project context...")
        
        # Check risk zones
        risk_file = VIBE_DIR / "risk-zones.yaml"
        if risk_file.exists():
            import yaml
            try:
                with open(risk_file, 'r', encoding='utf-8') as f:
                    risk_data = yaml.safe_load(f)
                    if risk_data and 'zones' in risk_data:
                        print(f"    Found {len(risk_data['zones'])} risk zones defined")
                        self.session.investigation_findings.append({
                            "type": "risk_zones",
                            "content": "Risk zones found",
                            "severity": "info",
                            "evidence": [str(z.get('title', '')) for z in risk_data['zones'][:5]]
                        })
            except Exception as e:
                print(f"    [WARN] Could not read risk zones: {e}")
        else:
            print("    [.vibe-integrity/ not found - run vibe-design first]")
    
    # === Phase 2: Pattern Analysis ===
    
    def analyze_patterns(self) -> List[PatternMatch]:
        """Enter analysis phase"""
        if not self.session:
            raise ValueError("No active session - run investigate() first")
        
        self.session.current_phase = Phase.ANALYSIS
        
        print("\n" + "="*60)
        print(f"PHASE 2: PATTERN ANALYSIS")
        print("="*60)
        
        matches = []
        
        # Find similar code patterns
        print("[1] Searching for similar patterns...")
        
        # Get relevant files based on issue
        keywords = self._extract_keywords(self.session.issue_description)
        
        # Search in codebase
        for keyword in keywords[:3]:
            matches.extend(self._find_similar_patterns(keyword))
        
        self.session.pattern_matches = [asdict(m) for m in matches]
        
        print(f"    Found {len(matches)} similar patterns")
        
        return matches
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract key terms from issue description"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 
                      'to', 'of', 'in', 'on', 'at', 'for', 'with', 'when',
                      'error', 'issue', 'problem', 'fail', 'broken'}
        
        words = re.findall(r'\w+', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords[:5]
    
    def _find_similar_patterns(self, keyword: str) -> List[PatternMatch]:
        """Find files containing similar patterns"""
        matches = []
        
        # Search for files with keyword
        try:
            result = subprocess.run(
                ["grep", "-r", "-l", keyword, "--include=*.py", "--include=*.js", 
                 "--include=*.ts", ".", "-m", "10"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                files = result.stdout.strip().split('\n')
                for f in files[:3]:
                    if f and not any(x in f for x in ['node_modules', '.git', '__pycache__']):
                        matches.append(PatternMatch(
                            similar_file=f,
                            similarity=0.7,  # Simplified similarity score
                            differences=[f"Contains keyword: {keyword}"]
                        ))
                        
        except Exception as e:
            print(f"    [WARN] Search error: {e}")
        
        return matches
    
    # === Phase 3: Hypothesis & Testing ===
    
    def form_hypothesis(self, statement: str, test_method: str) -> Hypothesis:
        """Form and test a hypothesis"""
        if not self.session:
            raise ValueError("No active session")
        
        self.session.current_phase = Phase.HYPOTHESIS
        self.session.attempts += 1
        
        hypothesis = Hypothesis(
            id=f"hyp-{self.session.attempts:02d}",
            statement=statement,
            evidence=self.session.investigation_findings,
            test_method=test_method
        )
        
        self.session.hypothesis = hypothesis
        
        print("\n" + "="*60)
        print(f"PHASE 3: HYPOTHESIS & TESTING")
        print("="*60)
        print(f"Hypothesis: {statement}")
        print(f"Test method: {test_method}")
        
        return hypothesis
    
    def test_hypothesis(self) -> bool:
        """Run hypothesis test"""
        if not self.session or not self.session.hypothesis:
            raise ValueError("No hypothesis to test")
        
        print("\n[Testing hypothesis...]")
        
        # In real implementation, this would:
        # 1. Make minimal change to test hypothesis
        # 2. Run tests
        # 3. Verify result
        
        # For now, prompt user
        result = input("Did the test confirm the hypothesis? (y/n): ").strip().lower()
        
        confirmed = result == 'y'
        
        if confirmed:
            self.session.hypothesis.status = "confirmed"
            print("[OK] Hypothesis confirmed - proceed to implementation")
        else:
            self.session.hypothesis.status = "rejected"
            print("[INFO] Hypothesis rejected - return to investigation")
        
        return confirmed
    
    # === Phase 4: Implementation ===
    
    def implement_fix(self, fix_description: str) -> bool:
        """Apply the fix"""
        if not self.session:
            raise ValueError("No active session")
        
        self.session.current_phase = Phase.IMPLEMENTATION
        
        print("\n" + "="*60)
        print(f"PHASE 4: IMPLEMENTATION")
        print("="*60)
        print(f"Fix: {fix_description}")
        
        # Record fix attempt
        print("\n[Applying fix...]")
        
        self.session.fix_applied = True
        
        # Verify fix
        verify = input("Verify fix works? (y/n): ").strip().lower()
        self.session.fix_verified = verify == 'y'
        
        if self.session.fix_verified:
            print("[OK] Fix verified!")
        else:
            print("[WARN] Fix not verified - may need further investigation")
        
        return self.session.fix_verified
    
    def record_risk_insight(self, title: str, description: str, impact: str = "medium"):
        """Record discovered risk to .vibe-integrity/"""
        risk_data = {
            "id": f"RISK-{uuid.uuid4().hex[:6].upper()}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "category": "debugging",
            "title": title,
            "description": description,
            "impact": impact,
            "status": "identified",
            "session_id": self.session.session_id if self.session else None
        }
        
        # Write to risk-zones.yaml
        risk_file = VIBE_DIR / "risk-zones.yaml"
        
        if not risk_file.exists():
            risk_file.parent.mkdir(parents=True, exist_ok=True)
            risk_file.write_text("zones: []\n")
        
        # Use writer if available
        if self.vibe_writer_path.exists():
            self._write_risk_via_writer(risk_data)
        else:
            self._write_risk_direct(risk_data, risk_file)
    
    def _write_risk_via_writer(self, risk_data: dict):
        """Use vibe-integrity-writer"""
        import subprocess
        
        try:
            result = subprocess.run([
                sys.executable,
                str(self.vibe_writer_path),
                "--target", "risk-zones.yaml",
                "--operation", "add_record",
                "--data", json.dumps(risk_data)
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"[OK] Risk recorded: {risk_data['id']}")
        except Exception as e:
            print(f"[WARN] Writer error: {e}")
    
    def _write_risk_direct(self, risk_data: dict, risk_file: Path):
        """Direct write fallback"""
        import yaml
        
        try:
            with open(risk_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            
            if 'zones' not in data:
                data['zones'] = []
            
            data['zones'].append(risk_data)
            
            with open(risk_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(data, f, default_flow_style=False)
            
            print(f"[OK] Risk recorded: {risk_data['id']}")
        except Exception as e:
            print(f"[ERROR] Could not record risk: {e}")
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get debugging session summary"""
        if not self.session:
            return {}
        
        return {
            "session_id": self.session.session_id,
            "issue": self.session.issue_description,
            "phase": self.session.current_phase,
            "findings_count": len(self.session.investigation_findings),
            "patterns_found": len(self.session.pattern_matches),
            "hypothesis": asdict(self.session.hypothesis) if self.session.hypothesis else None,
            "fix_applied": self.session.fix_applied,
            "fix_verified": self.session.fix_verified,
            "attempts": self.session.attempts
        }
    
    def run_interactive(self):
        """Run interactive debugging session"""
        print("\n" + "="*60)
        print("Vibe Integrity Debug - Interactive Mode")
        print("="*60)
        
        # Get issue
        issue = input("\nDescribe the issue: ").strip()
        if not issue:
            print("[ERROR] No issue provided")
            return
        
        # Phase 1: Investigation
        self.investigate(issue)
        
        # Show findings
        print("\n[Investigation Findings]")
        for f in self.session.investigation_findings:
            print(f"  - {f['type']}: {f['content']}")
        
        # Phase 2: Analysis
        cont = input("\nContinue to pattern analysis? (y/n): ").strip().lower()
        if cont == 'y':
            self.analyze_patterns()
            
            # Show patterns
            print("\n[Similar Patterns Found]")
            for p in self.session.pattern_matches:
                print(f"  - {p.get('similar_file', 'unknown')}")
        
        # Phase 3: Hypothesis
        cont = input("\nContinue to hypothesis formation? (y/n): ").strip().lower()
        if cont == 'y':
            statement = input("What do you think is the root cause? ").strip()
            test_method = input("How will you test this? ").strip()
            
            self.form_hypothesis(statement, test_method)
            
            test_result = self.test_hypothesis()
            
            if test_result and self.session.hypothesis.status == "confirmed":
                # Phase 4: Implementation
                cont = input("\nProceed to implementation? (y/n): ").strip().lower()
                if cont == 'y':
                    fix = input("Describe the fix: ").strip()
                    self.implement_fix(fix)
                    
                    # Ask about recording risk
                    record_risk = input("\nRecord as risk insight? (y/n): ").strip().lower()
                    if record_risk == 'y':
                        title = input("Risk title: ").strip()
                        desc = input("Description: ").strip()
                        self.record_risk_insight(title, desc)
        
        # Summary
        print("\n" + "="*60)
        print("DEBUGGING SESSION SUMMARY")
        print("="*60)
        
        summary = self.get_session_summary()
        print(json.dumps(summary, indent=2))
        
        return summary


def main():
    parser = argparse.ArgumentParser(
        description="Vibe Integrity Debug - Systematic debugging helper"
    )
    parser.add_argument(
        "--analyze",
        type=str,
        help="Start analysis with issue description"
    )
    parser.add_argument(
        "--issue",
        type=str,
        help="Issue description (alias for --analyze)"
    )
    parser.add_argument(
        "--phase",
        type=str,
        choices=["investigation", "analysis", "hypothesis", "implementation"],
        help="Start from specific phase"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--record-risk",
        type=str,
        help="Record a risk insight (JSON string)"
    )
    
    args = parser.parse_args()
    
    debugger = VibeIntegrityDebug()
    
    if args.analyze or args.issue:
        issue = args.analyze or args.issue
        debugger.investigate(issue)
        
        # Auto-continue to analysis
        debugger.analyze_patterns()
        
    elif args.interactive:
        debugger.run_interactive()
        
    elif args.record_risk:
        try:
            risk_data = json.loads(args.record_risk)
            debugger.record_risk_insight(
                risk_data.get('title', ''),
                risk_data.get('description', ''),
                risk_data.get('impact', 'medium')
            )
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON: {e}")
            sys.exit(1)
            
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
