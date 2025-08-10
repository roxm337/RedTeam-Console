# enhanced_logger.py
"""
Enhanced logging module for the AI Pentester Agent.
"""

import logging
import json
import datetime
from pathlib import Path
from typing import Dict, Any
from config import Colors, print_colored

class EnhancedLogger:
    """Enhanced logging with structured data and security events."""
    
    def __init__(self, log_dir: str = None):
        # Import here to avoid circular imports
        from session_manager import session_manager
        
        self.log_dir = session_manager.logs_dir if log_dir is None else Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create session-specific log file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_log = self.log_dir / f"session_{timestamp}.log"
        self.security_log = self.log_dir / f"security_{timestamp}.log"
        
        # Configure loggers
        self._setup_loggers()
        
        self.session_data = {
            "session_id": timestamp,
            "start_time": datetime.datetime.now().isoformat(),
            "objective": None,
            "iterations": [],
            "security_events": []
        }
    
    def _setup_loggers(self):
        """Setup structured logging."""
        # Session logger
        self.session_logger = logging.getLogger("session")
        self.session_logger.setLevel(logging.INFO)
        session_handler = logging.FileHandler(self.session_log)
        session_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        session_handler.setFormatter(session_formatter)
        self.session_logger.addHandler(session_handler)
        
        # Security logger
        self.security_logger = logging.getLogger("security")
        self.security_logger.setLevel(logging.WARNING)
        security_handler = logging.FileHandler(self.security_log)
        security_formatter = logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s'
        )
        security_handler.setFormatter(security_formatter)
        self.security_logger.addHandler(security_handler)
    
    def log_objective(self, objective: str):
        """Log the initial objective."""
        self.session_data["objective"] = objective
        self.session_logger.info(f"OBJECTIVE SET: {objective}")
        print_colored(f"📝 Logged objective: {objective}", Colors.GREEN)
    
    def log_iteration(self, iteration: int, thought: str, command: str, 
                     output: str, return_code: int, approved: bool):
        """Log a complete iteration."""
        iteration_data = {
            "iteration": iteration,
            "timestamp": datetime.datetime.now().isoformat(),
            "thought": thought,
            "command": command,
            "output": output[:1000],  # Truncate long outputs
            "return_code": return_code,
            "user_approved": approved
        }
        
        self.session_data["iterations"].append(iteration_data)
        self.session_logger.info(f"ITERATION {iteration}: Command='{command}', RC={return_code}, Approved={approved}")
    
    def log_security_event(self, event_type: str, command: str, details: str):
        """Log security-related events."""
        security_event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event_type": event_type,
            "command": command,
            "details": details
        }
        
        self.session_data["security_events"].append(security_event)
        self.security_logger.warning(f"{event_type}: {command} - {details}")
        print_colored(f"🔒 Security Event: {event_type} - {details}", Colors.RED)
    
    def save_session_summary(self):
        """Save a comprehensive session summary."""
        self.session_data["end_time"] = datetime.datetime.now().isoformat()
        
        summary_file = self.log_dir / f"summary_{self.session_data['session_id']}.json"
        with open(summary_file, 'w') as f:
            json.dump(self.session_data, f, indent=2)
        
        print_colored(f"📊 Session summary saved to: {summary_file}", Colors.GREEN)
        return str(summary_file)

# Global logger instance
enhanced_logger = EnhancedLogger()
