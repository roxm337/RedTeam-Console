#!/usr/bin/env python3
"""
Session Manager for AI Pentester Agent
Manages session archiving, cleanup, and organization
"""

import os
import shutil
import datetime
import json
import glob
from pathlib import Path
from config import print_colored, Colors

class SessionManager:
    """Manages pentesting sessions, archiving, and cleanup"""
    
    def __init__(self, base_sessions_dir: str = "sessions"):
        self.base_sessions_dir = Path(base_sessions_dir)
        self.current_session_dir = Path("current_session")
        self.results_dir = Path("results")
        self.logs_dir = Path("logs")
        
        # Session metadata
        self.session_start_time = None
        self.session_id = None
        
        # Ensure base directories exist
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure all necessary directories exist"""
        directories = [
            self.base_sessions_dir,
            self.current_session_dir,
            self.results_dir,
            self.logs_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def generate_session_id(self) -> str:
        """Generate a unique session identifier"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"session_{timestamp}"
    
    def start_new_session(self, session_name: str = None) -> str:
        """Start a new pentesting session"""
        # Archive current session if it exists
        if self.has_active_session():
            self.archive_current_session()
        
        # Generate new session ID
        self.session_id = self.generate_session_id()
        self.session_start_time = datetime.datetime.now()
        
        # Use custom name if provided
        if session_name:
            session_name_clean = session_name.replace(" ", "_").replace("/", "_")
            self.session_id = f"{self.session_id}_{session_name_clean}"
        
        # Clean current working directories
        self.clean_current_directories()
        
        # Create session metadata
        self.create_session_metadata()
        
        print_colored("🚀 NEW SESSION STARTED", Colors.GREEN, bold=True)
        print_colored(f"📋 Session ID: {self.session_id}", Colors.CYAN)
        print_colored(f"🕐 Start Time: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}", Colors.CYAN)
        print_colored(f"📁 Working Directory: {self.current_session_dir}", Colors.CYAN)
        print()
        
        return self.session_id
    
    def has_active_session(self) -> bool:
        """Check if there's an active session with data"""
        if not self.current_session_dir.exists():
            return False
        
        # Check for any files in current session directories
        session_files = []
        for directory in [self.current_session_dir, self.results_dir, self.logs_dir]:
            if directory.exists():
                session_files.extend(list(directory.rglob("*")))
        
        # Filter out directories, only count files
        session_files = [f for f in session_files if f.is_file()]
        
        return len(session_files) > 0
    
    def archive_current_session(self):
        """Archive the current session to sessions directory"""
        if not self.has_active_session():
            print_colored("ℹ️  No active session to archive", Colors.YELLOW)
            return
        
        # Generate archive session ID if not already set
        if not self.session_id:
            self.session_id = self.generate_session_id()
        
        archive_dir = self.base_sessions_dir / self.session_id
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        print_colored("📦 ARCHIVING CURRENT SESSION", Colors.YELLOW, bold=True)
        print_colored(f"📁 Archive Location: {archive_dir}", Colors.LIGHTBLACK_EX)
        
        # Archive directories with content
        archived_items = []
        
        # Archive current_session directory
        if self.current_session_dir.exists() and any(self.current_session_dir.iterdir()):
            session_archive = archive_dir / "session_data"
            shutil.copytree(self.current_session_dir, session_archive, dirs_exist_ok=True)
            archived_items.append(f"session_data ({self.count_files(session_archive)} files)")
        
        # Archive results directory
        if self.results_dir.exists() and any(self.results_dir.iterdir()):
            results_archive = archive_dir / "results"
            shutil.copytree(self.results_dir, results_archive, dirs_exist_ok=True)
            archived_items.append(f"results ({self.count_files(results_archive)} files)")
        
        # Archive logs directory
        if self.logs_dir.exists() and any(self.logs_dir.iterdir()):
            logs_archive = archive_dir / "logs"
            shutil.copytree(self.logs_dir, logs_archive, dirs_exist_ok=True)
            archived_items.append(f"logs ({self.count_files(logs_archive)} files)")
        
        # Create archive summary
        self.create_archive_summary(archive_dir, archived_items)
        
        print_colored("✅ Session archived successfully!", Colors.GREEN)
        for item in archived_items:
            print_colored(f"   📁 {item}", Colors.LIGHTWHITE_EX)
        print()
    
    def clean_current_directories(self):
        """Clean current working directories for new session"""
        print_colored("🧹 CLEANING WORKSPACE", Colors.YELLOW, bold=True)
        
        cleaned_items = []
        
        # Clean current_session directory
        if self.current_session_dir.exists():
            file_count = self.count_files(self.current_session_dir)
            if file_count > 0:
                shutil.rmtree(self.current_session_dir)
                self.current_session_dir.mkdir(parents=True, exist_ok=True)
                cleaned_items.append(f"current_session ({file_count} files)")
        
        # Clean results directory
        if self.results_dir.exists():
            file_count = self.count_files(self.results_dir)
            if file_count > 0:
                shutil.rmtree(self.results_dir)
                self.results_dir.mkdir(parents=True, exist_ok=True)
                cleaned_items.append(f"results ({file_count} files)")
        
        # Clean logs directory
        if self.logs_dir.exists():
            file_count = self.count_files(self.logs_dir)
            if file_count > 0:
                shutil.rmtree(self.logs_dir)
                self.logs_dir.mkdir(parents=True, exist_ok=True)
                cleaned_items.append(f"logs ({file_count} files)")
        
        # Clean any .txt, .json, .xml files in root directory
        root_files = []
        for pattern in ["*.txt", "*.json", "*.xml", "*.csv", "*.log"]:
            root_files.extend(glob.glob(pattern))
        
        if root_files:
            for file in root_files:
                try:
                    os.remove(file)
                    cleaned_items.append(f"root file: {file}")
                except Exception as e:
                    print_colored(f"⚠️  Could not remove {file}: {e}", Colors.RED)
        
        if cleaned_items:
            print_colored("🗑️  Cleaned:", Colors.GREEN)
            for item in cleaned_items:
                print_colored(f"   📄 {item}", Colors.LIGHTWHITE_EX)
        else:
            print_colored("✨ Workspace already clean", Colors.GREEN)
        print()
    
    def count_files(self, directory: Path) -> int:
        """Count files in a directory recursively"""
        if not directory.exists():
            return 0
        return len([f for f in directory.rglob("*") if f.is_file()])
    
    def create_session_metadata(self):
        """Create metadata file for current session"""
        metadata = {
            "session_id": self.session_id,
            "start_time": self.session_start_time.isoformat(),
            "status": "active",
            "directories": {
                "current_session": str(self.current_session_dir),
                "results": str(self.results_dir),
                "logs": str(self.logs_dir)
            },
            "tools_used": [],
            "targets": [],
            "phases_completed": []
        }
        
        metadata_file = self.current_session_dir / "session_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def create_archive_summary(self, archive_dir: Path, archived_items: list):
        """Create summary file for archived session"""
        end_time = datetime.datetime.now()
        
        summary = {
            "session_id": self.session_id,
            "start_time": self.session_start_time.isoformat() if self.session_start_time else None,
            "end_time": end_time.isoformat(),
            "duration": str(end_time - self.session_start_time) if self.session_start_time else "Unknown",
            "archived_items": archived_items,
            "archive_location": str(archive_dir),
            "total_files": self.count_files(archive_dir)
        }
        
        summary_file = archive_dir / "session_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Also create a readable summary
        readme_file = archive_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(f"# Session Archive: {self.session_id}\n\n")
            f.write(f"**Start Time:** {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S') if self.session_start_time else 'Unknown'}\n")
            f.write(f"**End Time:** {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Duration:** {summary['duration']}\n")
            f.write(f"**Total Files:** {summary['total_files']}\n\n")
            f.write("## Archived Content:\n\n")
            for item in archived_items:
                f.write(f"- {item}\n")
            f.write(f"\n## Directory Structure:\n\n")
            f.write("```\n")
            f.write(f"{archive_dir.name}/\n")
            for item in archive_dir.iterdir():
                if item.is_dir():
                    f.write(f"├── {item.name}/\n")
                else:
                    f.write(f"├── {item.name}\n")
            f.write("```\n")
    
    def list_sessions(self, limit: int = 10):
        """List recent sessions"""
        print_colored("📋 RECENT SESSIONS", Colors.CYAN, bold=True)
        print_colored("=" * 50, Colors.CYAN)
        
        if not self.base_sessions_dir.exists():
            print_colored("No sessions found", Colors.YELLOW)
            return
        
        sessions = sorted([d for d in self.base_sessions_dir.iterdir() if d.is_dir()], 
                         key=lambda x: x.name, reverse=True)
        
        if not sessions:
            print_colored("No sessions found", Colors.YELLOW)
            return
        
        for i, session_dir in enumerate(sessions[:limit]):
            session_name = session_dir.name
            summary_file = session_dir / "session_summary.json"
            
            if summary_file.exists():
                try:
                    with open(summary_file, 'r') as f:
                        summary = json.load(f)
                    
                    print_colored(f"{i+1}. {session_name}", Colors.YELLOW, bold=True)
                    print_colored(f"   📅 {summary.get('start_time', 'Unknown')[:19].replace('T', ' ')}", Colors.LIGHTWHITE_EX)
                    print_colored(f"   ⏱️  Duration: {summary.get('duration', 'Unknown')}", Colors.LIGHTWHITE_EX)
                    print_colored(f"   📁 Files: {summary.get('total_files', 0)}", Colors.LIGHTWHITE_EX)
                    print_colored(f"   📍 Location: {session_dir}", Colors.LIGHTBLACK_EX)
                    
                except Exception as e:
                    print_colored(f"{i+1}. {session_name}", Colors.YELLOW, bold=True)
                    print_colored(f"   ❌ Error reading summary: {e}", Colors.RED)
            else:
                print_colored(f"{i+1}. {session_name}", Colors.YELLOW, bold=True)
                print_colored(f"   📁 Location: {session_dir}", Colors.LIGHTBLACK_EX)
            
            print()
    
    def restore_session(self, session_id: str):
        """Restore a previous session to current workspace"""
        session_dir = self.base_sessions_dir / session_id
        
        if not session_dir.exists():
            print_colored(f"❌ Session {session_id} not found", Colors.RED)
            return False
        
        print_colored(f"🔄 RESTORING SESSION: {session_id}", Colors.YELLOW, bold=True)
        
        # Archive current session if it has data
        if self.has_active_session():
            print_colored("📦 Archiving current session first...", Colors.YELLOW)
            self.archive_current_session()
        
        # Clean current directories
        self.clean_current_directories()
        
        # Restore from archive
        restored_items = []
        
        # Restore session data
        session_archive = session_dir / "session_data"
        if session_archive.exists():
            shutil.copytree(session_archive, self.current_session_dir, dirs_exist_ok=True)
            restored_items.append(f"session_data ({self.count_files(self.current_session_dir)} files)")
        
        # Restore results
        results_archive = session_dir / "results"
        if results_archive.exists():
            shutil.copytree(results_archive, self.results_dir, dirs_exist_ok=True)
            restored_items.append(f"results ({self.count_files(self.results_dir)} files)")
        
        # Restore logs
        logs_archive = session_dir / "logs"
        if logs_archive.exists():
            shutil.copytree(logs_archive, self.logs_dir, dirs_exist_ok=True)
            restored_items.append(f"logs ({self.count_files(self.logs_dir)} files)")
        
        print_colored("✅ Session restored successfully!", Colors.GREEN)
        for item in restored_items:
            print_colored(f"   📁 {item}", Colors.LIGHTWHITE_EX)
        print()
        
        return True
    
    def get_session_stats(self):
        """Get statistics about current and archived sessions"""
        stats = {
            "total_sessions": 0,
            "current_session_files": 0,
            "total_archived_files": 0,
            "disk_usage_mb": 0
        }
        
        # Count archived sessions
        if self.base_sessions_dir.exists():
            sessions = [d for d in self.base_sessions_dir.iterdir() if d.is_dir()]
            stats["total_sessions"] = len(sessions)
            
            for session_dir in sessions:
                stats["total_archived_files"] += self.count_files(session_dir)
        
        # Count current session files
        for directory in [self.current_session_dir, self.results_dir, self.logs_dir]:
            if directory.exists():
                stats["current_session_files"] += self.count_files(directory)
        
        # Calculate disk usage
        try:
            if self.base_sessions_dir.exists():
                total_size = sum(f.stat().st_size for f in self.base_sessions_dir.rglob('*') if f.is_file())
                stats["disk_usage_mb"] = round(total_size / (1024 * 1024), 2)
        except Exception:
            stats["disk_usage_mb"] = 0
        
        return stats
    
    def cleanup_old_sessions(self, days_old: int = 30, keep_minimum: int = 5):
        """Clean up sessions older than specified days"""
        if not self.base_sessions_dir.exists():
            return
        
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days_old)
        sessions = sorted([d for d in self.base_sessions_dir.iterdir() if d.is_dir()], 
                         key=lambda x: x.name, reverse=True)
        
        # Always keep minimum number of recent sessions
        sessions_to_check = sessions[keep_minimum:]
        removed_count = 0
        
        print_colored(f"🧹 CLEANING OLD SESSIONS (>{days_old} days, keeping ≥{keep_minimum})", Colors.YELLOW, bold=True)
        
        for session_dir in sessions_to_check:
            try:
                # Extract date from session name
                date_part = session_dir.name.split('_')[1] + "_" + session_dir.name.split('_')[2]
                session_date = datetime.datetime.strptime(date_part, "%Y%m%d_%H%M%S")
                
                if session_date < cutoff_date:
                    print_colored(f"🗑️  Removing old session: {session_dir.name}", Colors.LIGHTBLACK_EX)
                    shutil.rmtree(session_dir)
                    removed_count += 1
                    
            except Exception as e:
                print_colored(f"⚠️  Could not process {session_dir.name}: {e}", Colors.YELLOW)
        
        if removed_count > 0:
            print_colored(f"✅ Removed {removed_count} old session(s)", Colors.GREEN)
        else:
            print_colored("✨ No old sessions to remove", Colors.GREEN)
        print()

# Global session manager instance
session_manager = SessionManager()

def start_new_session(session_name: str = None) -> str:
    """Convenience function to start a new session"""
    return session_manager.start_new_session(session_name)

def archive_current_session():
    """Convenience function to archive current session"""
    session_manager.archive_current_session()

def list_recent_sessions(limit: int = 10):
    """Convenience function to list recent sessions"""
    session_manager.list_sessions(limit)

def get_session_working_directories():
    """Get current session working directories"""
    return {
        "current_session": str(session_manager.current_session_dir),
        "results": str(session_manager.results_dir),
        "logs": str(session_manager.logs_dir)
    }

if __name__ == "__main__":
    # Demo the session manager
    print_colored("🤖 AI PENTESTER AGENT - SESSION MANAGER DEMO", Colors.GREEN, bold=True)
    print_colored("=" * 60, Colors.GREEN)
    print()
    
    # Show current stats
    stats = session_manager.get_session_stats()
    print_colored("📊 SESSION STATISTICS", Colors.CYAN, bold=True)
    print_colored(f"   Total Sessions: {stats['total_sessions']}", Colors.YELLOW)
    print_colored(f"   Current Session Files: {stats['current_session_files']}", Colors.YELLOW)
    print_colored(f"   Total Archived Files: {stats['total_archived_files']}", Colors.YELLOW)
    print_colored(f"   Disk Usage: {stats['disk_usage_mb']} MB", Colors.YELLOW)
    print()
    
    # List recent sessions
    list_recent_sessions()
    
    # Show working directories
    dirs = get_session_working_directories()
    print_colored("📁 CURRENT WORKING DIRECTORIES", Colors.CYAN, bold=True)
    for name, path in dirs.items():
        print_colored(f"   {name}: {path}", Colors.YELLOW)
    print()
