#!/usr/bin/env python3
"""
Vibe Guard Trigger - Automatic trigger system
=============================================

Provides automatic trigger detection for vibe-guard:
1. Phrase detection - monitors for completion phrases
2. State monitoring - watches SDD state transitions
3. Periodic checks - optional scheduled validation
4. Webhook receiver - external trigger support

Usage:
    python trigger-manager.py --watch
    python trigger-manager.py --daemon
    python trigger-manager.py --webhook-server
"""

import argparse
import json
import os
import re
import sys
import time
import uuid
import threading
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable

# === Configuration ===
SKILLS_BASE = Path(__file__).parent.parent
VIBE_GUARD = SKILLS_BASE / "vibe-guard"
CONFIG_FILE = VIBE_GUARD / "vibe-guard.config.json"
STATE_FILE = Path(".sdd-spec/state.json")
LAST_CHECK_FILE = Path(".sdd-spec/.last-vibe-guard-check")


@dataclass
class TriggerEvent:
    """Trigger event"""
    id: str
    type: str  # phrase, state_change, scheduled, webhook
    timestamp: str
    source: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TriggerConfig:
    """Trigger configuration"""
    mode: str = "standard"
    auto_trigger: bool = True
    trigger_phrases: List[str] = field(default_factory=lambda: [
        "done", "ready", "complete", "finished", "完成", "完成了"
    ])
    grace_period_minutes: int = 10
    skip_if_no_changes: bool = True


class TriggerManager:
    """
    Manages automatic triggers for vibe-guard.
    
    Features:
    - Phrase detection in conversation/text
    - SDD state change detection
    - Grace period to avoid redundant checks
    - File change detection
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config = self._load_config(config_path)
        self.last_check_time = self._load_last_check()
        self.grace_period = timedelta(minutes=self.config.grace_period_minutes)
        self.handlers: List[Callable] = []
        
    def _load_config(self, config_path: Optional[Path]) -> TriggerConfig:
        """Load trigger configuration"""
        path = config_path or CONFIG_FILE
        
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                return TriggerConfig(
                    mode=data.get('mode', 'standard'),
                    auto_trigger=data.get('auto_trigger', True),
                    trigger_phrases=data.get('trigger_phrases', []),
                    grace_period_minutes=data.get('grace_period_minutes', 10),
                    skip_if_no_changes=data.get('skip_if_no_changes', True)
                )
            except Exception as e:
                print(f"[WARN] Could not load config: {e}")
        
        return TriggerConfig()
    
    def _load_last_check(self) -> Optional[datetime]:
        """Load last check timestamp"""
        if LAST_CHECK_FILE.exists():
            try:
                ts = LAST_CHECK_FILE.read_text().strip()
                return datetime.fromisoformat(ts)
            except Exception:
                pass
        return None
    
    def _save_last_check(self):
        """Save last check timestamp"""
        LAST_CHECK_FILE.parent.mkdir(parents=True, exist_ok=True)
        LAST_CHECK_FILE.write_text(datetime.now().isoformat())
    
    # === Trigger Detection ===
    
    def detect_phrase_trigger(self, text: str) -> Optional[TriggerEvent]:
        """Detect completion phrases in text"""
        if not self.config.auto_trigger:
            return None
            
        text_lower = text.lower()
        
        for phrase in self.config.trigger_phrases:
            if phrase.lower() in text_lower:
                return TriggerEvent(
                    id=f"trigger-{uuid.uuid4().hex[:8]}",
                    type="phrase",
                    timestamp=datetime.now().isoformat(),
                    source="conversation",
                    payload={"phrase": phrase, "text": text[:200]}
                )
        
        return None
    
    def detect_state_change_trigger(self) -> Optional[TriggerEvent]:
        """Detect SDD state changes"""
        if not STATE_FILE.exists():
            return None
        
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            current_state = state_data.get('current_state', '')
            last_skill = state_data.get('last_skill', '')
            
            # Check if state just changed (different from last check)
            # For now, trigger on any state that indicates completion
            completion_states = ['Verify', 'ReleaseReady']
            
            if current_state in completion_states:
                return TriggerEvent(
                    id=f"trigger-{uuid.uuid4().hex[:8]}",
                    type="state_change",
                    timestamp=datetime.now().isoformat(),
                    source="sdd_state",
                    payload={"state": current_state, "last_skill": last_skill}
                )
                
        except Exception as e:
            print(f"[WARN] Could not check state: {e}")
        
        return None
    
    def detect_file_change_trigger(self) -> Optional[TriggerEvent]:
        """Detect if files have changed since last check"""
        if not self.config.skip_if_no_changes:
            return None
            
        if not LAST_CHECK_FILE.exists():
            return None
        
        # Check for recent changes
        try:
            # Get recently modified files (last 5 minutes)
            cutoff = datetime.now() - timedelta(minutes=5)
            
            # Simple check - look at .sdd-spec modification time
            if STATE_FILE.exists():
                mtime = datetime.fromtimestamp(STATE_FILE.stat().st_mtime)
                if mtime > cutoff:
                    return TriggerEvent(
                        id=f"trigger-{uuid.uuid4().hex[:8]}",
                        type="file_change",
                        timestamp=datetime.now().isoformat(),
                        source="file_system",
                        payload={"file": str(STATE_FILE)}
                    )
                    
        except Exception as e:
            print(f"[WARN] Could not check file changes: {e}")
        
        return None
    
    def check_grace_period(self) -> bool:
        """Check if we're within grace period"""
        if not self.last_check_time:
            return False
        
        elapsed = datetime.now() - self.last_check_time
        return elapsed < self.grace_period
    
    # === Trigger Execution ===
    
    def register_handler(self, handler: Callable):
        """Register handler to call when trigger fires"""
        self.handlers.append(handler)
    
    def execute_trigger(self, event: TriggerEvent):
        """Execute vibe-guard when trigger fires"""
        print(f"\n[TRIGGER] {event.type}: {event.payload}")
        
        # Run vibe-guard
        self._run_vibe_guard()
        
        # Notify handlers
        for handler in self.handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"[WARN] Handler error: {e}")
        
        # Update last check time
        self._save_last_check()
        self.last_check_time = datetime.now()
    
    def _run_vibe_guard(self):
        """Run vibe-guard validation"""
        guard_script = VIBE_GUARD / "validate-vibe-guard.py"
        
        if not guard_script.exists():
            print(f"[ERROR] vibe-guard not found: {guard_script}")
            return
        
        print(f"[RUNNING] vibe-guard in {self.config.mode} mode...")
        
        import subprocess
        result = subprocess.run(
            [sys.executable, str(guard_script), "--check", "--mode", self.config.mode],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("[OK] vibe-guard passed")
        else:
            print(f"[WARN] vibe-guard issues found:")
            print(result.stdout[-500:] if result.stdout else result.stderr[-500:])
    
    # === Monitoring ===
    
    def monitor(self, interval: int = 60):
        """Continuous monitoring loop"""
        print(f"\n[MONITOR] Starting trigger monitor (interval: {interval}s)")
        print(f"[MONITOR] Grace period: {self.config.grace_period_minutes} minutes")
        
        while True:
            try:
                # Check state changes
                event = self.detect_state_change_trigger()
                
                if event:
                    # Check grace period
                    if not self.check_grace_period():
                        self.execute_trigger(event)
                    else:
                        print(f"[SKIP] Within grace period")
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                print("\n[MONITOR] Stopped")
                break
            except Exception as e:
                print(f"[ERROR] Monitor error: {e}")
                time.sleep(interval)
    
    def watch_text(self, text: str) -> bool:
        """Check text for triggers and execute if found"""
        event = self.detect_phrase_trigger(text)
        
        if event:
            if not self.check_grace_period():
                self.execute_trigger(event)
                return True
            else:
                print("[SKIP] Within grace period")
        
        return False


# === Webhook Server (Optional) ===

class WebhookServer:
    """Simple webhook receiver for external triggers"""
    
    def __init__(self, port: int = 8765):
        self.port = port
        self.trigger_manager: Optional[TriggerManager] = None
    
    def set_trigger_manager(self, manager: TriggerManager):
        self.trigger_manager = manager
    
    def start(self):
        """Start webhook server"""
        try:
            from http.server import HTTPServer, BaseHTTPRequestHandler
            import urllib.parse
        except ImportError:
            print("[ERROR] Webhook server requires full Python stdlib")
            return
        
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                if self.path == '/trigger':
                    length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(length).decode('utf-8')
                    
                    try:
                        data = json.loads(body)
                        
                        if self.server.trigger_manager:
                            event = TriggerEvent(
                                id=f"webhook-{uuid.uuid4().hex[:8]}",
                                type="webhook",
                                timestamp=datetime.now().isoformat(),
                                source="external",
                                payload=data
                            )
                            self.server.trigger_manager.execute_trigger(event)
                    
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(b'{"status": "ok"}')
                        
                    except Exception as e:
                        self.send_response(400)
                        self.end_headers()
                        self.wfile.write(json.dumps({"error": str(e)}).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                # Suppress logging
                pass
        
        Handler.trigger_manager = self.trigger_manager
        
        server = HTTPServer(('', self.port), Handler)
        print(f"[WEBHOOK] Server started on port {self.port}")
        print(f"[WEBHOOK] Send POST to http://localhost:{self.port}/trigger")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Vibe Guard Trigger Manager")
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch for triggers continuously"
    )
    parser.add_argument(
        "--check-phrase",
        type=str,
        help="Check text for trigger phrases"
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run as daemon with monitoring"
    )
    parser.add_argument(
        "--webhook-server",
        action="store_true",
        help="Start webhook server"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Check interval in seconds (default: 60)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Webhook server port (default: 8765)"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Config file path"
    )
    
    args = parser.parse_args()
    
    config_path = Path(args.config) if args.config else None
    manager = TriggerManager(config_path)
    
    if args.watch:
        # One-time check
        event = manager.detect_state_change_trigger()
        if event:
            manager.execute_trigger(event)
        else:
            print("[OK] No triggers detected")
    
    elif args.check_phrase:
        triggered = manager.watch_text(args.check_phrase)
        if triggered:
            print("[TRIGGERED]")
        else:
            print("[NO TRIGGER]")
    
    elif args.daemon:
        # Continuous monitoring
        manager.monitor(args.interval)
    
    elif args.webhook_server:
        # Webhook server
        server = WebhookServer(args.port)
        server.set_trigger_manager(manager)
        server.start()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
