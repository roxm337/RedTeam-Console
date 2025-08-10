#!/usr/bin/env python3
"""
Multi-terminal execution manager for parallel pentesting operations
"""
import subprocess
import threading
import time
import uuid
import os
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from config import Colors, print_colored, COMMAND_TIMEOUT_SECONDS

@dataclass
class TerminalTask:
    """Represents a task running in a separate terminal."""
    task_id: str
    command: str
    phase: str
    tool_category: str
    expected_outcome: str
    start_time: float
    process: Optional[subprocess.Popen] = None
    output_file: Optional[str] = None
    status: str = "pending"  # pending, running, completed, failed, timeout
    return_code: Optional[int] = None
    output: str = ""
    error: str = ""
    execution_time: float = 0.0

class TerminalManager:
    """Manages multiple terminal windows for parallel command execution."""
    
    def __init__(self, results_dir: str = "terminal_results"):
        self.results_dir = results_dir
        self.active_tasks: Dict[str, TerminalTask] = {}
        self.completed_tasks: List[TerminalTask] = []
        self.max_parallel_tasks = 5
        
        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)
        
    def create_terminal_script(self, task: TerminalTask) -> str:
        """Create a script file for terminal execution."""
        script_content = f"""#!/bin/bash
# Pentesting Task: {task.task_id}
# Command: {task.command}
# Phase: {task.phase}
# Tool Category: {task.tool_category}

echo "🚀 Starting Task: {task.task_id}"
echo "📋 Command: {task.command}"
echo "🔍 Phase: {task.phase}"
echo "🛠️  Tool: {task.tool_category}"
echo "🎯 Expected: {task.expected_outcome}"
echo "⏰ Started: $(date)"
echo "=================================="
echo ""

# Change to project directory
cd "{os.getcwd()}"

# Execute the command and capture output
start_time=$(date +%s)
echo "Output:" > "{task.output_file}"
echo "======" >> "{task.output_file}"

# Run the actual command
{task.command} >> "{task.output_file}" 2>&1
exit_code=$?

end_time=$(date +%s)
execution_time=$((end_time - start_time))

echo "" >> "{task.output_file}"
echo "=================================" >> "{task.output_file}"
echo "Exit Code: $exit_code" >> "{task.output_file}"
echo "Execution Time: ${{execution_time}}s" >> "{task.output_file}"
echo "Completed: $(date)" >> "{task.output_file}"

echo ""
echo "🏁 Task Completed!"
echo "📊 Exit Code: $exit_code"
echo "⏱️  Execution Time: ${{execution_time}}s"
echo "📁 Results saved to: {task.output_file}"
echo ""

if [ $exit_code -eq 0 ]; then
    echo "✅ Task completed successfully"
else
    echo "❌ Task failed with exit code $exit_code"
fi

echo ""
echo "Press Enter to close terminal..."
read
exit $exit_code
"""
        
        script_file = f"{self.results_dir}/script_{task.task_id}.sh"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        # Make script executable
        os.chmod(script_file, 0o755)
        return script_file
    
    def launch_terminal_task(self, command: str, phase: str, tool_category: str, 
                           expected_outcome: str) -> str:
        """Launch a command in a new terminal window."""
        task_id = str(uuid.uuid4())[:8]
        output_file = f"{self.results_dir}/output_{task_id}.txt"
        
        task = TerminalTask(
            task_id=task_id,
            command=command,
            phase=phase,
            tool_category=tool_category,
            expected_outcome=expected_outcome,
            start_time=time.time(),
            output_file=output_file
        )
        
        # Create terminal script
        script_file = self.create_terminal_script(task)
        
        try:
            # Launch in new terminal based on OS
            system = os.uname().sysname.lower()
            
            if system == "darwin":  # macOS
                terminal_cmd = [
                    "osascript", "-e",
                    f'tell application "Terminal" to do script "bash {script_file}"'
                ]
            elif system == "linux":
                # Try different terminal emulators
                terminal_emulators = ["gnome-terminal", "xterm", "konsole", "terminator"]
                terminal_cmd = None
                
                for emulator in terminal_emulators:
                    if subprocess.run(["which", emulator], capture_output=True).returncode == 0:
                        if emulator == "gnome-terminal":
                            terminal_cmd = ["gnome-terminal", "--", "bash", script_file]
                        elif emulator == "xterm":
                            terminal_cmd = ["xterm", "-e", f"bash {script_file}"]
                        elif emulator == "konsole":
                            terminal_cmd = ["konsole", "-e", f"bash {script_file}"]
                        elif emulator == "terminator":
                            terminal_cmd = ["terminator", "-e", f"bash {script_file}"]
                        break
                
                if not terminal_cmd:
                    raise Exception("No suitable terminal emulator found")
            else:
                raise Exception(f"Unsupported operating system: {system}")
            
            # Launch the terminal
            process = subprocess.Popen(terminal_cmd)
            task.process = process
            task.status = "running"
            
            self.active_tasks[task_id] = task
            
            print_colored(f"🚀 Launched Task {task_id} in new terminal", Colors.GREEN, bold=True)
            print_colored(f"   📋 Command: {command}", Colors.LIGHTWHITE_EX)
            print_colored(f"   🔍 Phase: {phase}", Colors.LIGHTCYAN_EX)
            print_colored(f"   📁 Results: {output_file}", Colors.LIGHTBLACK_EX)
            
            return task_id
            
        except Exception as e:
            print_colored(f"❌ Failed to launch terminal for task {task_id}: {e}", Colors.RED)
            task.status = "failed"
            task.error = str(e)
            self.completed_tasks.append(task)
            return task_id
    
    def check_task_status(self, task_id: str) -> Optional[TerminalTask]:
        """Check the status of a running task."""
        if task_id not in self.active_tasks:
            return None
        
        task = self.active_tasks[task_id]
        
        # Check if output file exists and has content
        if os.path.exists(task.output_file):
            try:
                with open(task.output_file, 'r') as f:
                    content = f.read()
                    
                # Check if task is completed (contains exit code)
                if "Exit Code:" in content:
                    task.status = "completed"
                    task.execution_time = time.time() - task.start_time
                    
                    # Extract exit code
                    lines = content.split('\n')
                    for line in lines:
                        if line.startswith("Exit Code:"):
                            task.return_code = int(line.split(":")[1].strip())
                            break
                    
                    task.output = content
                    
                    # Move to completed tasks
                    del self.active_tasks[task_id]
                    self.completed_tasks.append(task)
                    
                    print_colored(f"✅ Task {task_id} completed", Colors.GREEN)
                    return task
                    
            except Exception as e:
                print_colored(f"⚠️  Error reading output for task {task_id}: {e}", Colors.YELLOW)
        
        # Check for timeout
        if time.time() - task.start_time > COMMAND_TIMEOUT_SECONDS:
            task.status = "timeout"
            task.execution_time = time.time() - task.start_time
            
            # Try to terminate the process
            if task.process:
                try:
                    task.process.terminate()
                except:
                    pass
            
            del self.active_tasks[task_id]
            self.completed_tasks.append(task)
            
            print_colored(f"⏰ Task {task_id} timed out", Colors.YELLOW)
            return task
        
        return task
    
    def wait_for_tasks(self, task_ids: List[str], check_interval: float = 2.0) -> List[TerminalTask]:
        """Wait for specific tasks to complete."""
        print_colored(f"⏳ Waiting for {len(task_ids)} tasks to complete...", Colors.CYAN, bold=True)
        
        completed = []
        remaining_tasks = set(task_ids)
        
        while remaining_tasks:
            for task_id in list(remaining_tasks):
                task = self.check_task_status(task_id)
                if task and task.status in ["completed", "failed", "timeout"]:
                    completed.append(task)
                    remaining_tasks.remove(task_id)
            
            if remaining_tasks:
                active_count = len([t for t in remaining_tasks if t in self.active_tasks])
                print_colored(f"📊 {active_count} tasks still running...", Colors.LIGHTBLACK_EX)
                time.sleep(check_interval)
        
        print_colored(f"🏁 All {len(task_ids)} tasks completed!", Colors.GREEN, bold=True)
        return completed
    
    def get_task_results(self, task_ids: List[str]) -> Dict[str, Dict]:
        """Get results from completed tasks."""
        results = {}
        
        for task_id in task_ids:
            # Check completed tasks
            for task in self.completed_tasks:
                if task.task_id == task_id:
                    results[task_id] = {
                        "command": task.command,
                        "phase": task.phase,
                        "tool_category": task.tool_category,
                        "expected_outcome": task.expected_outcome,
                        "status": task.status,
                        "return_code": task.return_code,
                        "execution_time": task.execution_time,
                        "output": task.output,
                        "error": task.error
                    }
                    break
        
        return results
    
    def analyze_results(self, results: Dict[str, Dict]) -> Dict:
        """Analyze results from multiple tasks."""
        analysis = {
            "total_tasks": len(results),
            "successful_tasks": 0,
            "failed_tasks": 0,
            "timeout_tasks": 0,
            "total_execution_time": 0,
            "findings": [],
            "recommendations": [],
            "summary": ""
        }
        
        for task_id, result in results.items():
            analysis["total_execution_time"] += result.get("execution_time", 0)
            
            if result["status"] == "completed" and result.get("return_code") == 0:
                analysis["successful_tasks"] += 1
            elif result["status"] == "timeout":
                analysis["timeout_tasks"] += 1
            else:
                analysis["failed_tasks"] += 1
            
            # Analyze output for findings
            output = result.get("output", "")
            if output:
                # Look for common pentesting findings
                if "open" in output.lower() and "port" in output.lower():
                    analysis["findings"].append(f"Open ports discovered by {result['command']}")
                
                if "vulnerable" in output.lower():
                    analysis["findings"].append(f"Potential vulnerability found by {result['command']}")
                
                if "sql injection" in output.lower():
                    analysis["findings"].append(f"SQL injection indicators found by {result['command']}")
        
        # Generate summary
        success_rate = (analysis["successful_tasks"] / analysis["total_tasks"]) * 100
        analysis["summary"] = f"Executed {analysis['total_tasks']} tasks with {success_rate:.1f}% success rate. Found {len(analysis['findings'])} potential findings."
        
        return analysis
    
    def print_results_summary(self, results: Dict[str, Dict]):
        """Print a formatted summary of results."""
        analysis = self.analyze_results(results)
        
        print_colored("\n" + "="*60, Colors.CYAN, bold=True)
        print_colored("           PARALLEL EXECUTION RESULTS", Colors.CYAN, bold=True)
        print_colored("="*60, Colors.CYAN, bold=True)
        
        print_colored(f"\n📊 Execution Summary:", Colors.YELLOW, bold=True)
        print_colored(f"   Total Tasks: {analysis['total_tasks']}", Colors.LIGHTWHITE_EX)
        print_colored(f"   ✅ Successful: {analysis['successful_tasks']}", Colors.GREEN)
        print_colored(f"   ❌ Failed: {analysis['failed_tasks']}", Colors.RED)
        print_colored(f"   ⏰ Timeout: {analysis['timeout_tasks']}", Colors.YELLOW)
        print_colored(f"   ⏱️  Total Time: {analysis['total_execution_time']:.1f}s", Colors.LIGHTBLUE_EX)
        
        if analysis['findings']:
            print_colored(f"\n🔍 Key Findings ({len(analysis['findings'])}):", Colors.GREEN, bold=True)
            for finding in analysis['findings']:
                print_colored(f"   • {finding}", Colors.LIGHTGREEN_EX)
        
        print_colored(f"\n📝 Summary:", Colors.LIGHTBLUE_EX, bold=True)
        print_colored(f"   {analysis['summary']}", Colors.LIGHTWHITE_EX)
        
        # Detailed task results
        print_colored(f"\n📋 Task Details:", Colors.LIGHTMAGENTA_EX, bold=True)
        for task_id, result in results.items():
            status_color = Colors.GREEN if result['status'] == 'completed' and result.get('return_code') == 0 else Colors.RED
            status_icon = "✅" if result['status'] == 'completed' and result.get('return_code') == 0 else "❌"
            
            print_colored(f"\n   {status_icon} Task {task_id}:", status_color, bold=True)
            print_colored(f"      Command: {result['command']}", Colors.LIGHTWHITE_EX)
            print_colored(f"      Phase: {result['phase']}", Colors.LIGHTCYAN_EX)
            print_colored(f"      Status: {result['status']}", status_color)
            print_colored(f"      Time: {result['execution_time']:.1f}s", Colors.LIGHTBLUE_EX)
            
            if result.get('output'):
                # Show first few lines of output
                output_lines = result['output'].split('\n')[:3]
                print_colored(f"      Output Preview:", Colors.LIGHTBLACK_EX)
                for line in output_lines:
                    if line.strip():
                        print_colored(f"        {line[:80]}{'...' if len(line) > 80 else ''}", Colors.LIGHTBLACK_EX)

# Global terminal manager instance
terminal_manager = TerminalManager()
