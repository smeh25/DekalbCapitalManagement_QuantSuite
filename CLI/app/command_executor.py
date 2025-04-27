from app.workspace import namespace


# def execute_command(command):
#     try:
#         result = eval(command, {}, namespace)
#         return result
#     except Exception as e:
#         return f"Error: {str(e)}"

from app.workspace import namespace, set_variable, get_variable
from models.tickers import Ticker

def execute_command(command):
    try:
        if command.startswith("inst "):
            symbol = command[len("inst "):].strip().upper()
            obj = Ticker(symbol)
            set_variable(symbol, obj)
            return f"Ticker '{symbol}' instantiated and saved."

        elif command.startswith("display "):
            symbol = command[len("display "):].strip().upper()
            obj = get_variable(symbol)
            if not obj:
                return f"Error: Variable '{symbol}' not found."

            attrs = {k: v for k, v in vars(obj).items() if not k.startswith('_')}
            output = [f"{k}: {v}" for k, v in attrs.items()]
            return "\n".join(output)

        else:
            # Default: try to eval any expression
            result = eval(command, {}, namespace)
            return result

    except Exception as e:
        return f"Error: {str(e)}"

