# autopentest_project/command_executor.py

import subprocess
import shlex
import json
from config import SUDO_PASSWORD, COMMAND_TIMEOUT_SECONDS, Colors, print_colored
from pentesting_tools import tools_manager
from custom_functions import custom_functions
from terminal_manager import terminal_manager
import platform

def execute_command(command: str, phase: str = "unknown", tool_category: str = "unknown", 
                   expected_outcome: str = "Unknown", run_in_terminal: bool = False) -> tuple[str, int, bool]:
    """
    Executes a shell command or custom function.
    Handles special commands like custom functions and tool installation.
    
    Args:
        command: Command to execute
        phase: Current pentesting phase
        tool_category: Category of tool being used
        expected_outcome: What we expect to achieve
        run_in_terminal: Whether to run in separate terminal window
    
    Special command formats:
    - custom_function:function_name:param1,param2,param3
    - install_tool:tool_name
    - report_generation
    - parallel_execute:command1;command2;command3
    - collect_results:task_id1,task_id2,task_id3
    """
    if not command:
        return "Error: No command to execute.", -1, False

    if command.strip().lower() == "exit":
        return "LLM requested exit, no shell command executed.", 0, False

    # Handle special commands
    if command.startswith("custom_function:"):
        return execute_custom_function(command)
    elif command.startswith("install_tool:"):
        return execute_tool_installation(command)
    elif command == "report_generation":
        return execute_report_generation()
    elif command.startswith("parallel_execute:"):
        return execute_parallel_commands(command, phase, tool_category, expected_outcome)
    elif command.startswith("collect_results:"):
        return collect_parallel_results(command)
    elif run_in_terminal:
        return execute_in_new_terminal(command, phase, tool_category, expected_outcome)
    else:
        return execute_shell_command(command)

def execute_parallel_commands(command: str, phase: str, tool_category: str, expected_outcome: str) -> tuple[str, int, bool]:
    """Execute multiple commands in parallel terminals."""
    try:
        commands = command.replace("parallel_execute:", "").split(";")
        task_ids = []
        
        print_colored(f"🚀 Launching {len(commands)} parallel tasks...", Colors.CYAN, bold=True)
        
        for cmd in commands:
            cmd = cmd.strip()
            if cmd:
                task_id = terminal_manager.launch_terminal_task(
                    command=cmd,
                    phase=phase,
                    tool_category=tool_category,
                    expected_outcome=expected_outcome
                )
                task_ids.append(task_id)
        
        result = {
            "parallel_execution": True,
            "task_ids": task_ids,
            "commands_launched": len(task_ids),
            "message": f"Launched {len(task_ids)} parallel tasks. Use 'collect_results:{','.join(task_ids)}' to gather results."
        }
        
        return json.dumps(result, indent=2), 0, False
        
    except Exception as e:
        error_msg = f"Error executing parallel commands: {str(e)}"
        print_colored(error_msg, Colors.RED)
        return error_msg, -1, False

def collect_parallel_results(command: str) -> tuple[str, int, bool]:
    """Collect results from parallel terminal executions."""
    try:
        task_ids = command.replace("collect_results:", "").split(",")
        task_ids = [tid.strip() for tid in task_ids if tid.strip()]
        
        print_colored(f"📊 Collecting results from {len(task_ids)} tasks...", Colors.CYAN, bold=True)
        
        # Wait for all tasks to complete
        completed_tasks = terminal_manager.wait_for_tasks(task_ids)
        
        # Get detailed results
        results = terminal_manager.get_task_results(task_ids)
        
        # Print summary
        terminal_manager.print_results_summary(results)
        
        # Return analysis
        analysis = terminal_manager.analyze_results(results)
        return json.dumps(analysis, indent=2), 0, False
        
    except Exception as e:
        error_msg = f"Error collecting parallel results: {str(e)}"
        print_colored(error_msg, Colors.RED)
        return error_msg, -1, False

def execute_in_new_terminal(command: str, phase: str, tool_category: str, expected_outcome: str) -> tuple[str, int, bool]:
    """Execute a single command in a new terminal window."""
    try:
        print_colored(f"🖥️  Launching command in new terminal...", Colors.CYAN, bold=True)
        
        task_id = terminal_manager.launch_terminal_task(
            command=command,
            phase=phase,
            tool_category=tool_category,
            expected_outcome=expected_outcome
        )
        
        # Wait for this task to complete
        completed_tasks = terminal_manager.wait_for_tasks([task_id])
        
        if completed_tasks:
            task = completed_tasks[0]
            return task.output, task.return_code or 0, False
        else:
            return "Task execution failed or timed out", -1, True
            
    except Exception as e:
        error_msg = f"Error executing in new terminal: {str(e)}"
        print_colored(error_msg, Colors.RED)
        return error_msg, -1, False

def execute_custom_function(command: str) -> tuple[str, int, bool]:
    """Execute custom pentesting functions."""
    try:
        parts = command.split(":")
        if len(parts) < 2:
            return "Error: Invalid custom function format. Use custom_function:function_name:params", -1, False
        
        function_name = parts[1]
        params = parts[2].split(",") if len(parts) > 2 and parts[2] else []
        
        print_colored(f"🔧 Executing custom function: {function_name}", Colors.CYAN, bold=True)
        
        # Map function names to actual functions
        function_map = {
            'port_scan_basic': lambda: custom_functions.port_scan_basic(
                params[0], [int(p) for p in params[1].split("-")] if len(params) > 1 else [22, 80, 443]
            ),
            'web_tech_detection': lambda: custom_functions.web_technology_detection(params[0]),
            'dns_enumeration': lambda: custom_functions.dns_enumeration(params[0]),
            'subdomain_enumeration': lambda: custom_functions.dns_enumeration(params[0]),  # Alias
            'whois_lookup': lambda: custom_functions.whois_lookup(params[0]),
            'vulnerability_check': lambda: custom_functions.vulnerability_check_basic(params[0]),
            'network_discovery': lambda: custom_functions.network_discovery(params[0])
        }
        
        if function_name not in function_map:
            available_functions = ", ".join(function_map.keys())
            return f"Error: Unknown function '{function_name}'. Available: {available_functions}", -1, False
        
        # Execute the function
        result = function_map[function_name]()
        formatted_result = json.dumps(result, indent=2, default=str)
        
        print_colored("✅ Custom function executed successfully", Colors.GREEN)
        return formatted_result, 0, False
        
    except Exception as e:
        error_msg = f"Error executing custom function: {str(e)}"
        print_colored(error_msg, Colors.RED)
        return error_msg, -1, False

def execute_tool_installation(command: str) -> tuple[str, int, bool]:
    """Handle tool installation requests."""
    try:
        tool_name = command.split(":")[1]
        print_colored(f"🔧 Installing pentesting tool: {tool_name}", Colors.CYAN, bold=True)
        
        success, message = tools_manager.install_tool(tool_name)
        return_code = 0 if success else -1
        
        return message, return_code, False
        
    except Exception as e:
        error_msg = f"Error installing tool: {str(e)}"
        print_colored(error_msg, Colors.RED)
        return error_msg, -1, False

def execute_report_generation() -> tuple[str, int, bool]:
    """Generate and save penetration testing report."""
    try:
        print_colored("📊 Generating penetration testing report...", Colors.CYAN, bold=True)
        
        # This would typically use collected findings from the session
        # For now, we'll create a basic structure
        findings = {
            'target': 'Session Target',
            'scan_date': 'Current Session',
            'vulnerabilities': [],
            'recommendations': ['Review all findings', 'Implement security controls'],
            'tools_used': ['AutoPentest AI Agent', 'Custom Functions']
        }
        
        report = custom_functions.generate_report(findings)
        
        # Save report to file
        with open("pentest_report.txt", "w") as f:
            f.write(report)
        
        print_colored("✅ Report generated and saved to pentest_report.txt", Colors.GREEN)
        return "Report generated successfully. Saved to pentest_report.txt", 0, False
        
    except Exception as e:
        error_msg = f"Error generating report: {str(e)}"
        print_colored(error_msg, Colors.RED)
        return error_msg, -1, False

def execute_shell_command(command: str) -> tuple[str, int, bool]:
    """
    Execute standard shell commands.
    Handles sudo with a hardcoded password (INSECURE).
    Handles WSL execution if on Windows.

    Returns:
        - output (str): Combined stdout and stderr of the command.
        - return_code (int): The exit code of the command.
        - timed_out (bool): True if the command timed out, False otherwise.
    """
    # !! SECURITY WARNING !! Hardcoded sudo password.
    # This is EXTREMELY DANGEROUS for real systems.
    processed_command = command
    if "sudo" in command:
        print_colored(
            "!! WARNING: Using sudo with a hardcoded password. This is a major security risk. !!",
            Colors.RED, bold=True
        )
        # Ensure sudo -S is used and the password is echoed
        # This basic replacement might not be robust for all sudo command structures.
        processed_command = command.replace("sudo ", f'echo "{SUDO_PASSWORD}" | sudo -S ')

    # Make apt non-interactive if present
    if "apt " in processed_command and " -y " not in processed_command:
        processed_command = processed_command.replace("apt ", "apt -y ")
    if "apt-get " in processed_command and " -y " not in processed_command:
        processed_command = processed_command.replace("apt-get ", "apt-get -y ")

    # Prepare command for execution (WSL or direct)
    system_platform = platform.system()
    if system_platform == "Windows":
        # Assuming bash commands are to be run in WSL
        cmd_list = ["wsl.exe", "-e", "bash", "-lc", processed_command]
        shell_to_print = processed_command
    elif system_platform == "Linux" or system_platform == "Darwin": # Linux or macOS
        # Execute directly. Using shell=True can be a security risk if `processed_command` is not sanitized.
        # However, LLM generates arbitrary commands, so `shell=True` is often necessary for pipes, etc.
        cmd_list = processed_command # Pass string to subprocess with shell=True
        shell_to_print = processed_command
    else:
        return f"Unsupported platform: {system_platform}", -1, False

    print_colored(f"\n[Executor] Running Command:", Colors.CYAN, bold=True)
    print_colored(f"  $ {shell_to_print}", Colors.LIGHTWHITE_EX)

    try:
        # For `shell=True` on Linux/macOS, cmd_list is a string.
        # For `wsl.exe`, cmd_list is a list of arguments.
        use_shell = True if system_platform != "Windows" else False

        process = subprocess.run(
            cmd_list,
            shell=use_shell, # Necessary for complex shell commands like pipes if not on WSL
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            check=False # Don't raise exception for non-zero exit codes
        )
        output = process.stdout + process.stderr # Combine stdout and stderr
        return_code = process.returncode
        timed_out = False

        print_colored(f"[Executor] Return Code: {return_code}", Colors.LIGHTBLACK_EX if return_code == 0 else Colors.LIGHTRED_EX)
        if output.strip():
            print_colored(f"[Executor] Output:", Colors.LIGHTBLACK_EX)
            # Indent output for clarity
            for line in output.strip().splitlines():
                print_colored(f"    {line}", Colors.LIGHTBLACK_EX)
        else:
            print_colored("[Executor] Output: <No output>", Colors.LIGHTBLACK_EX)


    except subprocess.TimeoutExpired:
        output = f"Error: Command '{shell_to_print}' timed out after {COMMAND_TIMEOUT_SECONDS} seconds."
        return_code = -100 # Special code for timeout
        timed_out = True
        print_colored(output, Colors.RED)
    except FileNotFoundError:
        # This could happen if wsl.exe is not found on Windows, or the command itself on Linux
        err_msg = f"Error: Command or interpreter not found. Ensure WSL is installed and in PATH if on Windows, or the command '{shlex.split(command)[0] if command else ''}' is installed."
        output = err_msg
        return_code = -101 # Special code for not found
        timed_out = False
        print_colored(output, Colors.RED)
    except Exception as e:
        output = f"Error executing command '{shell_to_print}': {str(e)}"
        return_code = -102 # Special code for other execution errors
        timed_out = False
        print_colored(output, Colors.RED)

    return output.strip(), return_code, timed_out
