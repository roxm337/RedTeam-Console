# AutoPentest AI Agent v2.0

**🚀 Professional Penetration Testing Framework powered by AI**

AutoPentest Agent v2.0 is a comprehensive AI-powered penetration testing framework that combines Google's Gemini LLM with real pentesting tools and custom functions. It follows industry-standard methodologies (OWASP, PTES) to conduct systematic security assessments.

**⚠️ SECURITY NOTICE:** *This tool executes commands on your system and is designed for authorized security testing only. Always obtain proper authorization before testing any systems.*

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google Gemini API Key
- Unix-like environment (Linux/macOS) or WSL on Windows

### Installation

1. **Clone and Setup:**
   ```bash
   git clone <repository_url>
   cd AI-Pentester-Agent
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Configure Environment:**
   ```bash
   cp .env.template .env
   # Edit .env and add your GEMINI_API_KEY
   source .env
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Agent:**
   ```bash
   python3 main_agent.py
   ```

## 🎯 Comprehensive Pentesting Methodology

### 1. **Reconnaissance & Information Gathering**
- OSINT collection and analysis
- Domain and subdomain enumeration  
- WHOIS lookups and DNS analysis
- Network range discovery
- Social engineering preparation

### 2. **Network & Service Enumeration**
- Port scanning (TCP/UDP)
- Service version detection
- Operating system fingerprinting
- Network topology mapping
- Live host discovery

### 3. **Vulnerability Assessment**
- Automated vulnerability scanning
- Configuration review
- Security misconfiguration detection
- Custom vulnerability checks
- Risk assessment and prioritization

### 4. **Web Application Testing**
- Technology stack identification
- Directory and file enumeration
- Input validation testing
- Authentication bypass attempts
- Session management analysis

### 5. **Exploitation & Post-Exploitation**
- Proof-of-concept development
- Privilege escalation testing
- Lateral movement simulation
- Persistence mechanism analysis
- Data exfiltration simulation

## 🛠️ Integrated Tools & Capabilities

### **Network Scanning Tools**
- **nmap** - Comprehensive port scanner
- **masscan** - High-speed port scanner
- Custom TCP/UDP scanning functions

### **Web Enumeration Tools**
- **gobuster** - Directory/file brute-forcer
- **dirb** - Web content scanner
- **nikto** - Web vulnerability scanner
- **whatweb** - Web technology identifier

### **DNS & Domain Tools**
- **dig** - DNS lookup utility
- **nslookup** - DNS query tool
- Custom DNS enumeration functions
- Subdomain discovery algorithms

### **Vulnerability Scanners**
- **sqlmap** - SQL injection testing
- Custom vulnerability assessment functions
- Security header analysis
- Configuration review tools

### **Custom AI Functions**
```
custom_function:port_scan_basic:target,ports
custom_function:web_tech_detection:url
custom_function:dns_enumeration:domain
custom_function:whois_lookup:domain
custom_function:vulnerability_check:url
custom_function:network_discovery:range
```

## 📊 Advanced Features

### **🤖 AI-Driven Decision Making**
- Intelligent tool selection based on target type
- Adaptive methodology based on findings
- Context-aware command generation
- Result analysis and next-step planning

### **🔒 Enhanced Security Controls**
- Command validation and risk assessment
- User approval workflows
- Security event logging
- Dangerous command blocking

### **📈 Comprehensive Reporting**
- Real-time session logging
- Structured finding documentation
- Executive summary generation
- Technical detail compilation
- Remediation recommendations

### **� Professional Integration**
- Standard pentesting tool integration
- Custom Python function library
- Wordlist and payload management
- Automated tool installation

## 📋 Usage Examples

### **Basic Reconnaissance**
```
Objective: Reconnaissance scan of example.com
```

### **Network Assessment**
```
Objective: Vulnerability assessment of 192.168.1.0/24
```

### **Web Application Testing**
```
Objective: Web application security test of https://target.com
```

### **Custom Function Usage**
```
Command: custom_function:dns_enumeration:target.com
Command: custom_function:port_scan_basic:192.168.1.100,22-80-443-8080
Command: custom_function:web_tech_detection:https://example.com
```

## 🏗️ Project Architecture

```
AI-Pentester-Agent/
├── main_agent.py              # Main orchestration engine
├── config.py                  # Configuration management
├── gemini_llm_client.py      # AI/LLM integration
├── command_executor.py       # Command execution engine
├── pentesting_tools.py       # Tool management system
├── custom_functions.py       # Custom pentesting functions
├── security_validator.py     # Command security validation
├── enhanced_logger.py        # Advanced logging system
├── config_validator.py       # Environment validation
├── wordlists/                # Pentesting wordlists
│   ├── common_dirs.txt       # Directory enumeration
│   └── common_subdomains.txt # Subdomain enumeration
├── logs/                     # Session logs and reports
├── requirements.txt          # Python dependencies
├── setup.sh                  # Automated setup script
├── .env.template            # Environment configuration
└── README.md                # This documentation
```

## ⚙️ Configuration Options

### **Environment Variables**
```bash
GEMINI_API_KEY="your_api_key_here"    # Required
SUDO_PASSWORD="password"              # Optional (INSECURE)
MAX_ITERATIONS="20"                   # Optional
COMMAND_TIMEOUT_SECONDS="180"         # Optional
```

### **Agent Behavior**
- `USER_COMMAND_APPROVAL`: Enable/disable command approval
- `MODEL_NAME`: Specify Gemini model variant
- `COMMAND_TIMEOUT_SECONDS`: Set command execution timeout
- `MAX_ITERATIONS`: Limit assessment iterations

## 🔐 Security Considerations

### **Command Execution**
- All commands are validated before execution
- User approval required for high-risk operations
- Dangerous command patterns are blocked
- Comprehensive audit logging maintained

### **Authentication & Authorization**
- API keys stored in environment variables
- No hardcoded credentials (except optional sudo)
- Session-based security tracking
- User control over all operations

### **Responsible Disclosure**
- Only test authorized systems
- Follow responsible disclosure practices
- Document all findings properly
- Provide actionable remediation steps

## 🚀 Advanced Usage

### **Tool Installation**
```
Command: install_tool:nmap
Command: install_tool:gobuster
Command: install_tool:nikto
```

### **Report Generation**
```
Command: report_generation
```

### **Security Validation**
All commands are automatically validated for:
- Dangerous system operations
- Network attack patterns
- File system modifications
- Privilege escalation attempts

## 🎯 Best Practices

1. **Always obtain written authorization** before testing
2. **Review all commands** before execution
3. **Use isolated environments** for testing
4. **Follow responsible disclosure** for findings
5. **Document everything** for compliance
6. **Keep tools updated** for accuracy
7. **Validate findings manually** when possible

## 📈 Future Enhancements

- **Advanced Exploitation Modules**
- **Machine Learning Integration**
- **Custom Payload Generation**
- **Integration with CVE Databases**
- **Automated Report Templates**
- **Multi-Target Support**
- **Plugin Architecture**

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Follow security best practices

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

**⚠️ DISCLAIMER:** This tool is for authorized security testing only. Users are responsible for complying with applicable laws and obtaining proper authorization before testing any systems.

## How It Works

1.  **Initialization:** The agent starts, loads configurations, and initializes the connection to the Gemini LLM with specific system instructions that define its role as a penetration tester.
2.  **Objective Input:** The user provides a penetration testing objective (e.g., "Test example.com for web vulnerabilities," "Enumerate open ports and services on 192.168.1.100").
3.  **LLM Planning & Command Generation:** The LLM receives the objective and the current context (e.g., previous command outputs). It formulates a "thought" process (its reasoning) and a specific shell "command" to execute next.
4.  **User Approval (if enabled):** If command approval is active, the agent presents the LLM's suggested command to the user. The user can:
    *   Approve the command for execution.
    *   Reject the command.
    *   Reject the command and provide a specific message to the LLM to guide its next attempt.
5.  **Command Execution:** Approved commands are executed by the agent.
    *   On Windows, commands are typically run within the Windows Subsystem for Linux (WSL) to provide a Unix-like environment.
    *   On Linux/macOS, commands are run directly in the shell.
    *   `sudo` commands are handled (with a **strong warning about the insecurity of hardcoded passwords** if used).
6.  **Feedback Loop:** The `stdout`, `stderr`, and return code from the executed command are captured and sent back to the LLM as input for the next iteration.
7.  **Iteration:** Steps 3-6 are repeated. The LLM uses the feedback to adapt its strategy, try different approaches if previous commands failed, and work towards the initial objective.
8.  **Conclusion/Exit:** The process continues until:
    *   The LLM determines the objective is complete and issues an "exit" command with a final report.
    *   The LLM decides it cannot proceed further.
    *   The maximum number of iterations is reached.
    *   The user quits the agent.
9.  **Logging:** The entire session is logged to a file for later analysis.

## Project Structure

```
autopentest_project/
├── config.py # Configuration settings (API keys, LLM model, agent behavior)
├── gemini_llm_client.py # Handles communication with the Google Gemini LLM
├── command_executor.py # Responsible for executing shell commands
├── main_agent.py # Main orchestration logic for the agent
└── README.md # This file
```
*(Note: Additional files like `playwright_handler.py` might exist for extended browser automation capabilities, but are not detailed here as per request.)*

## Setup and Usage

### Prerequisites

*   Python 3.9+
*   `pip` (Python package installer)
*   Google Gemini API Key
*   (On Windows) Windows Subsystem for Linux (WSL) installed and configured if you intend to run Unix-like commands.

### Installation

1.  **Clone the repository (if applicable) or download the files.**
    ```bash
    # git clone <repository_url>
    # cd autopentest_project
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install google-generativeai
    ```
3.  **Configure API Key:**
    *   Set the `GEMINI_API_KEY` environment variable:
        *   Linux/macOS: `export GEMINI_API_KEY="YOUR_ACTUAL_API_KEY"`
        *   Windows (PowerShell): `$env:GEMINI_API_KEY="YOUR_ACTUAL_API_KEY"`
        *   Windows (CMD): `set GEMINI_API_KEY=YOUR_ACTUAL_API_KEY`
    *   Alternatively, you can modify `config.py` directly, but using environment variables is recommended for security.

4.  **Review Configuration (`config.py`):**
    *   `MODEL_NAME`: Ensure it's a valid Gemini model you have access to.
    *   `USER_COMMAND_APPROVAL`: Set to `True` (recommended for safety) or `False`.
    *   `SUDO_PASSWORD`: **EXTREMELY INSECURE if hardcoded.** For development in isolated environments only. Remove or use a secure alternative for any real use.
    *   Other agent settings like `MAX_ITERATIONS`.

### Running the Agent

Execute the main script:

```bash
python main_agent.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
```
The agent will then prompt you to enter your penetration testing objective.

Security Considerations

Command Execution: This tool executes commands generated by an LLM. While there are safety mechanisms like user approval, there's an inherent risk. Always review commands carefully before execution, especially if USER_COMMAND_APPROVAL is False or if operating in sensitive environments.

Sudo Password: Never hardcode sudo passwords in production or shared environments. The current implementation with a hardcoded SUDO_PASSWORD in config.py is a major security risk and is included only for specific, isolated development scenarios if explicitly configured. Prefer sudoers configurations for passwordless execution of specific commands for the agent's user, or manual password entry when sudo is invoked.

API Keys: Protect your GEMINI_API_KEY. Use environment variables or secure secret management solutions.

Scope of Testing: Only use this tool on systems and networks for which you have explicit, written authorization. Unauthorized penetration testing is illegal.

Future Enhancements (Potential Ideas)

More sophisticated tool integration beyond basic shell commands.

Enhanced context management and memory for the LLM.

Ability for the LLM to request specific information or files from the local system (with user approval).

Integration with vulnerability databases.

Automated report generation based on findings.

Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request if you'd like to contribute.
(Add details here if you have specific contribution guidelines)

License

(Specify your project's license here, e.g., MIT, Apache 2.0)

**Key aspects of this README:**

*   **Clear Disclaimer:** Emphasizes responsible and authorized use.
*   **Focus on Core Functionality:** Describes the LLM-driven shell command execution loop.
*   **Highlights User Control:** Mentions objective setting and command approval.
*   **Security Warnings:** Strongly advises against hardcoded passwords and emphasizes command review.
*   **Setup Instructions:** Provides basic steps to get the agent running.
*   **Omits Playwright Details:** As requested, it doesn't go into the specifics of browser automation commands like `PW_NAVIGATE`, keeping the focus on the shell-based interaction. I added a small note in the "Project Structure" section that other files *might* exist for such features, just as a placeholder.

You can adapt the "Future Enhancements," "Contributing," and "License" sections to better fit your project's status and goals.
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
