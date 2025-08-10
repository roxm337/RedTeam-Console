#!/usr/bin/env python3
"""
Updated Command Executor with Working Multi-Terminal Support
This version uses proven parallel execution that actually works
"""

import subprocess
import shlex
import json
import time
import os
import threading
from typing import Union, Dict, Any, List, Optional, Tuple
from config import SUDO_PASSWORD, COMMAND_TIMEOUT_SECONDS, Colors, print_colored
from pentesting_tools import tools_manager
from custom_functions import custom_functions
from security_validator import CommandValidator
from enhanced_logger import EnhancedLogger
from wordlist_manager import wordlist_manager
from session_manager import session_manager

# Initialize components
security_validator = CommandValidator()
logger = EnhancedLogger()

class ParallelExecutor:
    """Handles parallel command execution with real results"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.getcwd()
        # Use session manager's results directory
        self.results_dir = session_manager.results_dir
        os.makedirs(self.results_dir, exist_ok=True)
        self.active_tasks = {}
    
    def execute_parallel_commands(self, commands: List[str], phase: str, tool_category: str, expected_outcome: str) -> Dict:
        """Execute multiple commands in parallel and return results"""
        
        print_colored(f"🚀 Launching {len(commands)} parallel tasks...", Colors.CYAN, bold=True)
        
        processes = []
        task_ids = []
        start_time = time.time()
        
        # Launch all commands in parallel
        for i, cmd in enumerate(commands):
            if not cmd.strip():
                continue
                
            task_id = f"task_{int(time.time() * 1000)}_{i}"
            task_ids.append(task_id)
            
            output_file = os.path.join(self.results_dir, f"{task_id}_output.txt")
            
            print_colored(f"   📋 Task {task_id}: {cmd[:60]}...", Colors.YELLOW)
            
            # Launch process with output redirection
            with open(output_file, 'w') as f:
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=self.base_dir
                )
            
            self.active_tasks[task_id] = {
                'process': process,
                'command': cmd,
                'output_file': output_file,
                'start_time': start_time,
                'phase': phase,
                'tool_category': tool_category
            }
            processes.append((process, task_id))
        
        # Wait for all processes to complete
        print_colored(f"\n⏳ Waiting for {len(processes)} tasks to complete...", Colors.CYAN)
        
        results = []
        for process, task_id in processes:
            return_code = process.wait()
            end_time = time.time()
            execution_time = end_time - start_time
            
            task_info = self.active_tasks[task_id]
            
            # Read output
            try:
                with open(task_info['output_file'], 'r') as f:
                    output = f.read()
            except:
                output = "Error reading output"
            
            result = {
                'task_id': task_id,
                'command': task_info['command'],
                'return_code': return_code,
                'execution_time': execution_time,
                'output': output,
                'output_file': task_info['output_file'],
                'phase': phase,
                'tool_category': tool_category,
                'status': 'success' if return_code == 0 else 'failed'
            }
            
            results.append(result)
        
        total_time = time.time() - start_time
        
        # Clean up
        for task_id in task_ids:
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
        
        return {
            'total_tasks': len(results),
            'successful_tasks': sum(1 for r in results if r['status'] == 'success'),
            'failed_tasks': sum(1 for r in results if r['status'] == 'failed'),
            'total_execution_time': total_time,
            'results': results,
            'task_ids': task_ids
        }
    
    def analyze_results(self, parallel_result: Dict) -> Dict:
        """Analyze parallel execution results for security findings"""
        
        findings = []
        recommendations = []
        
        for result in parallel_result['results']:
            if result['status'] == 'success' and result['output']:
                output = result['output'].lower()
                
                # Analyze different tool outputs
                if 'nmap' in result['command']:
                    if 'open' in output:
                        findings.append(f"Open ports detected: {result['command']}")
                    if 'filtered' in output:
                        findings.append(f"Filtered ports found: {result['command']}")
                
                elif 'curl' in result['command'] or 'wget' in result['command']:
                    if 'server:' in output:
                        findings.append(f"Web server information disclosed: {result['command']}")
                    if 'x-powered-by:' in output:
                        findings.append(f"Technology stack revealed: {result['command']}")
                
                elif 'nikto' in result['command']:
                    if 'vulnerability' in output or 'vuln' in output:
                        findings.append(f"Web vulnerabilities detected: {result['command']}")
                
                elif 'gobuster' in result['command'] or 'dirb' in result['command']:
                    if 'status: 200' in output or 'found' in output:
                        findings.append(f"Hidden directories/files discovered: {result['command']}")
                
                elif 'dig' in result['command'] or 'nslookup' in result['command']:
                    if 'mx' in output or 'ns' in output or 'txt' in output:
                        findings.append(f"DNS records enumerated: {result['command']}")
        
        # Generate recommendations based on findings
        if any('open ports' in f for f in findings):
            recommendations.append("Review open ports and disable unnecessary services")
        
        if any('server information' in f for f in findings):
            recommendations.append("Configure web server to hide version information")
        
        if any('vulnerabilities' in f for f in findings):
            recommendations.append("Prioritize patching identified web vulnerabilities")
        
        return {
            'findings': findings,
            'recommendations': recommendations,
            'analysis_summary': f"Found {len(findings)} potential security issues across {parallel_result['total_tasks']} tasks"
        }

# Global parallel executor instance
parallel_executor = ParallelExecutor()

def execute_command(command: str, phase: str = "unknown", tool_category: str = "unknown", 
                   expected_outcome: str = "Unknown", run_in_terminal: bool = False) -> tuple[str, int, bool]:
    """
    Enhanced command executor with parallel execution support
    """
    
    # Log the execution attempt (simplified)
    try:
        logger.log_security_event("command_execution", command, f"Phase: {phase}, Category: {tool_category}")
    except:
        pass  # Continue if logging fails
    
    # Security validation
    if not security_validator.validate_command(command):
        error_msg = "🚫 Command blocked by security validator"
        print_colored(error_msg, Colors.RED)
        return error_msg, -1, True
    
    # Update command with correct wordlist paths
    command = wordlist_manager.update_command_with_wordlist(command)
    
    # Handle parallel execution commands
    if command.startswith("parallel_execute:"):
        commands_str = command.replace("parallel_execute:", "").strip()
        commands = [cmd.strip() for cmd in commands_str.split(";") if cmd.strip()]
        
        if not commands:
            return "No valid commands provided for parallel execution", -1, True
        
        # Execute in parallel
        parallel_result = parallel_executor.execute_parallel_commands(
            commands, phase, tool_category, expected_outcome
        )
        
        # Print summary
        print_colored(f"\n🏁 Parallel execution completed!", Colors.GREEN, bold=True)
        print_colored(f"📊 Results: {parallel_result['successful_tasks']}/{parallel_result['total_tasks']} successful", Colors.CYAN)
        print_colored(f"⏱️  Total time: {parallel_result['total_execution_time']:.2f}s", Colors.CYAN)
        
        # Analyze results
        analysis = parallel_executor.analyze_results(parallel_result)
        
        if analysis['findings']:
            print_colored("\n🎯 SECURITY FINDINGS:", Colors.RED, bold=True)
            for finding in analysis['findings']:
                print_colored(f"   • {finding}", Colors.YELLOW)
        
        if analysis['recommendations']:
            print_colored("\n💡 RECOMMENDATIONS:", Colors.BLUE, bold=True)
            for rec in analysis['recommendations']:
                print_colored(f"   • {rec}", Colors.CYAN)
        
        # Return combined results
        return json.dumps({
            'parallel_execution': True,
            'summary': parallel_result,
            'analysis': analysis
        }, indent=2), 0, False
    
    # Handle result collection commands  
    if command.startswith("collect_results:"):
        # This is mainly for compatibility - results are collected automatically above
        return json.dumps({
            'message': 'Results are collected automatically in parallel execution',
            'results_dir': parallel_executor.results_dir
        }, indent=2), 0, False
    
    # Handle single terminal execution
    if run_in_terminal:
        print_colored(f"🖥️  Executing in separate process: {command}", Colors.CYAN)
        
        task_id = f"single_{int(time.time() * 1000)}"
        output_file = os.path.join(parallel_executor.results_dir, f"{task_id}_output.txt")
        
        start_time = time.time()
        
        # Execute and wait for completion
        with open(output_file, 'w') as f:
            result = subprocess.run(
                command,
                shell=True,
                stdout=f,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=COMMAND_TIMEOUT_SECONDS,
                cwd=parallel_executor.base_dir
            )
        
        execution_time = time.time() - start_time
        
        # Read output
        try:
            with open(output_file, 'r') as f:
                output = f.read()
        except:
            output = "Error reading output"
        
        print_colored(f"✅ Command completed in {execution_time:.2f}s", Colors.GREEN)
        return output, result.returncode, False
    
    # Handle custom functions
    if command.startswith("custom_function:"):
        function_name = command.replace("custom_function:", "").strip()
        return execute_custom_function(function_name)
    
    # Standard execution for non-parallel commands
    try:
        print_colored(f"🔄 Executing: {command}", Colors.YELLOW)
        
        # Determine if sudo is needed
        needs_sudo = any(cmd in command for cmd in ['nmap', 'masscan', 'tcpdump'])
        
        if needs_sudo and SUDO_PASSWORD:
            # Execute with sudo using echo for password input
            full_command = f"echo '{SUDO_PASSWORD}' | sudo -S {command}"
        else:
            full_command = command
        
        # Execute command
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
            cwd=parallel_executor.base_dir
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]: {result.stderr}"
        
        # Log result (simplified)
        try:
            logger.log_security_event("command_result", command, f"Return code: {result.returncode}, Output length: {len(output)}")
        except:
            pass
        
        if result.returncode == 0:
            print_colored(f"✅ Command successful", Colors.GREEN)
        else:
            print_colored(f"❌ Command failed with code {result.returncode}", Colors.RED)
        
        return output, result.returncode, result.returncode != 0
        
    except subprocess.TimeoutExpired:
        error_msg = f"⏰ Command timed out after {COMMAND_TIMEOUT_SECONDS} seconds"
        print_colored(error_msg, Colors.RED)
        return error_msg, -1, True
        
    except Exception as e:
        error_msg = f"💥 Execution error: {str(e)}"
        print_colored(error_msg, Colors.RED)
        return error_msg, -1, True

def execute_custom_function(function_name: str) -> tuple[str, int, bool]:
    """Execute a custom pentesting function"""
    try:
        if function_name in custom_functions:
            print_colored(f"🔧 Executing custom function: {function_name}", Colors.CYAN)
            result = custom_functions[function_name]()
            print_colored(f"✅ Custom function completed", Colors.GREEN)
            return str(result), 0, False
        else:
            available_functions = ", ".join(custom_functions.keys())
            error_msg = f"❌ Custom function '{function_name}' not found. Available: {available_functions}"
            print_colored(error_msg, Colors.RED)
            return error_msg, -1, True
            
    except Exception as e:
        error_msg = f"💥 Custom function error: {str(e)}"
        print_colored(error_msg, Colors.RED)
        return error_msg, -1, True

def get_parallel_results_summary() -> str:
    """Get a summary of recent parallel execution results"""
    try:
        results_files = []
        for file in os.listdir(parallel_executor.results_dir):
            if file.endswith('_output.txt'):
                file_path = os.path.join(parallel_executor.results_dir, file)
                stat = os.stat(file_path)
                results_files.append((file, stat.st_mtime))
        
        # Sort by modification time (newest first)
        results_files.sort(key=lambda x: x[1], reverse=True)
        
        summary = f"📊 Recent Parallel Execution Results ({len(results_files)} files):\n"
        
        for file, mtime in results_files[:10]:  # Show last 10 results
            file_path = os.path.join(parallel_executor.results_dir, file)
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    size = len(content)
                    preview = content[:100] + "..." if len(content) > 100 else content
                
                summary += f"\n📁 {file} ({size} bytes)\n   Preview: {preview.strip()}\n"
            except:
                summary += f"\n📁 {file} (Error reading file)\n"
        
        return summary
        
    except Exception as e:
        return f"Error reading parallel results: {str(e)}"

# Export main function for compatibility
__all__ = ['execute_command', 'execute_custom_function', 'get_parallel_results_summary', 'parallel_executor']
