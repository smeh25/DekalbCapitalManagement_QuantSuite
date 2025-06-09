def handle_get(parts, registry):
    if len(parts) < 2:
        return "Usage: get ObjectName.Attribute"

    try:
        expression = parts[1]
        obj_name, attr = expression.split('.', 1)

        obj = registry.get(obj_name.upper())
        if not obj:
            return f"Object '{obj_name}' not found."

        value = eval(f"obj.{attr}")
        return f"{expression} = {value}"
    except Exception as e:
        return f"Error retrieving attribute: {e}"
