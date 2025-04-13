import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from utils import correlation
from structure import Portfolio, Ticker


st.title("Delta Hedging Tool")

if "portfolio" not in st.session_state:
    st.error("No portfolio loaded. Please upload your file on the main page.")
    st.stop()

portfolio = st.session_state["portfolio"]


ticker_names = [tkr.symbol for tkr in portfolio.tickers]
selected_ticker_name = st.selectbox("Select Ticker to Hedge", ticker_names)
ticker = next(tkr for tkr in portfolio.tickers if tkr.symbol == selected_ticker_name)

# 2. Ask user for expected price move (%)
expected_move_pct = st.slider("Expected Move (to hedge against) (%)", -10.0, 10.0, 1.0, step=0.1) / 100


use_alt_hedge = st.checkbox("Hedge with a different equity?", value=False)

hedge_ticker = None
hedge_correlation = 1.0

if use_alt_hedge:
    hedge_ticker = st.text_input("Enter hedge equity ticker (e.g., SPY)", value="SPY")

    if hedge_ticker:
        try:
            # 2. Get close prices for both tickers
            hedge_data = yf.Ticker(hedge_ticker).history(
                period="3mo",
                interval="1d",
                auto_adjust=True,
                raise_errors=False
            )["Close"].dropna()
            main_data = ticker.historical_prices["Close"].dropna()

            

            # 3. Align lengths
            min_len = min(len(main_data), len(hedge_data))
            hedge_prices = hedge_data[-min_len:]
            main_prices = main_data[-min_len:]

            # 4. Compute correlation
            hedge_correlation = correlation.correlation(main_prices.tolist(), hedge_prices.tolist())
            st.markdown(f"**Correlation coefficient with {hedge_ticker}:** {hedge_correlation:.4f}")

        except Exception as e:
            st.error(f"Error computing correlation: {e}")
            use_alt_hedge = False
            hedge_correlation = 1.0

# --- Compute total Delta and Gamma ---
total_delta = sum(pos.delta for pos in ticker.positions)
total_gamma = sum(pos.gamma for pos in ticker.positions)
spot_price = ticker.current_price

st.markdown(f"**Current Price:** ${spot_price:.2f}")
st.markdown(f"**Expected Price:** ${(spot_price + (spot_price * expected_move_pct)):.2f}")
st.markdown(f"**Total Delta:** {total_delta:.2f}")
st.markdown(f"**Total Gamma:** {total_gamma:.2f}")

# --- Compute hedge ---
expected_move_dollars = spot_price * expected_move_pct
expected_delta_change = total_gamma * expected_move_dollars
future_delta = total_delta + expected_delta_change
hedge_shares = -future_delta

# If using alternate hedge, adjust shares by correlation and use that price
if use_alt_hedge and hedge_ticker and hedge_correlation != 0:
    hedge_shares /= hedge_correlation
    hedge_price = hedge_data.iloc[-1]  # last close of the hedge asset
else:
    hedge_price = spot_price  # hedge with same asset if no alt equity

st.markdown(f"**Expected Δ change (from Gamma):** {expected_delta_change:.2f}")

if use_alt_hedge:
    st.markdown(f"**Adjusted Hedge (in {hedge_ticker} shares):** {hedge_shares:.2f}")
else:
    st.markdown(f"**Required Hedge (in {ticker.symbol} shares):** {hedge_shares:.2f}")

# --- Graph: Realized Move vs PnL with Hedge ---
realized_moves = np.linspace(-0.1, 0.1, 200)  # ±10% range
pnl_no_hedge = []
pnl_with_hedge = []

for move_pct in realized_moves:
    dS = move_pct * spot_price

    # Original PnL: Delta + Gamma terms
    original_pnl = total_delta * dS + 0.5 * total_gamma * dS**2

    # Hedge PnL (always based on hedge price move, even for alt hedge)
    hedge_pnl = hedge_shares * (dS if not use_alt_hedge else dS * hedge_price / spot_price)

    pnl_no_hedge.append(original_pnl)
    pnl_with_hedge.append(original_pnl + hedge_pnl)

# --- Plot ---
fig, ax = plt.subplots()
ax.plot(realized_moves * 100, pnl_no_hedge, label="No Hedge")
ax.plot(realized_moves * 100, pnl_with_hedge, label="With Hedge")
ax.axvline(expected_move_pct * 100, color='gray', linestyle='--', label='Expected Move')

ax.set_xlabel("Realized Move (%)")
ax.set_ylabel("PnL ($)")
ax.set_title("PnL vs Realized Move")
ax.legend()
ax.grid(True)

st.pyplot(fig)