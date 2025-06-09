from objects.tickers import Ticker

def handle_inst(parts, registry):
    if len(parts) < 3:
        return "Usage: inst ticker SYMBOL"

    class_name = parts[1].lower()
    symbol = parts[2].upper()

    try:
        if class_name == "ticker":
            obj = Ticker(symbol)
            registry[symbol] = obj
            return f"Instantiated Ticker '{symbol}' successfully."
        else:
            return f"Unknown class type: {class_name}"
    except Exception as e:
        return f"Error instantiating object: {e}"
