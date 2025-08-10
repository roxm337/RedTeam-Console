#!/usr/bin/env python3
"""
AI Pentester Agent with Session Management
Enhanced main entry point with automatic session management
"""

import sys
import argparse
from config import print_colored, Colors
from session_manager import session_manager, start_new_session, list_recent_sessions
from main_agent import main as original_main
from wordlist_manager import ensure_wordlists_ready

def print_banner():
    """Print the AI Pentester Agent banner"""
    banner = """
    ╔═══════════════════════════════════════════════╗
    ║          🤖 AI Pentester Agent v2.0          ║
    ║              with Session Management          ║
    ╚═══════════════════════════════════════════════╝
    """
    print_colored(banner, Colors.CYAN, bold=True)

def show_session_status():
    """Show current session status"""
    stats = session_manager.get_session_stats()
    
    print_colored("📊 SESSION STATUS", Colors.YELLOW, bold=True)
    print_colored(f"   Total Sessions: {stats['total_sessions']}", Colors.LIGHTWHITE_EX)
    print_colored(f"   Current Session Files: {stats['current_session_files']}", Colors.LIGHTWHITE_EX)
    print_colored(f"   Disk Usage: {stats['disk_usage_mb']} MB", Colors.LIGHTWHITE_EX)
    
    if session_manager.session_id:
        print_colored(f"   Active Session: {session_manager.session_id}", Colors.GREEN)
    else:
        print_colored("   No active session", Colors.YELLOW)
    
    print()

def interactive_menu():
    """Interactive menu for session management"""
    while True:
        print_colored("\n🎛️  SESSION MANAGEMENT MENU", Colors.CYAN, bold=True)
        print_colored("=" * 40, Colors.CYAN)
        print_colored("1. Start New Session", Colors.YELLOW)
        print_colored("2. List Recent Sessions", Colors.YELLOW)
        print_colored("3. Restore Previous Session", Colors.YELLOW)
        print_colored("4. Show Session Status", Colors.YELLOW)
        print_colored("5. Clean Old Sessions", Colors.YELLOW)
        print_colored("6. Start Pentesting (Current Session)", Colors.GREEN)
        print_colored("0. Exit", Colors.RED)
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            session_name = input("Enter session name (optional): ").strip()
            session_name = session_name if session_name else None
            start_new_session(session_name)
            
        elif choice == "2":
            list_recent_sessions()
            
        elif choice == "3":
            list_recent_sessions(5)
            session_id = input("Enter session ID to restore: ").strip()
            if session_id:
                session_manager.restore_session(session_id)
            
        elif choice == "4":
            show_session_status()
            
        elif choice == "5":
            days = input("Remove sessions older than how many days? (default: 30): ").strip()
            days = int(days) if days.isdigit() else 30
            session_manager.cleanup_old_sessions(days_old=days)
            
        elif choice == "6":
            # Ensure we have an active session
            if not session_manager.session_id:
                print_colored("🚀 Starting new session for pentesting...", Colors.YELLOW)
                start_new_session()
            
            # Ensure wordlists are ready
            ensure_wordlists_ready()
            
            # Start pentesting
            print_colored("🎯 Starting AI Pentester Agent...", Colors.GREEN, bold=True)
            print()
            break
            
        elif choice == "0":
            print_colored("👋 Goodbye!", Colors.GREEN)
            sys.exit(0)
            
        else:
            print_colored("❌ Invalid option", Colors.RED)

def main():
    """Enhanced main function with session management"""
    parser = argparse.ArgumentParser(description="AI Pentester Agent with Session Management")
    parser.add_argument("--new-session", "-n", metavar="NAME", 
                       help="Start a new session with optional name")
    parser.add_argument("--list-sessions", "-l", action="store_true",
                       help="List recent sessions")
    parser.add_argument("--restore", "-r", metavar="SESSION_ID",
                       help="Restore a previous session")
    parser.add_argument("--auto-start", "-a", action="store_true",
                       help="Auto-start new session and begin pentesting")
    parser.add_argument("--clean-old", metavar="DAYS", type=int,
                       help="Clean sessions older than specified days")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Interactive session management menu")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Handle command line arguments
    if args.list_sessions:
        list_recent_sessions()
        return
    
    if args.clean_old:
        session_manager.cleanup_old_sessions(days_old=args.clean_old)
        return
    
    if args.restore:
        if session_manager.restore_session(args.restore):
            print_colored("✅ Session restored successfully", Colors.GREEN)
        else:
            print_colored("❌ Failed to restore session", Colors.RED)
            return
    
    if args.new_session:
        start_new_session(args.new_session)
    elif args.auto_start:
        # Auto-start new session
        start_new_session()
    elif args.interactive:
        # Interactive menu
        interactive_menu()
    else:
        # Default behavior - show status and prompt
        show_session_status()
        
        if session_manager.has_active_session():
            response = input("Continue with current session? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                start_new_session()
        else:
            start_new_session()
    
    # Ensure wordlists are ready
    print_colored("🔍 Preparing wordlists...", Colors.YELLOW)
    ensure_wordlists_ready()
    
    # Start the main pentesting agent
    print_colored("🎯 Launching AI Pentester Agent...", Colors.GREEN, bold=True)
    print_colored(f"📁 Session Directory: {session_manager.current_session_dir}", Colors.LIGHTBLACK_EX)
    print_colored(f"📊 Results Directory: {session_manager.results_dir}", Colors.LIGHTBLACK_EX)
    print_colored(f"📝 Logs Directory: {session_manager.logs_dir}", Colors.LIGHTBLACK_EX)
    print()
    
    try:
        # Call the original main agent
        original_main()
        
    except KeyboardInterrupt:
        print_colored("\n🛑 Session interrupted by user", Colors.YELLOW)
        
        # Ask if user wants to archive the session
        response = input("Archive current session before exit? (Y/n): ").strip().lower()
        if response not in ['n', 'no']:
            print_colored("📦 Archiving session...", Colors.YELLOW)
            session_manager.archive_current_session()
        
        print_colored("👋 Goodbye!", Colors.GREEN)
        
    except Exception as e:
        print_colored(f"❌ Error occurred: {e}", Colors.RED)
        
        # Auto-archive on error
        print_colored("📦 Auto-archiving session due to error...", Colors.YELLOW)
        session_manager.archive_current_session()
        
        raise
        
    finally:
        # Always show final session stats
        print_colored("\n📊 FINAL SESSION STATISTICS", Colors.CYAN, bold=True)
        stats = session_manager.get_session_stats()
        print_colored(f"   Current Session Files: {stats['current_session_files']}", Colors.YELLOW)
        print_colored(f"   Total Sessions: {stats['total_sessions']}", Colors.YELLOW)
        print_colored(f"   Total Disk Usage: {stats['disk_usage_mb']} MB", Colors.YELLOW)

if __name__ == "__main__":
    main()
