import pandas as pd

def run_backtest(
    buy_signal: pd.Series,
    sell_signal: pd.Series,
    ticker_obj,
    initial_cash=100000,
    trade_pct=0.1
) -> pd.DataFrame:
    prices = ticker_obj.historical_prices["Close"]

    # Safely align all 3 series — log if misaligned
    if not (buy_signal.index.equals(prices.index) and sell_signal.index.equals(prices.index)):
        print("[DEBUG] Reindexing signals to match prices...")
        print("Buy signal index head:", buy_signal.index[:3])
        print("Price index head:", prices.index[:3])
        buy_signal = buy_signal.reindex(prices.index)
        sell_signal = sell_signal.reindex(prices.index)

    currentVal = initial_cash
    inPosition = False
    shares = 0.0
    cash = initial_cash

    rows = []

    for date in prices.index:
        price = prices.loc[date]
        buy = buy_signal.loc[date]
        sell = sell_signal.loc[date]

        # Debug signal values
        print(f"{date.date()} | Price: {price} | Buy: {buy} | Sell: {sell} | InPos: {inPosition}")

        row = {
            "Date": date,
            "Price": price,
            "Buy": False,
            "Sell": False,
            "Shares": shares,
            "Cash": cash,
            "Portfolio Value": currentVal
        }

        if pd.isna(price):
            rows.append(row)
            continue

        # Use == True instead of 'is True' to avoid type mismatch
        if buy == True and (sell != True) and not inPosition:
            allocation = currentVal * trade_pct
            shares = allocation / price
            cash -= shares * price
            inPosition = True
            row["Buy"] = True

        elif sell == True and (buy != True) and inPosition:
            cash += shares * price
            shares = 0.0
            inPosition = False
            row["Sell"] = True

        currentVal = cash + shares * price
        row["Shares"] = shares
        row["Cash"] = cash
        row["Portfolio Value"] = currentVal

        rows.append(row)

    portfolioData = pd.DataFrame(rows)
    portfolioData.set_index("Date", inplace=True)
    return portfolioData


# import pandas as pd

# def run_backtest(
#     buy_signal: pd.Series,
#     sell_signal: pd.Series,
#     ticker_obj,
#     initial_cash=100000,
#     trade_pct=0.1
# ) -> pd.DataFrame:
#     """
#     Executes a long-only backtest based on explicit buy/sell signals.

#     Args:
#         buy_signal (pd.Series): Series of booleans for buy signals
#         sell_signal (pd.Series): Series of booleans for sell signals
#         ticker_obj: Ticker object with historical_prices["Close"]
#         initial_cash (float): Starting capital
#         trade_pct (float): Fraction of cash to use per buy

#     Returns:
#         pd.DataFrame: Portfolio time series with portfolio value and cash
#     """
#     prices = ticker_obj.historical_prices["Close"].copy()
#     buy_signal = buy_signal.reindex(prices.index)
#     sell_signal = sell_signal.reindex(prices.index)

#     df = pd.DataFrame(index=prices.index)
#     df["Price"] = prices
#     df["Buy"] = buy_signal
#     df["Sell"] = sell_signal

#     cash = initial_cash
#     shares = 0.0
#     in_position = False
#     portfolio_values = []

#     for date, row in df.iterrows():
#         price = row["Price"]
#         buy = row["Buy"]
#         sell = row["Sell"]

#         if pd.isna(price):
#             # No price data — skip
#             portfolio_values.append(cash)
#             continue

#         if buy is True and (sell is not True) and not in_position:
#             # Buy condition met
#             allocation = cash * trade_pct
#             shares = allocation / price
#             cash -= shares * price
#             in_position = True

#         elif sell is True and (buy is not True) and in_position:
#             # Sell condition met
#             cash += shares * price
#             shares = 0.0
#             in_position = False

#         # Calculate portfolio value
#         portfolio_values.append(cash + shares * price)

#     df["Portfolio Value"] = portfolio_values
#     df["Cash"] = [cash] * len(df)  # Optional: can track dynamically
#     return df
