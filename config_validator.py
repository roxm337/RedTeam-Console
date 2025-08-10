# config_validator.py
"""
Configuration validation and management.
"""

import os
from typing import Dict, List, Tuple
from config import Colors, print_colored

class ConfigValidator:
    """Validates and manages configuration settings."""
    
    REQUIRED_ENV_VARS = [
        "GEMINI_API_KEY"
    ]
    
    OPTIONAL_ENV_VARS = [
        "SUDO_PASSWORD",
        "COMMAND_TIMEOUT_SECONDS",
        "MAX_ITERATIONS"
    ]
    
    def validate_environment(self) -> Tuple[bool, List[str]]:
        """Validate environment variables and configuration."""
        errors = []
        warnings = []
        
        # Check required environment variables
        for var in self.REQUIRED_ENV_VARS:
            if not os.getenv(var):
                errors.append(f"Missing required environment variable: {var}")
        
        # Check if API key looks valid (basic check)
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            if len(api_key) < 20:
                warnings.append("GEMINI_API_KEY seems too short - may be invalid")
            if not api_key.startswith("AIza"):
                warnings.append("GEMINI_API_KEY doesn't match expected format")
        
        # Check sudo password warning
        if os.getenv("SUDO_PASSWORD"):
            warnings.append("SUDO_PASSWORD is set - this is a security risk")
        
        # Print results
        if errors:
            print_colored("❌ Configuration Errors:", Colors.RED, bold=True)
            for error in errors:
                print_colored(f"   • {error}", Colors.RED)
        
        if warnings:
            print_colored("⚠️  Configuration Warnings:", Colors.YELLOW, bold=True)
            for warning in warnings:
                print_colored(f"   • {warning}", Colors.YELLOW)
        
        if not errors and not warnings:
            print_colored("✅ Configuration validation passed", Colors.GREEN)
        
        return len(errors) == 0, errors + warnings
    
    def print_config_summary(self):
        """Print a summary of current configuration."""
        print_colored("\n📋 Configuration Summary:", Colors.CYAN, bold=True)
        
        # Safe config items (non-sensitive)
        from config import MODEL_NAME, MAX_ITERATIONS, COMMAND_TIMEOUT_SECONDS, USER_COMMAND_APPROVAL
        
        config_items = [
            ("Model Name", MODEL_NAME),
            ("Max Iterations", MAX_ITERATIONS),
            ("Command Timeout", f"{COMMAND_TIMEOUT_SECONDS}s"),
            ("User Approval Required", "Yes" if USER_COMMAND_APPROVAL else "No"),
            ("API Key Set", "Yes" if os.getenv("GEMINI_API_KEY") else "No"),
            ("Sudo Password Set", "Yes" if os.getenv("SUDO_PASSWORD") else "No")
        ]
        
        for key, value in config_items:
            color = Colors.GREEN if "Yes" in str(value) or value else Colors.YELLOW
            print_colored(f"   {key:20}: {value}", color)

# Global validator instance
config_validator = ConfigValidator()
