#!/usr/bin/env python3
"""
Simple Multi-Terminal Test - Direct execution for testing
"""

import subprocess
import time
import os
from config import print_colored, Colors

def run_simple_parallel_test():
    """Test parallel execution with direct subprocess calls"""
    print_colored("🧪 Simple Multi-Terminal Test", Colors.CYAN, bold=True)
    print()
    
    # Create results directory
    results_dir = "/Users/roxm1337/projets/AI-Pentester-Agent/simple_results"
    os.makedirs(results_dir, exist_ok=True)
    
    # Simple test commands
    commands = [
        ("echo 'Task 1: Network scan started'", "task1.txt"),
        ("sleep 2 && echo 'Task 2: Web scan complete'", "task2.txt"),
        ("date && echo 'Task 3: System info'", "task3.txt"),
        ("echo 'Task 4: DNS lookup' && dig google.com", "task4.txt"),
    ]
    
    processes = []
    start_time = time.time()
    
    print_colored("🚀 Launching parallel tasks...", Colors.CYAN)
    
    # Launch all commands in parallel
    for i, (cmd, output_file) in enumerate(commands, 1):
        output_path = os.path.join(results_dir, output_file)
        print_colored(f"   📋 Task {i}: {cmd[:50]}...", Colors.YELLOW)
        
        # Run command and redirect output to file
        with open(output_path, 'w') as f:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=f,
                stderr=subprocess.STDOUT,
                text=True
            )
            processes.append((process, cmd, output_file, output_path))
    
    print_colored(f"\n⏳ Waiting for {len(processes)} tasks to complete...", Colors.CYAN)
    
    # Wait for all processes to complete
    results = []
    for process, cmd, output_file, output_path in processes:
        return_code = process.wait()
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Read output
        try:
            with open(output_path, 'r') as f:
                output = f.read()
        except:
            output = "Error reading output"
        
        results.append({
            'command': cmd,
            'return_code': return_code,
            'execution_time': execution_time,
            'output': output,
            'output_file': output_file
        })
    
    total_time = time.time() - start_time
    
    print_colored(f"\n🏁 All tasks completed in {total_time:.2f}s", Colors.GREEN, bold=True)
    print()
    
    # Display results
    print_colored("📊 RESULTS SUMMARY", Colors.CYAN, bold=True)
    print("=" * 60)
    
    successful = 0
    for i, result in enumerate(results, 1):
        status = "✅ SUCCESS" if result['return_code'] == 0 else "❌ FAILED"
        if result['return_code'] == 0:
            successful += 1
            
        print_colored(f"Task {i}: {status}", Colors.GREEN if result['return_code'] == 0 else Colors.RED)
        print(f"   Command: {result['command']}")
        print(f"   Time: {result['execution_time']:.2f}s")
        print(f"   Output preview: {result['output'][:100]}...")
        print()
    
    print_colored(f"📈 Success Rate: {successful}/{len(results)} ({successful/len(results)*100:.1f}%)", Colors.GREEN, bold=True)
    print_colored(f"⏱️  Total Time: {total_time:.2f}s", Colors.CYAN)
    print_colored(f"📁 Results saved to: {results_dir}/", Colors.YELLOW)
    
    return results

def test_real_pentesting():
    """Test with real pentesting commands"""
    print_colored("\n🎯 Real Pentesting Parallel Test", Colors.CYAN, bold=True)
    print()
    
    target = "testphp.vulnweb.com"
    results_dir = "/Users/roxm1337/projets/AI-Pentester-Agent/pentest_results" 
    os.makedirs(results_dir, exist_ok=True)
    
    # Real pentesting commands (safe testing target)
    commands = [
        (f"nmap -sS -T4 -p 80,443 {target}", "nmap_scan.txt"),
        (f"curl -I http://{target}", "http_headers.txt"),
        (f"dig {target} ANY", "dns_lookup.txt"),
        (f"whois {target}", "whois_info.txt"),
    ]
    
    processes = []
    start_time = time.time()
    
    print_colored(f"🔍 Target: {target}", Colors.YELLOW)
    print_colored("🚀 Launching pentesting tasks...", Colors.CYAN)
    
    # Launch all commands in parallel
    for i, (cmd, output_file) in enumerate(commands, 1):
        output_path = os.path.join(results_dir, output_file)
        print_colored(f"   📋 Task {i}: {cmd}", Colors.YELLOW)
        
        with open(output_path, 'w') as f:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=f,
                stderr=subprocess.STDOUT,
                text=True
            )
            processes.append((process, cmd, output_file, output_path))
    
    print_colored(f"\n⏳ Waiting for {len(processes)} pentesting tasks...", Colors.CYAN)
    
    # Wait and collect results
    results = []
    for process, cmd, output_file, output_path in processes:
        return_code = process.wait()
        end_time = time.time()
        execution_time = end_time - start_time
        
        try:
            with open(output_path, 'r') as f:
                output = f.read()
        except:
            output = "Error reading output"
        
        results.append({
            'command': cmd,
            'return_code': return_code,
            'execution_time': execution_time,
            'output': output,
            'output_file': output_file
        })
    
    total_time = time.time() - start_time
    
    print_colored(f"\n🏁 Pentesting completed in {total_time:.2f}s", Colors.GREEN, bold=True)
    print()
    
    # Analyze results
    print_colored("🔍 PENTESTING ANALYSIS", Colors.CYAN, bold=True)
    print("=" * 60)
    
    findings = []
    for i, result in enumerate(results, 1):
        status = "✅ SUCCESS" if result['return_code'] == 0 else "❌ FAILED"
        
        print_colored(f"Task {i}: {status}", Colors.GREEN if result['return_code'] == 0 else Colors.RED)
        print(f"   Tool: {result['command'].split()[0]}")
        print(f"   Time: {result['execution_time']:.2f}s")
        
        # Basic analysis
        if result['return_code'] == 0 and result['output']:
            if 'nmap' in result['command'] and 'open' in result['output']:
                findings.append("Open ports detected")
            elif 'Server:' in result['output']:
                findings.append("Web server information disclosed")
            elif 'MX' in result['output'] or 'NS' in result['output']:
                findings.append("DNS records enumerated")
        
        print(f"   Output size: {len(result['output'])} bytes")
        print()
    
    if findings:
        print_colored("🎯 FINDINGS:", Colors.RED, bold=True)
        for finding in findings:
            print(f"   • {finding}")
    else:
        print_colored("ℹ️  No significant findings detected", Colors.YELLOW)
    
    print_colored(f"\n📁 Detailed results saved to: {results_dir}/", Colors.CYAN)
    
    return results

if __name__ == "__main__":
    # Run simple test first
    run_simple_parallel_test()
    
    print("\n" + "="*80 + "\n")
    
    # Run pentesting test
    test_real_pentesting()
    
    print()
    print_colored("✅ Multi-Terminal Testing Complete!", Colors.GREEN, bold=True)
    print_colored("✨ This demonstrates parallel command execution", Colors.CYAN)
    print_colored("🎯 Commands run simultaneously while main script continues", Colors.CYAN)
    print_colored("📊 Results collected and analyzed automatically", Colors.CYAN)
