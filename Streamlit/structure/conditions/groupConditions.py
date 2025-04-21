import re
import pandas as pd

class GroupConditions:
    def __init__(self, conditions, logic_str):
        self.conditions = conditions
        self.logic_str = logic_str
        self.boolData = None
        self._evaluate()

    def _evaluate(self):
        # Map: "1" → condition.boolData, etc.
        context = {str(i + 1): cond.boolData for i, cond in enumerate(self.conditions)}

        expr = self.logic_str.strip().upper()

        # Auto-wrap numeric-only expressions
        if re.fullmatch(r"\d+", expr):
            expr = f"({expr})"

        # Replace logical words with Python operators
        expr = expr.replace("AND", "&").replace("OR", "|").replace("XOR", "^")

        # Replace numbers like 1, 2, 3 with variable lookups: context['1'], etc.
        def replace_index(match):
            var = match.group()
            if var not in context:
                raise ValueError(f"Condition index '{var}' not found.")
            return f"context['{var}']"

        expr = re.sub(r"\b\d+\b", replace_index, expr)

        try:
            result = eval(expr, {"context": context})
            if not isinstance(result, pd.Series):
                raise ValueError("Expression must evaluate to a pandas Series, not a scalar.")
            self.boolData = result
        except Exception as e:
            raise ValueError(f"Error evaluating logical condition expression: {e}")
