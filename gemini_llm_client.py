# autopentest_project/gemini_llm_client.py

import google.generativeai as genai
# from google.generativeai import types # We might not need explicit types import this way
import json
import re
from config import Colors, print_colored

def parse_llm_response_json(response_text: str) -> dict:
    """
    Extracts the enhanced pentesting response from the model's JSON response.
    Handles potential ```json ... ``` markdown and other noise.
    """
    action = {
        "thought": "Error: LLM response was empty or unparseable.", 
        "command": "",
        "phase": "unknown",
        "tool_category": "unknown",
        "expected_outcome": "Unknown",
        "next_steps": "Review error and retry"
    }
    
    try:
        # Attempt to find JSON block within markdown
        match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
        if match:
            json_text = match.group(1).strip()
        else:
            # If no markdown, assume the whole text might be JSON or contain it
            json_text = response_text.strip()

        # Try to find the first '{' and last '}' to extract a valid JSON object
        first_brace = json_text.find('{')
        last_brace = json_text.rfind('}')

        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            json_text_to_parse = json_text[first_brace : last_brace + 1]
            try:
                parsed_action = json.loads(json_text_to_parse)
                
                # Validate required keys for enhanced format
                required_keys = ["thought", "command"]
                if all(key in parsed_action for key in required_keys):
                    # Update with parsed values, keeping defaults for missing optional keys
                    for key in ["thought", "command", "phase", "tool_category", "expected_outcome", "next_steps"]:
                        if key in parsed_action:
                            action[key] = parsed_action[key]
                else:
                    action["thought"] = "Error: LLM response JSON missing required keys."
                    print_colored(f"[LLM Client] Required keys missing. Raw: {json_text_to_parse}", Colors.RED)
                    
            except json.JSONDecodeError as e_inner:
                action["thought"] = f"Error: Failed to decode JSON from extracted text: {e_inner}. Raw: {json_text_to_parse}"
                print_colored(f"[LLM Client] JSONDecodeError on extracted text: {e_inner}. Raw: {json_text_to_parse}", Colors.RED)
                fallback_cmd = extract_fallback_command(response_text)
                if fallback_cmd and fallback_cmd != "exit":
                     action["command"] = fallback_cmd
                     action["thought"] = "Fallback: JSON parsing failed, extracted command directly."
                elif fallback_cmd == "exit":
                    if "command" not in action or action["command"].lower() != "exit":
                        action["command"] = "exit"
                        action["thought"] = "Fallback: JSON parsing failed, but 'exit' keyword found."
        else:
            action["thought"] = "Error: No valid JSON object found in LLM response."
            print_colored(f"[LLM Client] No clear JSON object found. Raw: {json_text}", Colors.RED)
            fallback_cmd = extract_fallback_command(response_text)
            if fallback_cmd:
                 action["command"] = fallback_cmd
                 action["thought"] = "Fallback: No JSON, extracted command directly."

    except Exception as e:
        action["thought"] = f"Error: Unexpected error parsing LLM response: {str(e)}. Raw: {response_text}"
        print_colored(f"[LLM Client] Unexpected parsing error: {e}. Raw: {response_text}", Colors.RED)
        fallback_cmd = extract_fallback_command(response_text)
        if fallback_cmd:
            action["command"] = fallback_cmd
            action["thought"] = "Fallback: Exception during JSON parse, extracted command directly."

    return action

def extract_fallback_command(response_text: str) -> str:
    """
    Fallback to extract command if JSON parsing fails.
    Looks for ```bash ... ``` or assumes the first non-empty line is a command.
    """
    pattern = r"```bash\s*(.*?)\s*```"
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return match.group(1).strip()

    stripped_response = response_text.strip().lower()
    if stripped_response == "exit" or stripped_response.startswith("exit "):
        return "exit"

    lines = [line.strip() for line in response_text.splitlines() if line.strip()]
    if lines:
        potential_command = lines[0]
        if len(potential_command.split()) < 15 and len(potential_command) < 200:
            if not potential_command.lower().startswith(("i think", "the next step", "my thought", "based on", "error:")):
                return potential_command
    return ""


class GeminiClient:
    def __init__(self, api_key: str, system_instructions: str, model_name: str):
        if not api_key:
            print_colored("API Key for Gemini is not configured. Please set the GEMINI_API_KEY environment variable.", Colors.RED, bold=True)
            raise ValueError("Gemini API Key is missing.")

        genai.configure(api_key=api_key)
        self.model_name = model_name
        # Store system instructions to be used with GenerativeModel
        self.system_instructions_text = system_instructions
        self.conversation_history = [] # List of {'role': 'user'/'model', 'parts': ['text']} dicts

        # Initialize the model here
        try:
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=self.system_instructions_text
                # generation_config can be set here too if needed globally
                # safety_settings can be set here too
            )
        except Exception as e:
            print_colored(f"Failed to initialize GenerativeModel: {e}", Colors.RED, bold=True)
            raise


    def send_message(self, user_input: str) -> str:
        """
        Sends user_input to the Gemini model and returns its response text.
        Manages conversation history.
        """
        print_colored(f"\n[LLM Client] Sending to Gemini:", Colors.LIGHTBLUE_EX)
        print_colored(f"  User Input: {user_input[:200]}...", Colors.LIGHTBLACK_EX)

        # Add current user message to history
        self.conversation_history.append({'role': 'user', 'parts': [user_input]})

        try:
            # Create a new chat session for each call if model is stateless or to ensure context
            # For multi-turn, we pass the whole history.
            chat_session = self.model.start_chat(history=self.conversation_history[:-1]) # Pass history *before* current user input
            response = chat_session.send_message(user_input) # Send only the current user input

            response_text = response.text.strip() # Access text directly

            # Update conversation history with model's response
            self.conversation_history.append({'role': 'model', 'parts': [response_text]})

            # Optional: Limit history size
            max_history_turns = 10 # Keep last 10 user-model exchanges (20 items)
            if len(self.conversation_history) > max_history_turns * 2:
                # Trim from the beginning, but keep at least one user/model pair if possible
                # Ensure we don't create an empty history or a history starting with 'model'
                # A more robust way is to ensure we always have pairs or start with 'user'
                # For simplicity here, just slicing:
                self.conversation_history = self.conversation_history[-(max_history_turns * 2):]


            print_colored(f"[LLM Client] Received from Gemini:", Colors.LIGHTBLUE_EX)
            # print_colored(f"  Raw Response: {response_text[:300]}...", Colors.LIGHTBLACK_EX)
            return response_text

        except Exception as e:
            print_colored(f"[LLM Client] Error communicating with Gemini API: {e}", Colors.RED, bold=True)
            # Attempt to remove the last user message if call failed, to avoid resending on retry
            if self.conversation_history and self.conversation_history[-1]['role'] == 'user':
                self.conversation_history.pop()

            # Log more details if available
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                 print_colored(f"  Prompt Feedback: {response.prompt_feedback}", Colors.YELLOW)
            if hasattr(response, 'candidates') and response.candidates and response.candidates[0].finish_reason:
                 print_colored(f"  Finish Reason: {response.candidates[0].finish_reason}", Colors.YELLOW)
                 if response.candidates[0].safety_ratings:
                     print_colored(f"  Safety Ratings: {response.candidates[0].safety_ratings}", Colors.YELLOW)

            return json.dumps({
                "thought": f"Critical Error: Failed to get response from LLM API: {str(e)}. Cannot proceed.",
                "command": "exit"
            })

    def clear_history(self):
        self.conversation_history = []
        print_colored("[LLM Client] Conversation history cleared.", Colors.YELLOW)
