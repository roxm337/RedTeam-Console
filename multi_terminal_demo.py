#!/usr/bin/env python3
"""
AI Pentester Agent - Multi-Terminal Demo
Complete demonstration of parallel pentesting capabilities
"""

import time
import json
from command_executor_v2 import execute_command, get_parallel_results_summary
from config import print_colored, Colors

def main_demo():
    """Main demonstration of multi-terminal parallel execution"""
    
    print_colored("🤖 AI PENTESTER AGENT - MULTI-TERMINAL DEMO", Colors.CYAN, bold=True)
    print_colored("=" * 60, Colors.CYAN)
    print()
    print_colored("🎯 This demo shows how to run multiple pentesting commands", Colors.YELLOW)
    print_colored("   simultaneously while the main script continues execution", Colors.YELLOW)
    print_colored("   and automatically collects and analyzes results.", Colors.YELLOW)
    print()
    
    # Demo 1: Basic parallel execution
    print_colored("📋 DEMO 1: Basic Parallel Commands", Colors.CYAN, bold=True)
    print_colored("-" * 40, Colors.CYAN)
    
    basic_commands = "parallel_execute:echo 'Reconnaissance started';date;echo 'Network scan initiated';sleep 1;echo 'Service enumeration';ping -c 2 google.com"
    
    print_colored("Executing basic parallel commands...", Colors.YELLOW)
    result, code, error = execute_command(
        command=basic_commands,
        phase="demo_basic",
        tool_category="basic_commands",
        expected_outcome="Demonstrate parallel execution"
    )
    
    print_colored("✅ Basic demo completed!", Colors.GREEN)
    print()
    
    # Wait a moment
    time.sleep(1)
    
    # Demo 2: Real pentesting scenario
    print_colored("📋 DEMO 2: Real Pentesting Scenario", Colors.CYAN, bold=True)
    print_colored("-" * 40, Colors.CYAN)
    
    target = "testphp.vulnweb.com"
    print_colored(f"🎯 Target: {target}", Colors.YELLOW)
    
    # Reconnaissance phase
    print_colored("\n🔍 Phase 1: Reconnaissance", Colors.BLUE, bold=True)
    recon_commands = f"parallel_execute:nmap -sS -T4 -p 80,443,22,21 {target};dig {target} ANY;whois {target};curl -I http://{target}"
    
    recon_result, recon_code, recon_error = execute_command(
        command=recon_commands,
        phase="reconnaissance",
        tool_category="network_scanning",
        expected_outcome="Gather target information"
    )
    
    time.sleep(2)
    
    # Web testing phase
    print_colored("\n🌐 Phase 2: Web Application Testing", Colors.BLUE, bold=True)
    web_commands = f"parallel_execute:curl -s http://{target}/robots.txt;curl -s http://{target}/.well-known/security.txt;whatweb http://{target};curl -s -H 'User-Agent: Mozilla/5.0' http://{target}"
    
    web_result, web_code, web_error = execute_command(
        command=web_commands,
        phase="web_testing", 
        tool_category="web_application",
        expected_outcome="Analyze web application"
    )
    
    time.sleep(2)
    
    # Custom functions demo
    print_colored("\n🔧 Phase 3: Custom Functions", Colors.BLUE, bold=True)
    custom_commands = "parallel_execute:custom_function:port_scan_tcp;custom_function:web_tech_detection;custom_function:dns_enumeration"
    
    custom_result, custom_code, custom_error = execute_command(
        command=custom_commands,
        phase="custom_analysis",
        tool_category="custom_functions", 
        expected_outcome="Run specialized pentesting functions"
    )
    
    time.sleep(1)
    
    # Demo 3: Single terminal execution
    print_colored("\n📋 DEMO 3: Single Terminal Execution", Colors.CYAN, bold=True)
    print_colored("-" * 40, Colors.CYAN)
    
    print_colored("Running detailed scan in separate terminal...", Colors.YELLOW)
    single_result, single_code, single_error = execute_command(
        command=f"nmap -sV -sC {target}",
        phase="detailed_scan",
        tool_category="comprehensive_scan",
        expected_outcome="Detailed service detection",
        run_in_terminal=True
    )
    
    print_colored("✅ Single terminal demo completed!", Colors.GREEN)
    print()
    
    # Results summary
    print_colored("📊 EXECUTION SUMMARY", Colors.CYAN, bold=True)
    print_colored("=" * 60, Colors.CYAN)
    
    summary = get_parallel_results_summary()
    print(summary)
    
    # Final analysis
    print_colored("\n🎯 KEY CAPABILITIES DEMONSTRATED:", Colors.GREEN, bold=True)
    print_colored("✅ Parallel command execution - multiple tools run simultaneously", Colors.GREEN)
    print_colored("✅ Main script continues - no blocking on long-running commands", Colors.GREEN)
    print_colored("✅ Automatic result collection - outputs saved and analyzed", Colors.GREEN)
    print_colored("✅ Security findings detection - vulnerability patterns identified", Colors.GREEN)
    print_colored("✅ Real pentesting tools - nmap, curl, dig, whois, custom functions", Colors.GREEN)
    print_colored("✅ Phase-based organization - reconnaissance, web testing, etc.", Colors.GREEN)
    print_colored("✅ Terminal management - single and parallel execution modes", Colors.GREEN)
    
    print()
    print_colored("🚀 READY FOR PRODUCTION PENTESTING!", Colors.CYAN, bold=True)
    print_colored("   Use 'parallel_execute:cmd1;cmd2;cmd3' for multiple commands", Colors.YELLOW)
    print_colored("   Use run_in_terminal=True for single dedicated terminal", Colors.YELLOW)
    print_colored("   Results are automatically collected and analyzed", Colors.YELLOW)

def advanced_pentesting_scenario():
    """Advanced scenario showing real-world pentesting workflow"""
    
    print_colored("\n" + "=" * 80, Colors.CYAN)
    print_colored("🎯 ADVANCED PENTESTING SCENARIO", Colors.CYAN, bold=True)
    print_colored("=" * 80, Colors.CYAN)
    print()
    
    # Multiple targets scenario
    targets = ["testphp.vulnweb.com", "httpbin.org"]
    
    for i, target in enumerate(targets, 1):
        print_colored(f"🎯 Target {i}: {target}", Colors.YELLOW, bold=True)
        print_colored("-" * 50, Colors.YELLOW)
        
        # Multi-stage parallel reconnaissance
        stage1_commands = f"parallel_execute:nmap -sn {target};dig {target};ping -c 3 {target}"
        
        print_colored("🔍 Stage 1: Host Discovery", Colors.BLUE)
        execute_command(
            command=stage1_commands,
            phase=f"host_discovery_{target}",
            tool_category="reconnaissance",
            expected_outcome="Confirm target availability"
        )
        
        time.sleep(1)
        
        # Service enumeration 
        stage2_commands = f"parallel_execute:nmap -sS -O {target};nmap -sV -p 80,443 {target};nmap -sC -p 80,443 {target}"
        
        print_colored("🔍 Stage 2: Service Enumeration", Colors.BLUE)
        execute_command(
            command=stage2_commands,
            phase=f"service_enum_{target}",
            tool_category="network_scanning",
            expected_outcome="Identify running services"
        )
        
        time.sleep(1)
        
        # Web application testing
        stage3_commands = f"parallel_execute:curl -I http://{target};curl -s http://{target}/robots.txt;whatweb http://{target}"
        
        print_colored("🌐 Stage 3: Web Application Analysis", Colors.BLUE)
        execute_command(
            command=stage3_commands,
            phase=f"web_analysis_{target}",
            tool_category="web_application",
            expected_outcome="Analyze web technologies and structure"
        )
        
        print()
    
    print_colored("🏁 Advanced scenario completed!", Colors.GREEN, bold=True)
    print_colored("📊 All results saved and analyzed automatically", Colors.CYAN)

if __name__ == "__main__":
    # Run main demo
    main_demo()
    
    # Ask if user wants to see advanced scenario
    print("\n" + "="*60)
    response = input("🤔 Run advanced multi-target scenario? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        advanced_pentesting_scenario()
    
    print()
    print_colored("✨ Demo complete! Multi-terminal pentesting system is ready!", Colors.GREEN, bold=True)
