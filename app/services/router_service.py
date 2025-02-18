from typing import Dict, List, Callable, Tuple
import logging



class Command:
    def __init__(self, name: str, handler: Callable, min_args: int, max_args: int, help_text: str):
        self.name = name
        self.handler = handler
        self.min_args = min_args
        self.max_args = max_args
        self.help_text = help_text

class RouterService:
    def __init__(self, ):
        self.commands: Dict[str, Command] = {}
        self._register_commands()

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
            return self._handle_help([], wa_id, phone_number)

        cmd = self.commands[command]

        # Validate number of arguments
        if len(args) < cmd.min_args:
            return f"Too few arguments for {command}. {cmd.help_text}"
        if len(args) > cmd.max_args:
            return f"Too many arguments for {command}. {cmd.help_text}"

        # Execute the command
        try:
            return cmd.handler(args, wa_id, phone_number)
        except Exception as e:
            logging.error(f"Error executing command {command}: {str(e)}")
            return f"Error executing command. Please try again."

    def _handle_help(self, args: List[str], wa_id: str, phone_number: str) -> str:
        """Handle !help command"""
        response = "Available commands:\n\n"

        # Group commands by whether they require registration
        public_commands = ["!help", "!register", "!validate"]

        response += "Public commands:\n"
        for cmd_name in public_commands:
            if cmd_name in self.commands:
                cmd = self.commands[cmd_name]
                response += f"{cmd_name} - {cmd.help_text}\n"

        response += "\nCommands requiring registration:\n"
        for cmd_name, cmd in self.commands.items():
            if cmd_name not in public_commands:
                response += f"{cmd_name} - {cmd.help_text}\n"

        return response