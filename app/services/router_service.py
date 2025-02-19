from typing import Dict, List, Callable, Tuple
import logging

from app.models.command import Command
from app.services.user_service import UserService

class RouterService:
    def __init__(self):
        self.commands: Dict[str, Command] = {}
        self._register_commands()
        self.public_commands = ["!help", "!register", "!validate"]
        self.user_service = UserService()

    def _register_commands(self):
        """Register all available commands"""
        self.register_command(
            "!help",
            self._handle_help,
            min_args=0,
            max_args=0,
            help_text="Show available commands"
        )

    def register_command(self, name: str, handler: Callable, min_args: int, max_args: int, help_text: str):
        """Register a new command"""
        self.commands[name] = Command(name, handler, min_args, max_args, help_text)

    def parse_message(self, message: str) -> Tuple[str, List[str]]:
        """Parse message into command and arguments"""
        parts = message.strip().split()
        if not parts:
            return "", []

        command = parts[0].lower()
        args = parts[1:]
        return command, args

    def route(self, message: str, wa_id: str, phone_number: str) -> str:
        """Route the message to appropriate handler"""
        command, args = self.parse_message(message)

        # Log the routing attempt
        logging.info(f"Routing command: {command} with args: {args}")

        # If no command or unrecognized command, show help
        if not command or command not in self.commands:
            return f"""❓ Unknown Command

{self._handle_help([], wa_id, phone_number)}"""

        cmd = self.commands[command]

        # Validate number of arguments
        if len(args) < cmd.min_args:
            return f"""⚠️ Missing Information

The command {command} requires more information.
{cmd.help_text}

Type !help for more details."""

        if len(args) > cmd.max_args:
            return f"""⚠️ Too Much Information

The command {command} was given too many arguments.
{cmd.help_text}

Type !help for more details."""

        # Check if the command requires registration
        user = self.user_service.get_user_by_wa_id(wa_id)
        if command not in self.public_commands and user is None:
            return f"""🔒 Registration Required

This command is only available for registered users.

To register:
1. Use !register <your-email>
2. Check your email for the verification code
3. Use !validate <your-email> <code>"""

        # Execute the command
        try:
            return cmd.handler(args, wa_id, phone_number)
        except Exception as e:
            logging.error(f"Error executing command {command}: {str(e)}")
            return str(e)

    def _handle_help(self, args: List[str], wa_id: str, phone_number: str) -> str:
        """Handle !help command"""
        # Check if user is registered to show appropriate help
        user = self.user_service.get_user_by_wa_id(wa_id) if wa_id else None

        response = """📱 Better Calendar Commands

"""
        # Public commands first
        response += """🌐 Public Commands:
"""
        for cmd_name in self.public_commands:
            if cmd_name in self.commands:
                cmd = self.commands[cmd_name]
                response += f"{cmd_name} - {cmd.help_text}\n"

        # Only show registered commands if user is registered
        if user:
            response += """
🔐 User Commands:
"""
            for cmd_name, cmd in self.commands.items():
                if cmd_name not in self.public_commands:
                    response += f"{cmd_name} - {cmd.help_text}\n"
        else:
            response += """
ℹ️ More commands will be available after registration.
Use !register <your-email> to get started."""

        return response