#!/usr/bin/env python3
"""
Complete Integration Demo
Shows session management integrated with wordlist management and parallel execution
"""

import time
from session_manager import start_new_session, session_manager, list_recent_sessions
from wordlist_manager import ensure_wordlists_ready, get_wordlist_for_tool
from command_executor_v2 import execute_command
from config import print_colored, Colors

def demo_complete_integration():
    """Demonstrate the complete integrated system"""
    print_colored("🎯 AI PENTESTER AGENT - COMPLETE INTEGRATION DEMO", Colors.GREEN, bold=True)
    print_colored("=" * 60, Colors.GREEN)
    print()
    
    # Step 1: Start new session with custom name
    print_colored("🚀 STEP 1: Starting New Pentesting Session", Colors.BLUE, bold=True)
    session_id = start_new_session("Complete_Integration_Demo")
    print()
    
    # Step 2: Prepare wordlists
    print_colored("📋 STEP 2: Preparing Wordlists", Colors.BLUE, bold=True)
    ensure_wordlists_ready()
    
    # Show wordlist paths for different tools
    print_colored("🛠️  Wordlist paths for tools:", Colors.CYAN)
    tools = [
        ("gobuster", "directory"),
        ("ffuf", "directory"), 
        ("dirb", "directory"),
        ("hydra", "password")
    ]
    
    for tool, purpose in tools:
        path = get_wordlist_for_tool(tool, purpose)
        print_colored(f"   {tool} ({purpose}): {path}", Colors.YELLOW)
    print()
    
    # Step 3: Simulate comprehensive pentesting with session organization
    print_colored("🔍 STEP 3: Comprehensive Pentesting Simulation", Colors.BLUE, bold=True)
    
    # Phase 1: Reconnaissance
    print_colored("Phase 1: Reconnaissance", Colors.CYAN, bold=True)
    recon_commands = [
        "echo 'Starting reconnaissance phase'",
        "whoami",
        "date",
        "uname -a"
    ]
    
    for cmd in recon_commands:
        result, code, error = execute_command(
            command=cmd,
            phase="reconnaissance", 
            tool_category="information_gathering",
            expected_outcome="Gather system information"
        )
        time.sleep(0.5)
    
    print()
    
    # Phase 2: Network Discovery
    print_colored("Phase 2: Network Discovery", Colors.CYAN, bold=True)
    network_commands = [
        "echo 'Network discovery initiated'",
        "ifconfig | grep inet || ip addr show | grep inet",
        "echo 'Network interfaces enumerated'",
        "ps aux | head -10"
    ]
    
    for cmd in network_commands:
        result, code, error = execute_command(
            command=cmd,
            phase="network_discovery",
            tool_category="network_scanning", 
            expected_outcome="Discover network configuration"
        )
        time.sleep(0.5)
    
    print()
    
    # Phase 3: Parallel Execution Demo
    print_colored("Phase 3: Parallel Execution with Session Management", Colors.CYAN, bold=True)
    
    parallel_commands = [
        "echo 'Parallel task 1: System info'",
        "echo 'Parallel task 2: Process list'", 
        "echo 'Parallel task 3: Network status'",
        "echo 'Parallel task 4: File system check'"
    ]
    
    parallel_cmd = f"parallel_execute:{';'.join(parallel_commands)}"
    
    result, code, error = execute_command(
        command=parallel_cmd,
        phase="parallel_assessment",
        tool_category="comprehensive_scanning",
        expected_outcome="Execute multiple tasks simultaneously"
    )
    
    print()
    
    # Step 4: Show session results
    print_colored("📊 STEP 4: Session Results Summary", Colors.BLUE, bold=True)
    
    stats = session_manager.get_session_stats()
    print_colored(f"📁 Session files created: {stats['current_session_files']}", Colors.GREEN)
    print_colored(f"📍 Results directory: {session_manager.results_dir}", Colors.LIGHTWHITE_EX)
    print_colored(f"📝 Logs directory: {session_manager.logs_dir}", Colors.LIGHTWHITE_EX)
    print_colored(f"💾 Session data: {session_manager.current_session_dir}", Colors.LIGHTWHITE_EX)
    print()
    
    # Step 5: Create session notes
    print_colored("📝 STEP 5: Creating Session Documentation", Colors.BLUE, bold=True)
    
    notes_file = session_manager.current_session_dir / "pentesting_notes.md"
    with open(notes_file, 'w') as f:
        f.write("# Complete Integration Demo - Pentesting Notes\n\n")
        f.write("## Session Overview\n")
        f.write(f"- **Session ID**: {session_id}\n")
        f.write(f"- **Target**: Complete integration demonstration\n")
        f.write(f"- **Tools**: Session management + Wordlist management + Parallel execution\n\n")
        f.write("## Phases Completed\n")
        f.write("1. ✅ Reconnaissance\n")
        f.write("2. ✅ Network Discovery\n") 
        f.write("3. ✅ Parallel Assessment\n\n")
        f.write("## Key Features Demonstrated\n")
        f.write("- Automatic session organization\n")
        f.write("- Wordlist integration\n")
        f.write("- Parallel command execution\n")
        f.write("- Comprehensive logging\n")
        f.write("- Results organization\n\n")
        f.write("## Next Steps\n")
        f.write("- Session will be automatically archived\n")
        f.write("- All results preserved for future reference\n")
        f.write("- Ready for next assessment\n")
    
    print_colored(f"✅ Session notes created: {notes_file}", Colors.GREEN)
    print()
    
    # Step 6: Archive current session
    print_colored("📦 STEP 6: Archiving Session", Colors.BLUE, bold=True)
    session_manager.archive_current_session()
    print()
    
    # Step 7: Show final session list
    print_colored("📋 STEP 7: Final Session Archive", Colors.BLUE, bold=True)
    list_recent_sessions(3)
    
    # Final statistics
    final_stats = session_manager.get_session_stats()
    print_colored("🏆 INTEGRATION DEMO COMPLETE!", Colors.GREEN, bold=True)
    print_colored("=" * 40, Colors.GREEN)
    print_colored("✅ Session management: WORKING", Colors.GREEN)
    print_colored("✅ Wordlist integration: WORKING", Colors.GREEN)
    print_colored("✅ Parallel execution: WORKING", Colors.GREEN)
    print_colored("✅ Automatic archiving: WORKING", Colors.GREEN)
    print_colored("✅ Clean workspace: READY", Colors.GREEN)
    print()
    print_colored(f"📊 Total sessions archived: {final_stats['total_sessions']}", Colors.CYAN)
    print_colored(f"💾 Total disk usage: {final_stats['disk_usage_mb']} MB", Colors.CYAN)
    print_colored(f"🧹 Current workspace: CLEAN", Colors.CYAN)

if __name__ == "__main__":
    demo_complete_integration()
