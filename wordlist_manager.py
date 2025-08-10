#!/usr/bin/env python3
"""
Wordlist Manager for AI Pentester Agent
Manages wordlists for various pentesting tools
"""

import os
import urllib.request
import urllib.error
from pathlib import Path
from config import print_colored, Colors

class WordlistManager:
    """Manages wordlists for pentesting tools"""
    
    def __init__(self, wordlist_dir: str = "/Users/roxm1337/BHSrOxM/wordlist/"):
        self.wordlist_dir = Path(wordlist_dir)
        self.ensure_wordlist_directory()
        
        # Define standard wordlists
        self.wordlists = {
            "common.txt": {
                "description": "Common directory/file names",
                "url": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt",
                "local_path": self.wordlist_dir / "common.txt"
            },
            "directory-list-2.3-medium.txt": {
                "description": "Medium directory list",
                "url": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/directory-list-2.3-medium.txt",
                "local_path": self.wordlist_dir / "directory-list-2.3-medium.txt"
            },
            "raft-large-directories.txt": {
                "description": "Large directory wordlist",
                "url": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/raft-large-directories.txt",
                "local_path": self.wordlist_dir / "raft-large-directories.txt"
            },
            "subdomains-top1million-5000.txt": {
                "description": "Top 5000 subdomains",
                "url": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
                "local_path": self.wordlist_dir / "subdomains-top1million-5000.txt"
            },
            "rockyou.txt": {
                "description": "RockYou password list (partial)",
                "url": "https://raw.githubusercontent.com/brannondorsey/naive-hashcat/master/example-hashes/rockyou-75.txt",
                "local_path": self.wordlist_dir / "rockyou.txt"
            },
            "big.txt": {
                "description": "Big directory/file wordlist",
                "url": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/big.txt",
                "local_path": self.wordlist_dir / "big.txt"
            },
            "usernames.txt": {
                "description": "Common usernames",
                "url": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/Names/names.txt",
                "local_path": self.wordlist_dir / "usernames.txt"
            }
        }
    
    def ensure_wordlist_directory(self):
        """Ensure the wordlist directory exists"""
        try:
            self.wordlist_dir.mkdir(parents=True, exist_ok=True)
            print_colored(f"📁 Wordlist directory: {self.wordlist_dir}", Colors.CYAN)
        except Exception as e:
            print_colored(f"❌ Error creating wordlist directory: {e}", Colors.RED)
    
    def download_wordlist(self, name: str) -> bool:
        """Download a specific wordlist"""
        if name not in self.wordlists:
            print_colored(f"❌ Unknown wordlist: {name}", Colors.RED)
            return False
        
        wordlist_info = self.wordlists[name]
        local_path = wordlist_info["local_path"]
        url = wordlist_info["url"]
        
        # Check if already exists
        if local_path.exists():
            print_colored(f"✅ Wordlist already exists: {local_path}", Colors.GREEN)
            return True
        
        try:
            print_colored(f"📥 Downloading {name}...", Colors.YELLOW)
            print_colored(f"   Source: {url}", Colors.LIGHTBLACK_EX)
            print_colored(f"   Target: {local_path}", Colors.LIGHTBLACK_EX)
            
            urllib.request.urlretrieve(url, local_path)
            
            # Check file size
            size = local_path.stat().st_size
            print_colored(f"✅ Downloaded {name} ({size:,} bytes)", Colors.GREEN)
            return True
            
        except urllib.error.URLError as e:
            print_colored(f"❌ Download failed for {name}: {e}", Colors.RED)
            return False
        except Exception as e:
            print_colored(f"❌ Error downloading {name}: {e}", Colors.RED)
            return False
    
    def create_basic_wordlist(self, name: str, content: list) -> bool:
        """Create a basic wordlist from provided content"""
        try:
            file_path = self.wordlist_dir / name
            with open(file_path, 'w') as f:
                for item in content:
                    f.write(f"{item}\n")
            
            print_colored(f"✅ Created basic wordlist: {file_path} ({len(content)} entries)", Colors.GREEN)
            return True
            
        except Exception as e:
            print_colored(f"❌ Error creating wordlist {name}: {e}", Colors.RED)
            return False
    
    def ensure_wordlist_exists(self, name: str) -> str:
        """Ensure a wordlist exists, download if necessary"""
        if name in self.wordlists:
            local_path = self.wordlists[name]["local_path"]
            
            if not local_path.exists():
                print_colored(f"📥 Wordlist {name} not found, downloading...", Colors.YELLOW)
                if self.download_wordlist(name):
                    return str(local_path)
                else:
                    # Fallback to creating basic wordlist
                    return self.create_fallback_wordlist(name)
            else:
                return str(local_path)
        else:
            # Unknown wordlist, create a basic one
            return self.create_fallback_wordlist(name)
    
    def create_fallback_wordlist(self, name: str) -> str:
        """Create a fallback wordlist when download fails"""
        fallback_path = self.wordlist_dir / name
        
        if name == "common.txt":
            basic_content = [
                "admin", "index", "home", "test", "login", "css", "js", "images", "img", 
                "api", "admin.php", "index.php", "config", "backup", "temp", "tmp",
                "uploads", "download", "files", "docs", "documentation", "help",
                "about", "contact", "user", "users", "account", "profile", "dashboard"
            ]
        elif name == "directory-list-2.3-medium.txt":
            basic_content = [
                "admin", "images", "css", "js", "img", "login", "test", "home",
                "api", "config", "backup", "uploads", "download", "files", "docs",
                "help", "about", "contact", "user", "account", "dashboard", "panel",
                "wp-admin", "wp-content", "wp-includes", "assets", "static", "media"
            ]
        elif name == "subdomains-top1million-5000.txt":
            basic_content = [
                "www", "mail", "ftp", "admin", "test", "dev", "api", "staging",
                "blog", "shop", "store", "support", "help", "docs", "cdn", "assets",
                "static", "media", "images", "files", "download", "secure", "ssl"
            ]
        elif name == "usernames.txt":
            basic_content = [
                "admin", "administrator", "root", "user", "test", "guest", "demo",
                "john", "jane", "smith", "johnson", "williams", "brown", "jones",
                "garcia", "miller", "davis", "rodriguez", "martinez", "hernandez"
            ]
        else:
            basic_content = [
                "admin", "test", "user", "home", "index", "login", "config", "backup"
            ]
        
        self.create_basic_wordlist(name, basic_content)
        return str(fallback_path)
    
    def get_wordlist_path(self, tool: str, purpose: str = "general") -> str:
        """Get appropriate wordlist path for a specific tool and purpose"""
        
        # Tool-specific wordlist mapping
        wordlist_mapping = {
            "gobuster": {
                "directory": "directory-list-2.3-medium.txt",
                "subdomain": "subdomains-top1million-5000.txt",
                "general": "common.txt"
            },
            "dirb": {
                "directory": "common.txt",
                "general": "common.txt"
            },
            "ffuf": {
                "directory": "big.txt",
                "subdomain": "subdomains-top1million-5000.txt",
                "general": "common.txt"
            },
            "wfuzz": {
                "directory": "raft-large-directories.txt",
                "general": "common.txt"
            },
            "hydra": {
                "password": "rockyou.txt",
                "username": "usernames.txt",
                "general": "common.txt"
            }
        }
        
        # Get the appropriate wordlist name
        if tool in wordlist_mapping:
            wordlist_name = wordlist_mapping[tool].get(purpose, wordlist_mapping[tool]["general"])
        else:
            wordlist_name = "common.txt"  # Default fallback
        
        # Ensure the wordlist exists
        return self.ensure_wordlist_exists(wordlist_name)
    
    def list_available_wordlists(self):
        """List all available wordlists"""
        print_colored("📋 Available Wordlists:", Colors.CYAN, bold=True)
        print_colored("-" * 40, Colors.CYAN)
        
        for name, info in self.wordlists.items():
            local_path = info["local_path"]
            status = "✅ Downloaded" if local_path.exists() else "📥 Available for download"
            
            if local_path.exists():
                size = local_path.stat().st_size
                size_str = f" ({size:,} bytes)"
            else:
                size_str = ""
            
            print_colored(f"   {name}: {info['description']}", Colors.YELLOW)
            print_colored(f"      Status: {status}{size_str}", Colors.LIGHTWHITE_EX)
            print_colored(f"      Path: {local_path}", Colors.LIGHTBLACK_EX)
            print()
    
    def download_all_wordlists(self):
        """Download all available wordlists"""
        print_colored("📥 Downloading all wordlists...", Colors.CYAN, bold=True)
        
        success_count = 0
        total_count = len(self.wordlists)
        
        for name in self.wordlists.keys():
            if self.download_wordlist(name):
                success_count += 1
        
        print_colored(f"\n📊 Download Summary: {success_count}/{total_count} successful", Colors.GREEN, bold=True)
    
    def update_command_with_wordlist(self, command: str) -> str:
        """Update a command to use the correct wordlist path"""
        
        # Common wordlist patterns to replace
        replacements = [
            ("/usr/share/wordlists/dirb/common.txt", self.get_wordlist_path("dirb", "directory")),
            ("/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt", self.get_wordlist_path("gobuster", "directory")),
            ("/usr/share/wordlists/rockyou.txt", self.get_wordlist_path("hydra", "password")),
            ("/usr/share/seclists/Discovery/Web-Content/common.txt", self.get_wordlist_path("gobuster", "general")),
        ]
        
        updated_command = command
        for old_path, new_path in replacements:
            if old_path in updated_command:
                updated_command = updated_command.replace(old_path, new_path)
                print_colored(f"🔄 Updated wordlist path in command", Colors.YELLOW)
                print_colored(f"   From: {old_path}", Colors.LIGHTBLACK_EX)
                print_colored(f"   To: {new_path}", Colors.LIGHTBLACK_EX)
        
        return updated_command

# Global wordlist manager instance
wordlist_manager = WordlistManager()

def get_wordlist_for_tool(tool: str, purpose: str = "general") -> str:
    """Convenience function to get wordlist path for a tool"""
    return wordlist_manager.get_wordlist_path(tool, purpose)

def ensure_wordlists_ready():
    """Ensure essential wordlists are available"""
    print_colored("🔍 Checking essential wordlists...", Colors.CYAN)
    
    essential_wordlists = ["common.txt", "directory-list-2.3-medium.txt"]
    
    for wordlist in essential_wordlists:
        wordlist_manager.ensure_wordlist_exists(wordlist)
    
    print_colored("✅ Essential wordlists ready", Colors.GREEN)

if __name__ == "__main__":
    # Test the wordlist manager
    wordlist_manager.list_available_wordlists()
    print()
    
    # Download essential wordlists
    ensure_wordlists_ready()
    print()
    
    # Show tool-specific paths
    print_colored("🛠️  Tool-specific wordlist paths:", Colors.CYAN, bold=True)
    tools = ["gobuster", "dirb", "ffuf", "hydra"]
    
    for tool in tools:
        path = get_wordlist_for_tool(tool, "directory")
        print_colored(f"   {tool}: {path}", Colors.YELLOW)
