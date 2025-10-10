#!/usr/bin/env python3
"""
🜏 Luxor Observer Poll Monitor
Polls the dashboard endpoints and displays changes in real-time
"""

import argparse
import json
import sys
import time
from datetime import datetime
from typing import Dict, Optional, Any

# Try to import requests or urllib
try:
    import requests
    USE_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    USE_REQUESTS = False


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class LuxorPollMonitor:
    """Monitor Luxor Observer endpoints and display changes"""
    
    def __init__(self, base_url: str, interval: int = 2):
        self.base_url = base_url.rstrip('/')
        self.interval = interval
        self.last_state: Optional[Dict] = None
        self.last_health: Optional[Dict] = None
        self.last_metrics: Optional[Dict] = None
        self.error_count = 0
        
    def fetch_json(self, endpoint: str) -> Optional[Dict]:
        """Fetch JSON from an endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if USE_REQUESTS:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                return response.json()
            else:
                with urllib.request.urlopen(url, timeout=5) as response:
                    data = response.read().decode('utf-8')
                    return json.loads(data)
                    
        except Exception as e:
            self.error_count += 1
            if self.error_count % 10 == 1:  # Only show every 10th error
                print(f"{Colors.RED}❌ Error fetching {endpoint}: {e}{Colors.ENDC}")
            return None
    
    def format_timestamp(self) -> str:
        """Get formatted current timestamp"""
        return datetime.now().strftime("%H:%M:%S")
    
    def print_header(self):
        """Print monitor header"""
        print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.BOLD}🜏 LUXOR OBSERVER POLL MONITOR{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Monitoring: {self.base_url}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Interval: {self.interval}s{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}\n")
    
    def detect_changes(self, old: Optional[Dict], new: Optional[Dict], key_path: str = "") -> list:
        """Recursively detect changes between two dictionaries"""
        if old is None or new is None:
            return []
        
        changes = []
        
        # Check all keys in new dict
        for key, new_value in new.items():
            full_key = f"{key_path}.{key}" if key_path else key
            
            if key not in old:
                changes.append(f"  {Colors.GREEN}+ {full_key}: {new_value}{Colors.ENDC}")
            elif old[key] != new_value:
                # For nested dicts, recurse
                if isinstance(new_value, dict) and isinstance(old[key], dict):
                    changes.extend(self.detect_changes(old[key], new_value, full_key))
                else:
                    changes.append(
                        f"  {Colors.YELLOW}~ {full_key}: {old[key]} → {new_value}{Colors.ENDC}"
                    )
        
        # Check for removed keys
        for key in old:
            if key not in new:
                full_key = f"{key_path}.{key}" if key_path else key
                changes.append(f"  {Colors.RED}- {full_key}: {old[key]}{Colors.ENDC}")
        
        return changes
    
    def display_state_update(self, state: Dict):
        """Display current state information"""
        timestamp = self.format_timestamp()
        
        # Extract key information
        consciousness = state.get('consciousness_level', 'unknown')
        workflow = state.get('workflow_context', 'unknown')
        kb_activity = state.get('keyboard_activity', 0)
        mouse_activity = state.get('mouse_activity', 0)
        
        print(f"\n{Colors.BOLD}[{timestamp}] Current State:{Colors.ENDC}")
        print(f"  {Colors.CYAN}🧠 Consciousness: {consciousness}{Colors.ENDC}")
        print(f"  {Colors.BLUE}⚙️  Workflow: {workflow}{Colors.ENDC}")
        print(f"  {Colors.GREEN}⌨️  Keyboard: {kb_activity:.2f}/s{Colors.ENDC}")
        print(f"  {Colors.GREEN}🖱️  Mouse: {mouse_activity:.2f}/s{Colors.ENDC}")
        
        # Show active apps if available
        if 'active_apps' in state and state['active_apps']:
            apps = state['active_apps']
            if isinstance(apps, dict) and 'active' in apps:
                print(f"  {Colors.YELLOW}📱 Active App: {apps['active']}{Colors.ENDC}")
            elif isinstance(apps, list) and apps:
                print(f"  {Colors.YELLOW}📱 Active Apps: {', '.join(apps[:3])}{Colors.ENDC}")
        
        # Detect and show changes
        if self.last_state:
            changes = self.detect_changes(self.last_state, state)
            if changes:
                print(f"\n  {Colors.BOLD}Changes detected:{Colors.ENDC}")
                for change in changes[:10]:  # Limit to first 10 changes
                    print(change)
    
    def display_health_update(self, health: Dict):
        """Display health check information"""
        timestamp = self.format_timestamp()
        status = health.get('status', 'unknown')
        
        status_color = Colors.GREEN if status == 'healthy' else Colors.YELLOW
        if status in ['unhealthy', 'error']:
            status_color = Colors.RED
        
        print(f"\n{Colors.BOLD}[{timestamp}] Health Check:{Colors.ENDC}")
        print(f"  {status_color}Status: {status}{Colors.ENDC}")
        
        if 'data_file_exists' in health:
            file_status = "✅" if health['data_file_exists'] else "❌"
            print(f"  {file_status} Data file: {health['data_file_exists']}")
        
        if 'cache_active' in health:
            cache_status = "✅" if health['cache_active'] else "⚠️"
            print(f"  {cache_status} Cache: {health['cache_active']}")
    
    def display_metrics_update(self, metrics: Dict):
        """Display system metrics"""
        timestamp = self.format_timestamp()
        
        cpu = metrics.get('cpu_usage', 0)
        memory = metrics.get('memory_usage', 0)
        
        print(f"\n{Colors.BOLD}[{timestamp}] System Metrics:{Colors.ENDC}")
        print(f"  {Colors.CYAN}💻 CPU: {cpu:.1f}%{Colors.ENDC}")
        print(f"  {Colors.CYAN}🧠 Memory: {memory:.1f}%{Colors.ENDC}")
        
        if 'process_memory' in metrics:
            print(f"  {Colors.BLUE}🔧 Process: {metrics['process_memory']:.2f} MB{Colors.ENDC}")
    
    def run(self):
        """Main monitoring loop"""
        self.print_header()
        
        print(f"{Colors.GREEN}🚀 Monitoring started. Press Ctrl+C to stop.{Colors.ENDC}\n")
        
        try:
            while True:
                # Reset error count periodically
                if self.error_count > 100:
                    self.error_count = 0
                
                # Fetch current state
                state = self.fetch_json('/api/current_state')
                if state and state.get('status') != 'no_data':
                    if not self.last_state or state != self.last_state:
                        self.display_state_update(state)
                        self.last_state = state
                
                # Fetch health (less frequently - every 4 polls)
                if int(time.time() / self.interval) % 4 == 0:
                    health = self.fetch_json('/health')
                    if health and health != self.last_health:
                        self.display_health_update(health)
                        self.last_health = health
                
                # Fetch metrics (less frequently - every 6 polls)
                if int(time.time() / self.interval) % 6 == 0:
                    metrics = self.fetch_json('/api/system_metrics')
                    if metrics and metrics != self.last_metrics:
                        self.display_metrics_update(metrics)
                        self.last_metrics = metrics
                
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}🛑 Monitoring stopped by user{Colors.ENDC}")
            print(f"{Colors.GREEN}✅ Goodbye!{Colors.ENDC}\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.ENDC}\n")
            sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='🜏 Luxor Observer Poll Monitor - Monitor dashboard endpoints',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --url http://localhost:8888
  %(prog)s --url http://localhost:8888 --interval 5
        """
    )
    
    parser.add_argument(
        '--url',
        default='http://localhost:8888',
        help='Base URL of Luxor Observer dashboard (default: http://localhost:8888)'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        default=2,
        help='Polling interval in seconds (default: 2)'
    )
    
    args = parser.parse_args()
    
    # Validate interval
    if args.interval < 1:
        print(f"{Colors.RED}Error: Interval must be at least 1 second{Colors.ENDC}")
        sys.exit(1)
    
    # Create and run monitor
    monitor = LuxorPollMonitor(args.url, args.interval)
    monitor.run()


if __name__ == '__main__':
    main()
