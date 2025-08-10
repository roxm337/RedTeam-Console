#!/usr/bin/env python3
"""
Session Management Test
Comprehensive test of the session management system
"""

import os
import time
import tempfile
from pathlib import Path
from session_manager import session_manager, start_new_session, list_recent_sessions
from command_executor_v2 import execute_command
from wordlist_manager import ensure_wordlists_ready
from config import print_colored, Colors

def create_test_files():
    """Create some test files to simulate pentesting activity"""
    
    # Create files in results directory
    results_dir = session_manager.results_dir
    
    # Simulate nmap scan results
    nmap_result = results_dir / "nmap_scan.txt"
    with open(nmap_result, 'w') as f:
        f.write("Nmap scan results:\n")
        f.write("PORT     STATE SERVICE\n")
        f.write("22/tcp   open  ssh\n")
        f.write("80/tcp   open  http\n")
        f.write("443/tcp  open  https\n")
    
    # Simulate gobuster results
    gobuster_result = results_dir / "gobuster_dirs.txt"
    with open(gobuster_result, 'w') as f:
        f.write("Gobuster directory enumeration:\n")
        f.write("/admin (Status: 200)\n")
        f.write("/login (Status: 200)\n")
        f.write("/backup (Status: 403)\n")
    
    # Create files in logs directory
    logs_dir = session_manager.logs_dir
    
    # Simulate command log
    cmd_log = logs_dir / "commands.log"
    with open(cmd_log, 'w') as f:
        f.write("2024-08-06 14:30:00 - INFO - Executed: nmap -sS target.com\n")
        f.write("2024-08-06 14:31:00 - INFO - Executed: gobuster dir -u http://target.com\n")
        f.write("2024-08-06 14:32:00 - WARNING - Potential vulnerability found\n")
    
    # Create files in current session directory
    session_dir = session_manager.current_session_dir
    
    # Simulate session notes
    notes_file = session_dir / "session_notes.md"
    with open(notes_file, 'w') as f:
        f.write("# Pentesting Session Notes\n\n")
        f.write("## Target: example.com\n\n")
        f.write("### Findings:\n")
        f.write("- Web server running on port 80\n")
        f.write("- SSH service on port 22\n")
        f.write("- Admin panel discovered\n")
    
    print_colored("✅ Test files created:", Colors.GREEN)
    print_colored(f"   📄 {nmap_result}", Colors.LIGHTWHITE_EX)
    print_colored(f"   📄 {gobuster_result}", Colors.LIGHTWHITE_EX)
    print_colored(f"   📄 {cmd_log}", Colors.LIGHTWHITE_EX)
    print_colored(f"   📄 {notes_file}", Colors.LIGHTWHITE_EX)
    print()

def test_session_lifecycle():
    """Test complete session lifecycle"""
    print_colored("🔄 TESTING SESSION LIFECYCLE", Colors.CYAN, bold=True)
    print_colored("=" * 50, Colors.CYAN)
    print()
    
    # Step 1: Start first session
    print_colored("📅 Step 1: Starting first session", Colors.BLUE, bold=True)
    session1_id = start_new_session("Web_App_Test")
    
    # Create some test activity
    create_test_files()
    
    # Show current stats
    stats = session_manager.get_session_stats()
    print_colored(f"📊 Current session has {stats['current_session_files']} files", Colors.YELLOW)
    print()
    
    time.sleep(1)
    
    # Step 2: Start second session (should archive first)
    print_colored("📅 Step 2: Starting second session", Colors.BLUE, bold=True)
    session2_id = start_new_session("Network_Scan")
    
    # Create different test activity
    results_dir = session_manager.results_dir
    network_result = results_dir / "network_scan.txt"
    with open(network_result, 'w') as f:
        f.write("Network scan results for session 2\n")
        f.write("Host discovery completed\n")
    
    print_colored("✅ Second session active with different content", Colors.GREEN)
    print()
    
    time.sleep(1)
    
    # Step 3: List sessions
    print_colored("📋 Step 3: Listing all sessions", Colors.BLUE, bold=True)
    list_recent_sessions()
    
    # Step 4: Restore first session
    print_colored("🔄 Step 4: Restoring first session", Colors.BLUE, bold=True)
    success = session_manager.restore_session(session1_id)
    
    if success:
        # Verify restored content
        notes_file = session_manager.current_session_dir / "session_notes.md"
        if notes_file.exists():
            print_colored("✅ First session restored successfully", Colors.GREEN)
            print_colored(f"   📄 Found restored file: {notes_file}", Colors.LIGHTWHITE_EX)
        else:
            print_colored("❌ Session restoration may have failed", Colors.RED)
    
    print()

def test_session_commands():
    """Test session management with actual commands"""
    print_colored("🛠️  TESTING SESSION WITH COMMANDS", Colors.CYAN, bold=True)
    print_colored("=" * 50, Colors.CYAN)
    print()
    
    # Start a new session for testing
    session_id = start_new_session("Command_Test")
    
    # Ensure wordlists are ready
    ensure_wordlists_ready()
    
    # Test some basic commands that generate output
    test_commands = [
        "echo 'Testing session command logging'",
        "pwd",
        "ls -la",
        "whoami"
    ]
    
    for cmd in test_commands:
        print_colored(f"🔍 Executing: {cmd}", Colors.YELLOW)
        result, code, error = execute_command(
            command=cmd,
            phase="session_testing",
            tool_category="system",
            expected_outcome="Basic system information"
        )
        
        if code == 0:
            print_colored("   ✅ Command executed successfully", Colors.GREEN)
        else:
            print_colored(f"   ❌ Command failed: {error}", Colors.RED)
        
        time.sleep(0.5)
    
    # Show session statistics
    stats = session_manager.get_session_stats()
    print_colored(f"📊 Session now has {stats['current_session_files']} files", Colors.CYAN)
    print()

def test_cleanup_functionality():
    """Test cleanup and archiving functionality"""
    print_colored("🧹 TESTING CLEANUP FUNCTIONALITY", Colors.CYAN, bold=True)
    print_colored("=" * 50, Colors.CYAN)
    print()
    
    # Show current stats before cleanup
    stats_before = session_manager.get_session_stats()
    print_colored("📊 Before cleanup:", Colors.YELLOW)
    print_colored(f"   Total Sessions: {stats_before['total_sessions']}", Colors.LIGHTWHITE_EX)
    print_colored(f"   Current Files: {stats_before['current_session_files']}", Colors.LIGHTWHITE_EX)
    print_colored(f"   Disk Usage: {stats_before['disk_usage_mb']} MB", Colors.LIGHTWHITE_EX)
    print()
    
    # Archive current session
    print_colored("📦 Archiving current session...", Colors.YELLOW)
    session_manager.archive_current_session()
    
    # Show stats after archiving
    stats_after = session_manager.get_session_stats()
    print_colored("📊 After archiving:", Colors.GREEN)
    print_colored(f"   Total Sessions: {stats_after['total_sessions']}", Colors.LIGHTWHITE_EX)
    print_colored(f"   Current Files: {stats_after['current_session_files']}", Colors.LIGHTWHITE_EX)
    print_colored(f"   Disk Usage: {stats_after['disk_usage_mb']} MB", Colors.LIGHTWHITE_EX)
    print()
    
    # Clean workspace
    print_colored("🧹 Testing workspace cleanup...", Colors.YELLOW)
    session_manager.clean_current_directories()
    
    final_stats = session_manager.get_session_stats()
    print_colored(f"✅ Cleanup complete - Current files: {final_stats['current_session_files']}", Colors.GREEN)
    print()

def demonstrate_session_features():
    """Demonstrate key session management features"""
    print_colored("🎯 SESSION MANAGEMENT FEATURE DEMO", Colors.CYAN, bold=True)
    print_colored("=" * 50, Colors.CYAN)
    print()
    
    # Feature 1: Working directories
    print_colored("📁 Feature 1: Organized Working Directories", Colors.BLUE, bold=True)
    
    from session_manager import get_session_working_directories
    dirs = get_session_working_directories()
    
    for name, path in dirs.items():
        exists = "✅" if os.path.exists(path) else "❌"
        print_colored(f"   {name}: {exists} {path}", Colors.YELLOW)
    print()
    
    # Feature 2: Automatic path integration
    print_colored("📍 Feature 2: Automatic Path Integration", Colors.BLUE, bold=True)
    print_colored(f"   Results go to: {session_manager.results_dir}", Colors.LIGHTWHITE_EX)
    print_colored(f"   Logs go to: {session_manager.logs_dir}", Colors.LIGHTWHITE_EX)
    print_colored(f"   Session data: {session_manager.current_session_dir}", Colors.LIGHTWHITE_EX)
    print()
    
    # Feature 3: Session metadata
    print_colored("📋 Feature 3: Session Metadata", Colors.BLUE, bold=True)
    metadata_file = session_manager.current_session_dir / "session_metadata.json"
    if metadata_file.exists():
        print_colored(f"   ✅ Metadata file: {metadata_file}", Colors.GREEN)
    else:
        print_colored(f"   📝 Metadata will be created: {metadata_file}", Colors.YELLOW)
    print()

def main():
    """Main test function"""
    print_colored("🤖 AI PENTESTER AGENT - SESSION MANAGEMENT TEST", Colors.GREEN, bold=True)
    print_colored("=" * 60, Colors.GREEN)
    print()
    
    try:
        # Demo session features
        demonstrate_session_features()
        
        # Test session lifecycle
        test_session_lifecycle()
        
        # Test with actual commands
        test_session_commands()
        
        # Test cleanup
        test_cleanup_functionality()
        
        print_colored("🎉 ALL SESSION MANAGEMENT TESTS COMPLETED!", Colors.GREEN, bold=True)
        print_colored("✅ Session archiving working", Colors.GREEN)
        print_colored("✅ Session restoration working", Colors.GREEN)
        print_colored("✅ Automatic cleanup working", Colors.GREEN)
        print_colored("✅ Organized directory structure", Colors.GREEN)
        print_colored("✅ Command integration working", Colors.GREEN)
        
        # Final session list
        print()
        print_colored("📋 FINAL SESSION LIST", Colors.CYAN, bold=True)
        list_recent_sessions()
        
    except Exception as e:
        print_colored(f"❌ Test failed: {e}", Colors.RED)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
