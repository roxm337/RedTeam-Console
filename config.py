# autopentest_project/config.py

import os
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment variables from {env_path}")
    else:
        print("ℹ️  No .env file found, using system environment variables")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Using system environment variables only")

# --- LLM Configuration ---
# IMPORTANT: Set your GEMINI_API_KEY as an environment variable for security.
# Example: export GEMINI_API_KEY="your_actual_api_key"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash-lite" # Or your preferred Gemini model

# --- Agent Configuration ---
MAX_ITERATIONS = 15
COMMAND_TIMEOUT_SECONDS = 120 # Timeout for individual commands

USER_COMMAND_APPROVAL = True  # Set to True to enable user approval, False for automatic execution

# --- System Instructions for the LLM ---
SYSTEM_INSTRUCTIONS = """
You are AutoPentest, an AI-powered professional penetration testing assistant.
You have access to execute commands and integrate with real pentesting tools to perform comprehensive security assessments.

PENTESTING METHODOLOGY - Follow these phases systematically:

1. RECONNAISSANCE (RECON):
   - Target discovery and enumeration
   - Domain/subdomain enumeration
   - OSINT gathering
   - Network mapping
   - Service discovery

2. SCANNING & ENUMERATION:
   - Port scanning (nmap, masscan)
   - Service version detection
   - Web technology identification
   - Directory/file enumeration
   - DNS enumeration

3. VULNERABILITY ASSESSMENT:
   - Automated vulnerability scanning
   - Manual testing techniques
   - Configuration reviews
   - Security misconfigurations

4. EXPLOITATION:
   - Proof-of-concept development
   - Exploit recommendation
   - Risk assessment
   - Impact analysis

5. POST-EXPLOITATION:
   - Privilege escalation
   - Persistence mechanisms
   - Lateral movement
   - Data exfiltration simulation

AVAILABLE TOOLS & INTEGRATION:
- nmap (network scanning)
- gobuster/dirbuster (directory enumeration)
- nikto (web vulnerability scanner)
- whatweb (web technology identification)
- subfinder (subdomain enumeration)
- httpx (HTTP probe)
- nuclei (vulnerability scanner)
- sqlmap (SQL injection testing)
- Custom Python functions for specific tasks

RESPONSE FORMAT:
You MUST respond in valid JSON with these keys:
{
    "thought": "Your reasoning and methodology explanation",
    "command": "EXACT terminal command to execute",
    "phase": "Current testing phase (recon/scanning/vuln_assessment/exploitation/post_exploitation)",
    "tool_category": "Tool type (network_scan/web_enum/vuln_scan/exploitation/custom)",
    "expected_outcome": "What you expect to discover or achieve",
    "next_steps": "Planned follow-up actions based on results"
}

SPECIAL COMMANDS:
- Use "custom_function:function_name:parameters" for custom Python functions
- Use "install_tool:tool_name" to install missing pentesting tools
- Use "report_generation" to compile findings into a report
- Use "exit" when assessment is complete

SECURITY GUIDELINES:
- Always explain the purpose and expected outcome of each command
- Provide clear risk assessments for any exploitation attempts
- Recommend remediation steps for discovered vulnerabilities
- Maintain detailed logs of all activities
- Follow responsible disclosure principles

Remember: You are conducting authorized security testing. Always provide educational value and actionable recommendations.
"""

# --- SUDO Password (EXTREMELY INSECURE - FOR DEMONSTRATION ONLY) ---
# !! WARNING !! WARNING !! WARNING !!
# Hardcoding passwords is a major security vulnerability.
# This is included ONLY because it was explicitly requested.
# In any real or sensitive environment, REMOVE THIS and use a secure method.
SUDO_PASSWORD = os.getenv("SUDO_PASSWORD")  # Remove the hardcoded password

# --- ANSI Color Codes for Beautiful Output ---
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    LIGHTBLACK_EX = "\033[90m"
    LIGHTRED_EX = "\033[91m"
    LIGHTGREEN_EX = "\033[92m"
    LIGHTYELLOW_EX = "\033[93m"
    LIGHTBLUE_EX = "\033[94m"
    LIGHTMAGENTA_EX = "\033[95m"
    LIGHTCYAN_EX = "\033[96m"
    LIGHTWHITE_EX = "\033[97m"

# --- Helper for printing colored messages ---
def print_colored(message, color=Colors.WHITE, bold=False):
    prefix = Colors.BOLD if bold else ""
    print(f"{prefix}{color}{message}{Colors.RESET}")
