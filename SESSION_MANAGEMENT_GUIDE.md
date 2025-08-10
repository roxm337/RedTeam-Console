# 🤖 AI Pentester Agent - Session Management Guide

## 🚀 Quick Start

### Starting a New Session
```bash
# Start with interactive menu
python3 main_with_sessions.py --interactive

# Auto-start new session and begin pentesting
python3 main_with_sessions.py --auto-start

# Start named session
python3 main_with_sessions.py --new-session "Web_App_Assessment"
```

## 📁 Session Organization

Your pentesting sessions are automatically organized in clean directory structures:

```
AI-Pentester-Agent/
├── sessions/                    # Archived sessions
│   ├── session_20240806_143022_Web_App_Test/
│   │   ├── session_data/       # Session files & notes
│   │   ├── results/            # Tool outputs & findings
│   │   ├── logs/               # Command logs & security events
│   │   ├── session_summary.json
│   │   └── README.md
│   └── session_20240806_150315_Network_Scan/
├── current_session/            # Active session data
├── results/                    # Current results
├── logs/                       # Current logs
└── main_with_sessions.py       # Enhanced entry point
```

## 🛠️ Key Features

### ✅ **Automatic Session Management**
- **Auto-archive**: Previous sessions are automatically saved when starting new ones
- **Clean workspace**: Each new session starts with clean results and logs directories
- **Organized storage**: Sessions are saved with timestamps and optional names

### ✅ **Session Operations**
```bash
# List recent sessions
python3 main_with_sessions.py --list-sessions

# Restore a previous session
python3 main_with_sessions.py --restore session_20240806_143022_Web_App_Test

# Clean old sessions (older than 30 days)
python3 main_with_sessions.py --clean-old 30
```

### ✅ **Integrated Tool Support**
- All pentesting tools automatically save outputs to session directories
- Wordlist manager integrated with session paths
- Command executor logs everything to session logs
- Parallel execution results organized by session

### ✅ **Session Metadata**
Each session includes:
- **Start/end timestamps**
- **Duration tracking** 
- **File counts and sizes**
- **Tools used**
- **Targets assessed**
- **Phases completed**
- **Readable summary** (README.md)

## 🎯 Usage Examples

### Example 1: Web Application Assessment
```bash
# Start named session
python3 main_with_sessions.py --new-session "WebApp_Target_com"

# Your pentesting will automatically:
# - Save nmap results to results/nmap_scan.txt
# - Save gobuster findings to results/gobuster_dirs.txt  
# - Log all commands to logs/commands.log
# - Store session notes in current_session/
```

### Example 2: Network Penetration Test
```bash
# Auto-start and begin
python3 main_with_sessions.py --auto-start

# All results organized automatically:
# - Network discovery → results/network_discovery/
# - Vulnerability scans → results/vuln_scans/
# - Exploitation logs → logs/exploitation.log
```

### Example 3: Session Management
```bash
# Interactive menu for full control
python3 main_with_sessions.py --interactive

# Options include:
# 1. Start New Session
# 2. List Recent Sessions  
# 3. Restore Previous Session
# 4. Show Session Status
# 5. Clean Old Sessions
# 6. Start Pentesting
```

## 📊 Session Statistics

Monitor your pentesting activities:
```bash
# View current stats
python3 session_manager.py

# Shows:
# - Total sessions: 15
# - Current session files: 23
# - Total archived files: 342
# - Disk usage: 45.2 MB
```

## 🧹 Cleanup & Maintenance

### Automatic Cleanup
- **New sessions**: Automatically archive previous session
- **Clean workspace**: Remove old results/logs for fresh start  
- **Organized archives**: Sessions saved with full metadata

### Manual Cleanup
```bash
# Remove sessions older than 30 days (keep minimum 5)
python3 main_with_sessions.py --clean-old 30

# Or use interactive cleanup
python3 main_with_sessions.py --interactive
# → Select option 5: Clean Old Sessions
```

## 🔧 Integration with Existing Tools

### Command Executor Integration
- All `execute_command()` calls automatically save to session directories
- Parallel execution results organized by session
- Real-time logging to session logs directory

### Wordlist Manager Integration  
- Wordlists automatically managed per session
- Custom wordlist directory: `/Users/roxm1337/BHSrOxM/wordlist/`
- Tool-specific wordlist mapping maintained

### Enhanced Logger Integration
- Session-specific log files
- Security event tracking per session
- Structured logging with metadata

## 🎉 Benefits

1. **🔄 Never lose work**: Every session automatically archived
2. **🧹 Clean workspace**: Each session starts fresh  
3. **📋 Full traceability**: Complete audit trail of all activities
4. **🔍 Easy review**: Organized results easy to review later
5. **⚡ Quick restart**: Restore any previous session instantly
6. **📊 Progress tracking**: Monitor your pentesting history
7. **🛡️ Compliance ready**: Structured logs for reporting

## 💡 Tips

- **Use descriptive names**: `python3 main_with_sessions.py --new-session "ClientName_WebApp_Phase1"`
- **Regular cleanup**: Clean old sessions monthly to save disk space
- **Review sessions**: Use `--list-sessions` to review recent work  
- **Restore when needed**: Continue previous assessments with `--restore`
- **Interactive mode**: Use `--interactive` for full control

---

Your pentesting sessions are now fully managed! 🎯 No more lost results, cluttered directories, or missing logs. Every session is captured, organized, and ready for review or continuation.
