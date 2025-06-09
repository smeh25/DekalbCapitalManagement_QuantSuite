from command_directory.inst.inst import handle_inst
from command_directory.get.get import handle_get

registry = {}

def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "No input detected."

    command = parts[0].lower()

    if command == "inst":
        return handle_inst(parts, registry)
    elif command == "get":
        return handle_get(parts, registry)
    else:
        return f"Unknown command: {command}"

def get_registry():
    return registry
