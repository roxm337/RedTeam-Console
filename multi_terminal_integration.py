#!/usr/bin/env python3
"""
AI Pentester Agent - Multi-Terminal Integration
Easy-to-use interface for parallel pentesting operations
"""

from command_executor_v2 import execute_command, get_parallel_results_summary
from config import print_colored, Colors
import time

class MultiTerminalPentester:
    """High-level interface for multi-terminal pentesting operations"""
    
    def __init__(self):
        self.current_target = None
        
    def set_target(self, target: str):
        """Set the current target for pentesting"""
        self.current_target = target
        print_colored(f"🎯 Target set: {target}", Colors.CYAN, bold=True)
    
    def parallel_reconnaissance(self, target: str = None):
        """Run parallel reconnaissance against target"""
        target = target or self.current_target
        if not target:
            print_colored("❌ No target specified", Colors.RED)
            return
        
        print_colored("🔍 Running parallel reconnaissance...", Colors.CYAN, bold=True)
        
        commands = f"parallel_execute:nmap -sS -T4 -p 80,443,22,21,25 {target};dig {target} ANY;whois {target};ping -c 3 {target}"
        
        result, code, error = execute_command(
            command=commands,
            phase="reconnaissance",
            tool_category="network_scanning",
            expected_outcome="Target discovery and enumeration"
        )
        
        return result
    
    def parallel_web_testing(self, target: str = None):
        """Run parallel web application testing"""
        target = target or self.current_target
        if not target:
            print_colored("❌ No target specified", Colors.RED)
            return
            
        print_colored("🌐 Running parallel web testing...", Colors.CYAN, bold=True)
        
        commands = f"parallel_execute:curl -I http://{target};curl -s http://{target}/robots.txt;whatweb http://{target};curl -s http://{target}/.well-known/security.txt"
        
        result, code, error = execute_command(
            command=commands,
            phase="web_testing",
            tool_category="web_application",
            expected_outcome="Web application analysis"
        )
        
        return result
    
    def parallel_custom_functions(self):
        """Run parallel custom pentesting functions"""
        print_colored("🔧 Running parallel custom functions...", Colors.CYAN, bold=True)
        
        commands = "parallel_execute:custom_function:port_scan_tcp;custom_function:web_tech_detection;custom_function:dns_enumeration"
        
        result, code, error = execute_command(
            command=commands,
            phase="custom_analysis",
            tool_category="custom_functions",
            expected_outcome="Specialized security analysis"
        )
        
        return result
    
    def comprehensive_scan(self, target: str = None):
        """Run comprehensive multi-phase parallel pentesting"""
        target = target or self.current_target
        if not target:
            print_colored("❌ No target specified", Colors.RED)
            return
        
        print_colored(f"🚀 Starting comprehensive scan of {target}", Colors.GREEN, bold=True)
        print_colored("=" * 60, Colors.GREEN)
        
        # Phase 1: Reconnaissance
        print_colored("\n📋 Phase 1: Reconnaissance", Colors.BLUE, bold=True)
        recon_result = self.parallel_reconnaissance(target)
        time.sleep(1)
        
        # Phase 2: Web Testing
        print_colored("\n📋 Phase 2: Web Application Testing", Colors.BLUE, bold=True)
        web_result = self.parallel_web_testing(target)
        time.sleep(1)
        
        # Phase 3: Custom Functions
        print_colored("\n📋 Phase 3: Custom Security Functions", Colors.BLUE, bold=True)
        custom_result = self.parallel_custom_functions()
        
        print_colored("\n🏁 Comprehensive scan completed!", Colors.GREEN, bold=True)
        
        # Show results summary
        print_colored("\n📊 RESULTS SUMMARY:", Colors.CYAN, bold=True)
        summary = get_parallel_results_summary()
        print(summary)
        
        return {
            'reconnaissance': recon_result,
            'web_testing': web_result, 
            'custom_functions': custom_result
        }

def quick_demo():
    """Quick demonstration of capabilities"""
    pentester = MultiTerminalPentester()
    
    print_colored("🤖 AI PENTESTER AGENT - QUICK DEMO", Colors.CYAN, bold=True)
    print_colored("=" * 50, Colors.CYAN)
    print()
    
    # Demo against safe target
    target = "testphp.vulnweb.com"
    pentester.set_target(target)
    
    print_colored("🚀 Running quick parallel demo...", Colors.YELLOW)
    print()
    
    # Quick parallel test
    commands = "parallel_execute:echo 'Pentesting started';date;echo 'Tools initialized';dig google.com +short"
    
    result, code, error = execute_command(
        command=commands,
        phase="demo",
        tool_category="demonstration",
        expected_outcome="Show parallel execution"
    )
    
    print_colored("\n✅ Quick demo completed!", Colors.GREEN, bold=True)
    print_colored("🎯 Ready for comprehensive pentesting!", Colors.CYAN)

if __name__ == "__main__":
    # Run quick demo
    quick_demo()
    
    print("\n" + "="*60)
    choice = input("🤔 Run comprehensive scan on testphp.vulnweb.com? (y/N): ").strip().lower()
    
    if choice in ['y', 'yes']:
        pentester = MultiTerminalPentester()
        pentester.comprehensive_scan("testphp.vulnweb.com")
    
    print()
    print_colored("✨ Multi-terminal pentesting system ready for use!", Colors.GREEN, bold=True)
    print_colored("📖 Usage:", Colors.CYAN)
    print_colored("   from multi_terminal_integration import MultiTerminalPentester", Colors.WHITE)
    print_colored("   pentester = MultiTerminalPentester()", Colors.WHITE)
    print_colored("   pentester.comprehensive_scan('your-target.com')", Colors.WHITE)
