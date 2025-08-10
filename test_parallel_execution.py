#!/usr/bin/env python3
"""
Test script to demonstrate multi-terminal parallel execution capabilities
"""

import time
import json
from command_executor import execute_command
from config import print_colored, Colors

def test_parallel_execution():
    """Test the parallel execution functionality"""
    print_colored("🧪 Testing Multi-Terminal Parallel Execution", Colors.CYAN, bold=True)
    print()
    
    # Test 1: Simple parallel commands
    print_colored("Test 1: Basic parallel execution", Colors.YELLOW, bold=True)
    parallel_cmd = "parallel_execute:echo 'Task 1: Network scan started'; sleep 3; echo 'Task 1: Complete';echo 'Task 2: Web scan started'; sleep 2; echo 'Task 2: Complete';echo 'Task 3: Service enum started'; sleep 4; echo 'Task 3: Complete'"
    
    result, code, error = execute_command(
        command=parallel_cmd,
        phase="testing",
        tool_category="test",
        expected_outcome="Parallel execution test"
    )
    
    print("Parallel execution result:")
    print(result)
    
    # Extract task IDs from result
    try:
        result_data = json.loads(result)
        task_ids = result_data.get("task_ids", [])
        
        if task_ids:
            print_colored(f"\n📊 Collecting results from {len(task_ids)} tasks...", Colors.CYAN)
            time.sleep(1)  # Brief pause
            
            # Collect results
            collect_cmd = f"collect_results:{','.join(task_ids)}"
            collect_result, collect_code, collect_error = execute_command(
                command=collect_cmd,
                phase="testing",
                tool_category="test",
                expected_outcome="Result collection"
            )
            
            print("Collection result:")
            print(collect_result)
        
    except json.JSONDecodeError:
        print_colored("❌ Could not parse parallel execution result", Colors.RED)
    
    print()
    print_colored("Test 2: Single terminal execution", Colors.YELLOW, bold=True)
    
    # Test 2: Single new terminal
    single_result, single_code, single_error = execute_command(
        command="echo 'Single terminal test'; date; echo 'Current directory:'; pwd",
        phase="testing", 
        tool_category="test",
        expected_outcome="Single terminal test",
        run_in_terminal=True
    )
    
    print("Single terminal result:")
    print(single_result)
    
    print()
    print_colored("✅ Multi-terminal testing complete!", Colors.GREEN, bold=True)

if __name__ == "__main__":
    test_parallel_execution()
