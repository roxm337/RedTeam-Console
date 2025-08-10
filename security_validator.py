# security_validator.py
"""
Security validation module for command safety checks.
"""

import re
from typing import List, Tuple
from config import Colors, print_colored

class CommandValidator:
    """Validates commands for security risks before execution."""
    
    # Dangerous commands that should be blocked or require special approval
    DANGEROUS_COMMANDS = [
        r'\brm\s+.*-rf\s*/',  # rm -rf /
        r'\bdd\s+if=.*of=/dev/',  # dd commands to devices
        r'\bmkfs\.',  # filesystem formatting
        r'\bfdisk\b',  # disk partitioning
        r'\bshred\b',  # secure deletion
        r'\bwipefs\b',  # filesystem signature wiping
        r'[:>]\s*/dev/sd[a-z]',  # writing to disk devices
        r'\bfork\s*\(\s*\)\s*while\s*true',  # fork bombs
        r':\(\)\{.*\|.*\&\}\;.*',  # bash fork bomb
    ]
    
    # Commands that modify system critical files
    SYSTEM_MODIFYING = [
        r'/etc/passwd',
        r'/etc/shadow',
        r'/etc/sudoers',
        r'/boot/',
        r'/sys/',
        r'/proc/sys/',
    ]
    
    # Network commands that might be suspicious
    NETWORK_SUSPICIOUS = [
        r'\bnc\s+.*-l.*-e',  # netcat backdoor
        r'\bbash\s+.*\|\s*nc\b',  # reverse shell
        r'/dev/tcp/.*\|\s*sh',  # bash reverse shell
        r'python.*socket.*exec',  # python reverse shell
    ]
    
    def __init__(self):
        self.blocked_patterns = self.DANGEROUS_COMMANDS
        self.warning_patterns = self.SYSTEM_MODIFYING + self.NETWORK_SUSPICIOUS
    
    def validate_command(self, command: str) -> Tuple[bool, str, List[str]]:
        """
        Validate a command for security risks.
        
        Returns:
            Tuple of (is_safe: bool, risk_level: str, warnings: List[str])
        """
        command_lower = command.lower().strip()
        warnings = []
        risk_level = "LOW"
        
        # Check for blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return False, "CRITICAL", [f"Blocked: Command matches dangerous pattern: {pattern}"]
        
        # Check for warning patterns
        for pattern in self.warning_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                warnings.append(f"WARNING: Command matches suspicious pattern: {pattern}")
                risk_level = "HIGH"
        
        # Check for other risk indicators
        if len(command) > 500:
            warnings.append("WARNING: Command is unusually long")
            risk_level = "MEDIUM"
        
        if command.count('|') > 5:
            warnings.append("WARNING: Command has many pipes (complex chain)")
            risk_level = "MEDIUM"
        
        if re.search(r'\$\(.*\)', command):
            warnings.append("WARNING: Command contains command substitution")
            risk_level = "MEDIUM"
        
        if 'sudo' in command_lower and not re.search(r'sudo\s+-S', command):
            warnings.append("INFO: Command uses sudo without -S flag")
        
        return True, risk_level, warnings
    
    def print_validation_result(self, command: str, is_safe: bool, risk_level: str, warnings: List[str]):
        """Print formatted validation results."""
        if not is_safe:
            print_colored(f"🚫 COMMAND BLOCKED: {command}", Colors.RED, bold=True)
            for warning in warnings:
                print_colored(f"   {warning}", Colors.RED)
            return
        
        color = Colors.GREEN
        if risk_level == "HIGH":
            color = Colors.RED
        elif risk_level == "MEDIUM":
            color = Colors.YELLOW
        
        print_colored(f"🔍 Security Check - Risk Level: {risk_level}", color)
        for warning in warnings:
            print_colored(f"   {warning}", Colors.YELLOW)

# Global validator instance
validator = CommandValidator()
