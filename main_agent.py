# autopentest_project/main_agent.py

import sys
import datetime
from typing import Union
from config import (
    GEMINI_API_KEY, SYSTEM_INSTRUCTIONS, MODEL_NAME, MAX_ITERATIONS,
    USER_COMMAND_APPROVAL, Colors, print_colored, SUDO_PASSWORD
)
from gemini_llm_client import GeminiClient, parse_llm_response_json
from command_executor import execute_command
from security_validator import validator
from enhanced_logger import enhanced_logger
from config_validator import config_validator
from pentesting_tools import tools_manager

def display_welcome_message():
    print_colored("==============================================", Colors.MAGENTA, bold=True)
    print_colored("    AutoPentest AI Agent v2.0               ", Colors.MAGENTA, bold=True)
    print_colored("    Professional Pentesting Framework       ", Colors.MAGENTA, bold=True)
    print_colored("==============================================", Colors.MAGENTA, bold=True)
    print_colored("Powered by Google Gemini + Real Pentesting Tools", Colors.LIGHTBLUE_EX)
    print_colored("Comprehensive Security Assessment Framework", Colors.LIGHTBLUE_EX)
    print_colored("", Colors.WHITE)
    
    # Validate configuration
    is_valid, issues = config_validator.validate_environment()
    if not is_valid:
        print_colored("❌ Configuration validation failed. Please fix the issues above.", Colors.RED, bold=True)
        sys.exit(1)
    
    config_validator.print_config_summary()
    
    # Check pentesting tools
    print_colored("", Colors.WHITE)
    tools_manager.check_all_tools()
    
    print_colored("", Colors.WHITE)
    if USER_COMMAND_APPROVAL:
        print_colored("🔒 SECURITY MODE: User approval required for all commands", Colors.LIGHTGREEN_EX, bold=True)
    else:
        print_colored("⚡ AUTO MODE: Commands execute automatically (HIGH RISK)", Colors.LIGHTRED_EX, bold=True)
    
    print_colored("", Colors.WHITE)
    print_colored("📋 AVAILABLE METHODOLOGIES:", Colors.CYAN, bold=True)
    print_colored("   • Reconnaissance & Information Gathering", Colors.LIGHTYELLOW_EX)
    print_colored("   • Network & Service Enumeration", Colors.LIGHTYELLOW_EX)
    print_colored("   • Vulnerability Assessment", Colors.LIGHTYELLOW_EX)
    print_colored("   • Web Application Testing", Colors.LIGHTYELLOW_EX)
    print_colored("   • Custom Function Integration", Colors.LIGHTYELLOW_EX)
    
    print_colored("", Colors.WHITE)
    print_colored("🔧 SPECIAL COMMANDS:", Colors.CYAN, bold=True)
    print_colored("   • custom_function:function_name:params", Colors.LIGHTWHITE_EX)
    print_colored("   • install_tool:tool_name", Colors.LIGHTWHITE_EX)
    print_colored("   • report_generation", Colors.LIGHTWHITE_EX)
    
    if SUDO_PASSWORD:
        print_colored("", Colors.WHITE)
        print_colored("!! SECURITY WARNING !!", Colors.RED, bold=True)
        print_colored("Sudo password configured - Use only in isolated environments", Colors.RED)
    
    print_colored("----------------------------------------------", Colors.MAGENTA)

def get_initial_objective():
    print_colored("\n🎯 Define your penetration testing objective:", Colors.CYAN, bold=True)
    print_colored("Examples:", Colors.LIGHTBLACK_EX)
    print_colored("  • 'Reconnaissance scan of example.com'", Colors.LIGHTBLACK_EX)
    print_colored("  • 'Vulnerability assessment of 192.168.1.0/24'", Colors.LIGHTBLACK_EX)
    print_colored("  • 'Web application security test of https://target.com'", Colors.LIGHTBLACK_EX)
    print_colored("  • 'Network enumeration and service discovery'", Colors.LIGHTBLACK_EX)
    
    objective = input(f"{Colors.LIGHTWHITE_EX}Objective> {Colors.RESET}")
    if not objective.strip():
        print_colored("Objective cannot be empty. Exiting.", Colors.RED)
        sys.exit(1)
    return objective

#highlight_start
def get_user_approval_for_command(command_to_run: str) -> tuple[bool, Union[str, None]]:
    """
    Prompts the user to approve, reject, or reject with a message for the LLM.

    Returns:
        - bool: True if approved, False otherwise.
        - str | None: Message to LLM if rejected with a message, else None.
    """
    while True:
        print_colored("\n[User Interaction] Proposed command for execution:", Colors.LIGHTMAGENTA_EX, bold=True)
        print_colored(f"  $ {command_to_run}", Colors.WHITE)
        prompt_message = (
            f"{Colors.LIGHTMAGENTA_EX}Do you want to:"
            f"\n  (Y)es, execute this command."
            f"\n  (N)o, reject this command (LLM will try another)."
            f"\n  (R)eject with message (provide feedback to LLM why it was rejected)."
            f"\n  (Q)uit the agent."
            f"\nYour choice (Y/N/R/Q): {Colors.RESET}"
        )
        choice = input(prompt_message).strip().lower()

        if choice == 'y':
            return True, None
        elif choice == 'n':
            return False, "User rejected the command. Please provide an alternative command or approach."
        elif choice == 'r':
            print_colored("Please provide a message to the LLM explaining why you are rejecting this command:", Colors.LIGHTMAGENTA_EX)
            rejection_message = input(f"{Colors.LIGHTWHITE_EX}> {Colors.RESET}")
            if not rejection_message.strip():
                rejection_message = "User rejected the command without a specific message, but chose to provide feedback. Please reconsider."
            return False, f"User rejected the command with the following feedback: '{rejection_message}'. Please analyze this feedback and provide a new command or approach."
        elif choice == 'q':
            print_colored("[Agent] User requested quit. Exiting.", Colors.YELLOW)
            sys.exit(0) # Clean exit
        else:
            print_colored("Invalid choice. Please enter Y, N, R, or Q.", Colors.RED)
#highlight_end

def main():
    display_welcome_message()

    if not GEMINI_API_KEY:
        print_colored("Error: GEMINI_API_KEY environment variable not set. Exiting.", Colors.RED, bold=True)
        sys.exit(1)

    initial_objective = get_initial_objective()
    print_colored(f"\n[Agent] Objective Set: {initial_objective}", Colors.GREEN)
    enhanced_logger.log_objective(initial_objective)

    try:
        llm_client = GeminiClient(
            api_key=GEMINI_API_KEY,
            system_instructions=SYSTEM_INSTRUCTIONS,
            model_name=MODEL_NAME
        )
    except ValueError as e:
        print_colored(f"Failed to initialize LLM Client: {e}", Colors.RED, bold=True)
        sys.exit(1)
    except Exception as e: # Catch other potential init errors from GenerativeModel
        print_colored(f"An unexpected error occurred during LLM Client initialization: {e}", Colors.RED, bold=True)
        sys.exit(1)


    current_llm_input = f"My objective is: '{initial_objective}'.\n" \
                        "I have not run any commands yet. What is your first thought and command to start working towards this objective?"
    session_log = [f"Objective: {initial_objective}\n"]

    for i in range(1, MAX_ITERATIONS + 1):
        print_colored(f"\n=============== Iteration {i}/{MAX_ITERATIONS} ===============", Colors.MAGENTA, bold=True)

        llm_response_text = llm_client.send_message(current_llm_input)

        if not llm_response_text:
            print_colored("[Agent] LLM returned an empty response. Aborting.", Colors.RED, bold=True)
            session_log.append("LLM returned an empty response. Aborted.")
            break

        action = parse_llm_response_json(llm_response_text)
        thought = action.get("thought", "Error: No thought provided by LLM.")
        command_to_run = action.get("command", "")
        phase = action.get("phase", "unknown")
        tool_category = action.get("tool_category", "unknown")
        expected_outcome = action.get("expected_outcome", "Unknown")
        next_steps = action.get("next_steps", "Continue assessment")

        print_colored("\n[LLM Analysis]", Colors.YELLOW, bold=True)
        print_colored(f"💭 Thought: {thought}", Colors.LIGHTYELLOW_EX)
        print_colored(f"🔍 Phase: {phase}", Colors.LIGHTCYAN_EX)
        print_colored(f"🛠️  Tool Category: {tool_category}", Colors.LIGHTMAGENTA_EX)
        print_colored(f"🎯 Expected Outcome: {expected_outcome}", Colors.LIGHTBLUE_EX)
        
        session_log.append(f"\n--- Iteration {i} ---\n")
        session_log.append(f"LLM Thought: {thought}\n")
        session_log.append(f"Phase: {phase}\n")
        session_log.append(f"Tool Category: {tool_category}\n")
        session_log.append(f"Expected: {expected_outcome}\n")

        if not command_to_run:
            print_colored("[Agent] LLM did not provide a command in the current step.", Colors.YELLOW)
            current_llm_input = (
                f"You did not provide a command in your last response. "
                f"Your thought was: '{thought}'. "
                f"Please provide a command to proceed with the objective: '{initial_objective}', or type 'exit' in the command field if you are done or stuck."
            )
            session_log.append("LLM Action: No command provided.\n")
            continue

        print_colored("\n[Proposed Command]", Colors.CYAN, bold=True)
        
        # Check if it's a special command
        if command_to_run.startswith(("custom_function:", "install_tool:", "report_generation")):
            print_colored(f"🔧 Special Command: {command_to_run}", Colors.LIGHTMAGENTA_EX)
        else:
            print_colored(f"💻 Shell Command: $ {command_to_run}", Colors.LIGHTWHITE_EX)
            
            # Security validation for shell commands
            is_safe, risk_level, warnings = validator.validate_command(command_to_run)
            validator.print_validation_result(command_to_run, is_safe, risk_level, warnings)
            
            if not is_safe:
                print_colored("🚫 Command blocked by security validator", Colors.RED, bold=True)
                current_llm_input = (
                    f"The command '{command_to_run}' was BLOCKED by security validation due to safety concerns. "
                    f"Please provide an alternative, safer command to achieve the objective: '{initial_objective}'."
                )
                continue
        
        session_log.append(f"LLM Command: {command_to_run}\n")

        if command_to_run.strip().lower() == "exit":
            print_colored("\n==============================================", Colors.GREEN, bold=True)
            print_colored("    LLM has requested to EXIT.             ", Colors.GREEN, bold=True)
            print_colored("==============================================", Colors.GREEN, bold=True)
            print_colored("\nFinal Report from LLM:", Colors.LIGHTGREEN_EX, bold=True)
            print_colored(thought, Colors.LIGHTGREEN_EX)
            session_log.append(f"\nLLM Exited. Final Report:\n{thought}\n")
            break

        #highlight_start
        execute_this_command = True
        user_feedback_for_llm = None

        if USER_COMMAND_APPROVAL:
            approved, feedback_msg = get_user_approval_for_command(command_to_run)
            if approved:
                print_colored("[User Interaction] Command Approved for execution.", Colors.GREEN)
                session_log.append("User Action: Approved command.\n")
            else:
                execute_this_command = False
                user_feedback_for_llm = feedback_msg # This will be sent to LLM
                print_colored(f"[User Interaction] Command Rejected. Feedback to LLM: {feedback_msg}", Colors.YELLOW)
                session_log.append(f"User Action: Rejected command. Feedback: {feedback_msg}\n")
        else:
            # If approval is not needed, we can still log that it was auto-approved or simply proceed
            session_log.append("User Action: Command auto-approved (approval disabled).\n")


        if execute_this_command:
            cmd_output, cmd_rc, cmd_timed_out = execute_command(command_to_run)
            
            # Log the iteration with enhanced data
            enhanced_logger.log_iteration(i, thought, command_to_run, cmd_output, cmd_rc, True)
            
            session_log.append(f"Command Output (RC: {cmd_rc}, Timed Out: {cmd_timed_out}):\n{cmd_output}\n")
            
            # Enhanced feedback based on command type and results
            if cmd_timed_out:
                current_llm_input = (
                    f"The command '{command_to_run}' TIMED OUT.\n"
                    f"Phase: {phase}, Tool Category: {tool_category}\n"
                    f"Expected Outcome: {expected_outcome}\n"
                    f"Output (if any) before timeout:\n{cmd_output}\n\n"
                    f"Analyze this timeout and decide on the next step for the objective: '{initial_objective}'. "
                    f"Consider if the command needs modification, a different timeout, or if an alternative approach is better. "
                    f"Next planned steps were: {next_steps}"
                )
            elif cmd_rc != 0:
                current_llm_input = (
                    f"The command '{command_to_run}' FAILED with return code {cmd_rc}.\n"
                    f"Phase: {phase}, Tool Category: {tool_category}\n"
                    f"Expected Outcome: {expected_outcome}\n"
                    f"Output/Error:\n{cmd_output}\n\n"
                    f"Analyze this failure and decide on the next step for the objective: '{initial_objective}'. "
                    f"You might need to try a different command, correct the previous one, or change your approach. "
                    f"Consider the planned next steps: {next_steps}"
                )
            else:
                current_llm_input = (
                    f"The command '{command_to_run}' executed SUCCESSFULLY (return code {cmd_rc}).\n"
                    f"Phase: {phase}, Tool Category: {tool_category}\n"
                    f"Expected Outcome: {expected_outcome}\n"
                    f"Actual Output:\n{cmd_output}\n\n"
                    f"Analyze this output and determine if the expected outcome was achieved. "
                    f"Based on this result, what is your next thought and command to achieve the objective: '{initial_objective}'? "
                    f"Continue with the planned next steps: {next_steps}"
                )
        else: # Command was rejected by user
            enhanced_logger.log_iteration(i, thought, command_to_run, "Command rejected by user", -1, False)
            current_llm_input = (
                f"The previously suggested command ('{command_to_run}') was REJECTED by the user.\n"
                f"Phase: {phase}, Tool Category: {tool_category}\n"
                f"Expected Outcome: {expected_outcome}\n"
                f"User feedback: {user_feedback_for_llm}\n\n"
                f"Please analyze this feedback and provide a new thought and command to achieve the objective: '{initial_objective}'. "
                f"Consider alternative approaches for the {phase} phase using {tool_category} tools."
            )
        #highlight_end

    else:
        print_colored(f"\n[Agent] Reached maximum iterations ({MAX_ITERATIONS}). Ending session.", Colors.YELLOW, bold=True)
        session_log.append(f"Reached maximum iterations ({MAX_ITERATIONS}). Aborted.")
        print_colored("Consider increasing MAX_ITERATIONS or refining the objective if more steps are needed.", Colors.YELLOW)


    print_colored("\n==============================================", Colors.BLUE, bold=True)
    print_colored("         End of AutoPentest Session         ", Colors.BLUE, bold=True)
    print_colored("==============================================", Colors.BLUE, bold=True)

    # Generate comprehensive report
    try:
        summary_file = enhanced_logger.save_session_summary()
        print_colored(f"\n📊 Session summary saved: {summary_file}", Colors.GREEN)
    except Exception as e:
        print_colored(f"\n⚠️  Could not save session summary: {e}", Colors.YELLOW)

    # Save traditional session log
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"autopentest_session_{timestamp}.log"
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("".join(session_log))
        print_colored(f"📝 Traditional session log saved: {log_file}", Colors.GREEN)
    except IOError as e:
        print_colored(f"\n⚠️  Could not save session log: {e}", Colors.YELLOW)

    # Offer to generate final report
    print_colored("\n🎯 Assessment Complete!", Colors.GREEN, bold=True)
    print_colored("Would you like to generate a comprehensive penetration testing report? (y/n): ", Colors.CYAN, bold=False)
    choice = input().strip().lower()
    if choice == 'y':
        try:
            # Execute report generation
            report_output, _, _ = execute_command("report_generation")
            print_colored("✅ Final report generated!", Colors.GREEN, bold=True)
        except Exception as e:
            print_colored(f"❌ Report generation failed: {e}", Colors.RED)


if __name__ == "__main__":
    main()
