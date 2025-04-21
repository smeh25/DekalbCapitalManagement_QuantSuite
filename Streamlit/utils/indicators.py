# indicators.py
import pandas as pd

supportedIndicators = [
    "RSI",
    "PCTCHANGE_1D",
    "PCTCHANGE_3D",
    "PCTCHANGE_5D"
]

def compute_indicator(data, indicator):
    if indicator == "RSI":
        return compute_RSI(data)
    elif indicator == "PCTCHANGE_1D":
        return compute_pctchange(data, 1)
    elif indicator == "PCTCHANGE_3D":
        return compute_pctchange(data, 3)
    elif indicator == "PCTCHANGE_5D":
        return compute_pctchange(data, 5)
    else:
        raise ValueError(f"Unsupported indicator: {indicator}")

def compute_RSI(data, period=14):
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def compute_pctchange(data, n_days):
    return data['Close'].pct_change(periods=n_days) * 100
