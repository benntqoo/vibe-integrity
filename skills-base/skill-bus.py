#!/usr/bin/env python3
"""
Skill Bus - Cross-skill communication protocol
===============================================

This module provides:
1. Standardized skill calling interface
2. Event-driven communication between skills
3. Skill discovery and registration
4. Request/Response contract validation

Usage:
    from skill_bus import SkillBus, SkillCall, SkillResponse
    
    bus = SkillBus()
    result = await bus.call_skill("vibe-integrity-writer", {
        "operation": "add_record",
        "target_file": "tech-records.yaml",
        "data": {...}
    })
"""

import json
import os
import subprocess
import sys
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

# === Configuration ===
SKILLS_BASE = Path(__file__).parent
PROTOCOL_VERSION = "1.0.0"


class CallStatus(Enum):
    """Status of skill call"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"


@dataclass
class SkillCall:
    """Incoming skill call request"""
    protocol_version: str = PROTOCOL_VERSION
    call_id: str = field(default_factory=lambda: f"call-{uuid.uuid4().hex[:8]}")
    caller: str = ""
    callee: str = ""
    operation: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    callback: Optional[Dict[str, str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillResponse:
    """Outgoing skill response"""
    protocol_version: str = PROTOCOL_VERSION
    call_id: str = ""
    status: str = CallStatus.PENDING.value
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    output_files: List[str] = field(default_factory=list)
    duration_ms: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class SkillBus:
    """
    Central bus for cross-skill communication.
    
    Provides:
    - Skill discovery via registry
    - Standardized call interface
    - Event subscription
    - Request/Response validation
    """
    
    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or (SKILLS_BASE / "skill-registry.json")
        self.registry = self._load_registry()
        self.handlers: Dict[str, Callable] = {}
        self.event_subscribers: Dict[str, List[Callable]] = {}
        self.call_history: List[Dict[str, Any]] = []
        
    def _load_registry(self) -> Dict[str, Any]:
        """Load skill registry"""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARN] Could not load registry: {e}")
        
        return {"skills": [], "workflows": {}}
    
    def _get_skill_info(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """Get skill info from registry"""
        for skill in self.registry.get("skills", []):
            if skill.get("id") == skill_id or skill.get("name") == skill_id:
                return skill
        return None
    
    # === Skill Discovery ===
    
    def list_skills(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List available skills"""
        skills = self.registry.get("skills", [])
        
        if category:
            skills = [s for s in skills if s.get("category") == category]
        
        return skills
    
    def get_skill(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """Get skill by ID"""
        return self._get_skill_info(skill_id)
    
    # === Skill Calling ===
    
    def call_skill(
        self,
        callee: str,
        operation: str,
        payload: Dict[str, Any],
        caller: str = "unknown",
        timeout: int = 60
    ) -> SkillResponse:
        """
        Call a skill with given operation and payload.
        
        This is the main entry point for cross-skill communication.
        """
        call_id = f"call-{uuid.uuid4().hex[:8]}"
        start_time = datetime.now()
        
        # Build call request
        call = SkillCall(
            call_id=call_id,
            caller=caller,
            callee=callee,
            operation=operation,
            payload=payload
        )
        
        # Get skill info
        skill_info = self._get_skill_info(callee)
        
        if not skill_info:
            return SkillResponse(
                call_id=call_id,
                status=CallStatus.FAILURE.value,
                error=f"Skill not found: {callee}"
            )
        
        # Get implementation path
        implementation = skill_info.get("implementation", "")
        
        if not implementation:
            return SkillResponse(
                call_id=call_id,
                status=CallStatus.FAILURE.value,
                error=f"No implementation for skill: {callee}"
            )
        
        # Execute skill
        response = self._execute_skill(call, skill_info, implementation, timeout)
        
        # Record history
        self.call_history.append({
            "call_id": call_id,
            "caller": caller,
            "callee": callee,
            "operation": operation,
            "status": response.status,
            "duration_ms": response.duration_ms,
            "timestamp": call.timestamp
        })
        
        return response
    
    def _execute_skill(
        self,
        call: SkillCall,
        skill_info: Dict[str, Any],
        implementation: str,
        timeout: int
    ) -> SkillResponse:
        """Execute a skill"""
        
        # Build command
        impl_path = Path(implementation)
        
        if not impl_path.exists():
            # Try relative to skills-base
            impl_path = SKILLS_BASE / implementation
            if not impl_path.exists():
                return SkillResponse(
                    call_id=call.call_id,
                    status=CallStatus.FAILURE.value,
                    error=f"Implementation not found: {implementation}"
                )
        
        # Build args based on skill type
        cmd = self._build_command(call, skill_info, impl_path)
        
        try:
            # Execute
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.getcwd()
            )
            
            duration_ms = int((datetime.now() - datetime.fromisoformat(call.timestamp)).total_seconds() * 1000)
            
            if result.returncode == 0:
                # Try to parse output
                output = result.stdout
                parsed_result = None
                
                try:
                    parsed_result = json.loads(output)
                except json.JSONDecodeError:
                    parsed_result = {"output": output.strip()}
                
                return SkillResponse(
                    call_id=call.call_id,
                    status=CallStatus.SUCCESS.value,
                    result=parsed_result,
                    output_files=self._extract_output_files(parsed_result),
                    duration_ms=duration_ms
                )
            else:
                return SkillResponse(
                    call_id=call.call_id,
                    status=CallStatus.FAILURE.value,
                    error=result.stderr or result.stdout,
                    duration_ms=duration_ms
                )
                
        except subprocess.TimeoutExpired:
            return SkillResponse(
                call_id=call.call_id,
                status=CallStatus.TIMEOUT.value,
                error=f"Skill execution timeout after {timeout}s"
            )
        except Exception as e:
            return SkillResponse(
                call_id=call.call_id,
                status=CallStatus.FAILURE.value,
                error=str(e)
            )
    
    def _build_command(
        self,
        call: SkillCall,
        skill_info: Dict[str, Any],
        impl_path: Path
    ) -> List[str]:
        """Build command for skill execution"""
        
        # Determine command based on file type
        ext = impl_path.suffix.lower()
        
        if ext == ".py":
            cmd = [sys.executable, str(impl_path)]
        elif ext == ".js":
            cmd = ["node", str(impl_path)]
        elif ext == ".sh":
            cmd = ["bash", str(impl_path)]
        else:
            cmd = [str(impl_path)]
        
        # Add operation-specific args
        if call.operation:
            if impl_path.stem == "vibe-integrity-writer":
                cmd.extend(["--target", call.payload.get("target_file", "")])
                cmd.extend(["--operation", call.operation])
                if call.payload.get("data"):
                    cmd.extend(["--data", json.dumps(call.payload.get("data"))])
            elif impl_path.stem == "vibe-design":
                cmd.extend(["--clarify", call.payload.get("input", "")])
            elif impl_path.stem == "vibe_integrity_debug":
                cmd.extend(["--analyze", call.payload.get("issue", "")])
            elif impl_path.stem == "validate-vibe-guard":
                cmd.append("--check")
        
        return cmd
    
    def _extract_output_files(self, result: Any) -> List[str]:
        """Extract file paths from result"""
        files = []
        
        if isinstance(result, dict):
            for key in ["output_file", "output_files", "report_file", "files"]:
                if key in result:
                    value = result[key]
                    if isinstance(value, list):
                        files.extend(value)
                    elif isinstance(value, str):
                        files.append(value)
        
        return files
    
    # === Event System ===
    
    def subscribe(self, event: str, handler: Callable):
        """Subscribe to skill events"""
        if event not in self.event_subscribers:
            self.event_subscribers[event] = []
        self.event_subscribers[event].append(handler)
    
    def publish(self, event: str, data: Dict[str, Any]):
        """Publish event to subscribers"""
        if event in self.event_subscribers:
            for handler in self.event_subscribers[event]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"[WARN] Event handler error: {e}")
    
    # === Handler Registration ===
    
    def register_handler(self, skill_id: str, handler: Callable):
        """Register a local handler for a skill"""
        self.handlers[skill_id] = handler
    
    def call_handler(self, skill_id: str, payload: Dict[str, Any]) -> SkillResponse:
        """Call a locally registered handler"""
        
        if skill_id not in self.handlers:
            return SkillResponse(
                status=CallStatus.FAILURE.value,
                error=f"No handler registered for: {skill_id}"
            )
        
        try:
            result = self.handlers[skill_id](payload)
            return SkillResponse(
                status=CallStatus.SUCCESS.value,
                result=result if isinstance(result, dict) else {"result": result}
            )
        except Exception as e:
            return SkillResponse(
                status=CallStatus.FAILURE.value,
                error=str(e)
            )
    
    # === History ===
    
    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get call history"""
        return self.call_history[-limit:]
    
    def clear_history(self):
        """Clear call history"""
        self.call_history = []


# === Convenience Functions ===

def create_call(
    callee: str,
    operation: str,
    payload: Dict[str, Any],
    caller: str = "system"
) -> SkillCall:
    """Create a skill call request"""
    return SkillCall(
        caller=caller,
        callee=callee,
        operation=operation,
        payload=payload
    )


def format_response(response: SkillResponse) -> str:
    """Format response for display"""
    lines = [
        f"Call ID: {response.call_id}",
        f"Status: {response.status}",
        f"Duration: {response.duration_ms}ms"
    ]
    
    if response.result:
        lines.append(f"Result: {json.dumps(response.result, indent=2)}")
    
    if response.error:
        lines.append(f"Error: {response.error}")
    
    if response.output_files:
        lines.append(f"Output Files: {', '.join(response.output_files)}")
    
    return "\n".join(lines)


# === CLI ===

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Skill Bus CLI")
    parser.add_argument("--call", type=str, help="Skill to call")
    parser.add_argument("--operation", type=str, help="Operation to perform")
    parser.add_argument("--payload", type=str, help="JSON payload")
    parser.add_argument("--list", action="store_true", help="List available skills")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--history", action="store_true", help="Show call history")
    
    args = parser.parse_args()
    
    bus = SkillBus()
    
    if args.list:
        skills = bus.list_skills(args.category)
        print(f"Available skills ({len(skills)}):")
        for s in skills:
            print(f"  - {s.get('name')} ({s.get('category')})")
            print(f"    {s.get('description', '')}")
            
    elif args.history:
        for h in bus.get_history():
            print(f"{h['timestamp']}: {h['caller']} -> {h['callee']} ({h['status']})")
            
    elif args.call:
        payload = {}
        if args.payload:
            try:
                payload = json.loads(args.payload)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Invalid JSON: {e}")
                return
        
        response = bus.call_skill(args.call, args.operation or "", payload)
        print(format_response(response))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
