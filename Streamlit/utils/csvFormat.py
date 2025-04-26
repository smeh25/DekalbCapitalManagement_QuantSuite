import pandas as pd

REQUIRED_COLUMNS = ["Type", "Ticker", "Shares", "Expiration", "Strike", "OptionType"]

def validate_csv(df: pd.DataFrame) -> tuple[bool, list[str]]:
    errors = []

    # 1. Column check
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")
        return False, errors

    # 2. Row-wise validation
    for i, row in df.iterrows():
        row_num = i + 2  # 1-based indexing + header
        try:
            row_type = row["Type"]
            if row_type not in ["stock", "option"]:
                errors.append(f"Row {row_num}: Invalid 'Type' value: {row_type}")

            if pd.isna(row["Ticker"]) or not isinstance(row["Ticker"], str):
                errors.append(f"Row {row_num}: 'Ticker' must be a non-empty string")

            if pd.isna(row["Shares"]) or not isinstance(row["Shares"], (int, float)):
                errors.append(f"Row {row_num}: 'Shares' must be a number")

            if row_type == "option":
                if pd.isna(row["Expiration"]):
                    errors.append(f"Row {row_num}: 'Expiration' is required for options")
                else:
                    try:
                        pd.to_datetime(row["Expiration"])
                    except Exception:
                        errors.append(f"Row {row_num}: 'Expiration' must be in YYYY-MM-DD format")

                if pd.isna(row["Strike"]) or not isinstance(row["Strike"], (int, float)):
                    errors.append(f"Row {row_num}: 'Strike' must be a number")

                if row["OptionType"] not in ["call", "put"]:
                    errors.append(f"Row {row_num}: 'Option Type' must be 'call' or 'put'")

        except Exception as e:
            errors.append(f"Row {row_num}: Unexpected error during validation: {str(e)}")

    is_valid = len(errors) == 0
    return is_valid, errors
