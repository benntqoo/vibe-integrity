#!/usr/bin/env python3
"""
Fold Events to State
=====================

Read events.yaml and fold it into the consolidated state.yaml file.
This is the "source of truth" for the project state.

Usage:
    python fold-events.py [--root /path/to/project] [--since EVT-xxx]
"""

import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


VIBE_DIR = Path('.vibe-integrity')
EVENTS_FILE = VIBE_DIR / 'events.yaml'
STATE_FILE = VIBE_DIR / 'state.yaml'


def load_yaml(filepath: Path) -> Dict:
    """Load YAML file with error handling"""
    if not filepath.exists():
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}")
        return {}


def save_yaml(filepath: Path, data: Dict):
    """Save YAML file with proper formatting"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


class EventFolder:
    """Fold events into a consolidated state"""
    
    def __init__(self, root_path: Optional[Path] = None):
        self.root_path = Path(root_path) if root_path else Path.cwd()
        self.vibe_dir = self.root_path / '.vibe-integrity'
        self.events_file = self.vibe_dir / 'events.yaml'
        self.state_file = self.vibe_dir / 'state.yaml'
        self.state: Dict = {}
    
    def load_events(self) -> List[Dict]:
        """Load all events from events.yaml"""
        events_data = load_yaml(self.events_file)
        return events_data.get('events', [])
    
    def apply_event(self, event: Dict):
        """Apply a single event to state"""
        event_type = event.get('type', '')
        event_data = event.get('data', {})
        
        if event_type == 'decision_made':
            record_id = event_data.get('id')
            if record_id:
                if 'decisions' not in self.state:
                    self.state['decisions'] = {}
                self.state['decisions'][record_id] = {
                    'category': event_data.get('category', ''),
                    'title': event_data.get('title', ''),
                    'decision': event_data.get('decision', {}),
                    'reason': event_data.get('reason', ''),
                    'impact': event_data.get('impact', 'medium'),
                    'status': 'active',
                    'since': event.get('timestamp', ''),
                    'created_by': event.get('agent_id', '')
                }
        
        elif event_type == 'decision_changed':
            record_id = event_data.get('id')
            if record_id and record_id in self.state.get('decisions', {}):
                # Keep history
                if 'history' not in self.state['decisions'][record_id]:
                    self.state['decisions'][record_id]['history'] = []
                self.state['decisions'][record_id]['history'].append({
                    'old_value': event_data.get('old_value'),
                    'new_value': event_data.get('new_value'),
                    'reason': event_data.get('reason'),
                    'at': event.get('timestamp', '')
                })
                # Update current value
                if 'decision' in event_data.get('new_value', {}):
                    self.state['decisions'][record_id]['decision'] = event_data['new_value']['decision']
        
        elif event_type == 'risk_identified':
            risk_id = event_data.get('id')
            if risk_id:
                if 'risks' not in self.state:
                    self.state['risks'] = {}
                self.state['risks'][risk_id] = {
                    'category': event_data.get('category', ''),
                    'area': event_data.get('area', ''),
                    'description': event_data.get('description', ''),
                    'impact': event_data.get('impact', 'medium'),
                    'status': 'identified',
                    'since': event.get('timestamp', '')
                }
        
        elif event_type == 'risk_mitigated':
            risk_id = event_data.get('id')
            if risk_id and risk_id in self.state.get('risks', {}):
                self.state['risks'][risk_id]['status'] = 'mitigated'
                self.state['risks'][risk_id]['mitigated_at'] = event.get('timestamp', '')
                self.state['risks'][risk_id]['mitigation'] = event_data.get('mitigation', '')
        
        elif event_type == 'dependency_added':
            dep_name = event_data.get('name')
            if dep_name:
                if 'dependencies' not in self.state:
                    self.state['dependencies'] = {}
                self.state['dependencies'][dep_name] = {
                    'version': event_data.get('version', ''),
                    'reason': event_data.get('reason', ''),
                    'added_at': event.get('timestamp', '')
                }
        
        elif event_type == 'dependency_removed':
            dep_name = event_data.get('name')
            if dep_name and dep_name in self.state.get('dependencies', {}):
                del self.state['dependencies'][dep_name]
        
        elif event_type == 'schema_changed':
            self.state['schema_version'] = event_data.get('new_version', self.state.get('schema_version', '0'))
    
    def fold(self, since_event_id: Optional[str] = None) -> Dict:
        """Fold all events into state"""
        events = self.load_events()
        
        if not events:
            return {}
        
        # Sort by timestamp
        events.sort(key=lambda e: e.get('timestamp', ''))
        
        # Find starting point
        start_index = 0
        if since_event_id:
            for i, event in enumerate(events):
                if event.get('id') == since_event_id:
                    start_index = i
                    break
        
        # Apply events
        for event in events[start_index:]:
            self.apply_event(event)
        
        # Update metadata
        self.state['last_folded'] = datetime.now().isoformat()
        self.state['folded_by'] = 'fold-events.py'
        
        return self.state
    
    def save_state(self):
        """Save folded state to file"""
        header = """# Current State Summary
# =====================
# This file is auto-generated from events.yaml folding.
# DO NOT EDIT MANUALLY - use vibe-integrity-writer.py
#
# To regenerate: python skills-base/vibe-integrity/fold-events.py
#
"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            f.write(header)
            yaml.dump(self.state, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"✅ State folded and saved to {self.state_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Fold events to state')
    parser.add_argument('--root', help='Root path of project')
    parser.add_argument('--since', help='Start from specific event ID')
    parser.add_argument('--dry-run', action='store_true', help='Show result without saving')
    
    args = parser.parse_args()
    
    vibe_dir = Path(args.root) / '.vibe-integrity' if args.root else Path('.vibe-integrity')
    
    folder = EventFolder(vibe_dir)  # Pass Path object directly
    state = folder.fold(args.since)
    
    if args.dry_run:
        print(yaml.dump(state, default_flow_style=False, allow_unicode=True, sort_keys=False))
    else:
        folder.save_state()
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Decisions: {len(state.get('decisions', {}))}")
    print(f"  Risks: {len(state.get('risks', {}))}")
    print(f"  Dependencies: {len(state.get('dependencies', {}))}")


if __name__ == '__main__':
    main()
