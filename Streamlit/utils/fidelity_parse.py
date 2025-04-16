import pandas as pd
import re

def parse_fidelity_csv(df: pd.DataFrame) -> pd.DataFrame:
    parsed_data = []

    for _, row in df.iterrows():
        symbol = str(row.get("Symbol", ""))
        description = str(row.get("Description", ""))
        quantity = row.get("Quantity", None)

        # Skip invalid or non-position rows
        if not symbol or pd.isna(quantity) or "HELD IN MONEY MARKET" in description:
            continue

        # Stock position
        if "CALL" not in description and "PUT" not in description and not re.match(r".*\d{6}[CP]\d+", symbol):
            parsed_data.append({
                "Type": "stock",
                "Ticker": symbol.strip(),
                "Shares": float(quantity),
                "Expiration": "",
                "Strike": "",
                "OptionType": ""
            })
        else:
            # Try to extract option info
            match = re.match(r"-?([A-Z]+)(\d{6})([CP])(\d+)", symbol)
            if match:
                ticker, date_str, opt_type_letter, strike_str = match.groups()
                expiration = f"20{date_str[:2]}-{date_str[2:4]}-{date_str[4:]}"
                opt_type = "call" if opt_type_letter == "C" else "put"
                strike = float(strike_str)
                parsed_data.append({
                    "Type": "option",
                    "Ticker": ticker,
                    "Shares": float(quantity),
                    "Expiration": expiration,
                    "Strike": strike,
                    "OptionType": opt_type
                })

    return pd.DataFrame(parsed_data)

# Example usage:
# df = pd.read_csv("your_fidelity_export.csv")
# parsed_df = parse_fidelity_csv(df)
# parsed_df.to_csv("parsed_positions.csv", index=False)
