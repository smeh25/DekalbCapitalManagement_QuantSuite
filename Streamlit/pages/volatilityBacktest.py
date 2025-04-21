# app.py
import streamlit as st
from utils.indicators import supportedIndicators
from utils.backtestRunner import run_backtest
from structure import Ticker, Condition, GroupConditions
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import yfinance as yf


st.set_page_config(page_title="Strategy Builder", layout="wide")
st.title("Strategy Backtester")

# --- General Configuration ---
st.header("1 General Configuration")
col1, col2 = st.columns(2)
# with col1:
#     start_date = st.date_input("Start Date")
#     end_date = st.date_input("End Date")
# with col2:
initial_capital = st.number_input("Initial Portfolio Capital ($)", value=100000)
backtest_period = st.selectbox("Data Period", options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"], index=5)

# --- Buy Setup ---
st.header("2 Buy Conditions")
st.subheader("a. Buy Allocation")
buy_allocation = st.number_input("Max % of Portfolio to Allocate to Trade", min_value=0, max_value=100, value=10)

num_assets = st.number_input("How many assets in this trade?", min_value=1, step=1, value=1)
buy_assets = []
for i in range(num_assets):
    st.markdown(f"**Asset {i+1}**")
    col1, col2 = st.columns([2, 1])
    with col1:
        symbol = st.text_input(f"Ticker Symbol {i+1}", key=f"ticker_{i}")
    with col2:
        weight = st.number_input(f"Allocation % (must total 100%)", min_value=0, max_value=100, key=f"weight_{i}")
    buy_assets.append((symbol, weight))

st.subheader("b. Buy Conditions")
num_buy_conditions = st.number_input("Number of Buy Conditions", min_value=1, step=1, value=1)
buy_conditions = []
for i in range(num_buy_conditions):
    st.markdown(f"**Buy Condition {i+1}**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ticker = st.text_input(f"Condition {i+1} - Ticker", key=f"buy_cond_ticker_{i}")
    with col2:
        indicator = st.selectbox(f"Condition {i+1} - Indicator", supportedIndicators, key=f"buy_cond_ind_{i}")
    with col3:
        operator = st.selectbox(f"Condition {i+1} - Operator", ["<", "<=", "==", ">=", ">", "!="], key=f"buy_cond_op_{i}")
    with col4:
        value = st.number_input(f"Condition {i+1} - Value", key=f"buy_cond_val_{i}", step=0.1)
    buy_conditions.append((ticker, indicator, operator, value))

buy_relation = st.text_input("Logical Expression for Buy Conditions (e.g. (1 AND 2) OR 3)")

# --- Sell Setup ---
st.header("3 Sell Conditions")
num_sell_conditions = st.number_input("Number of Sell Conditions", min_value=1, step=1, value=1)
sell_conditions = []
for i in range(num_sell_conditions):
    st.markdown(f"**Sell Condition {i+1}**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        ticker = st.text_input(f"Sell Cond {i+1} - Ticker", key=f"sell_cond_ticker_{i}")
    with col2:
        indicator = st.selectbox(f"Sell Cond {i+1} - Indicator", supportedIndicators, key=f"sell_cond_ind_{i}")
    with col3:
        operator = st.selectbox(f"Sell Cond {i+1} - Operator", ["<", "<=", "==", ">=", ">", "!="], key=f"sell_cond_op_{i}")
    with col4:
        value = st.number_input(f"Sell Cond {i+1} - Value", key=f"sell_cond_val_{i}", step=0.1)
    sell_conditions.append((ticker, indicator, operator, value))

sell_relation = st.text_input("Logical Expression for Sell Conditions (e.g. 1 AND 2)")

# --- Submit ---
st.markdown("---")
simulate = st.button("🚀 Simulate Backtest")

if simulate:
    st.subheader("📊 Backtest Results")
    try:
        # Build Condition objects
        buy_cond_objs = [Condition(Ticker(t, period=backtest_period, interval="1d"), ind, op, val, backtest_period) for t, ind, op, val in buy_conditions]
        sell_cond_objs = [Condition(Ticker(t, period=backtest_period, interval="1d"), ind, op, val, backtest_period) for t, ind, op, val in sell_conditions]

        if num_buy_conditions == 1:
            buy_relation = "(1)"
        if num_sell_conditions == 1:
            sell_relation = "(1)"


        # Create GroupConditions
        buy_group = GroupConditions(buy_cond_objs, buy_relation)
        sell_group = GroupConditions(sell_cond_objs, sell_relation)

        # Use the first asset's ticker for now (can be extended later)
        ticker_symbol = buy_assets[0][0]
        ticker_obj = Ticker(ticker_symbol, backtest_period)

        # Run backtest
        trades_df = run_backtest(
            buy_signal=buy_group.boolData,
            sell_signal=sell_group.boolData,
            ticker_obj=ticker_obj,
            initial_cash=initial_capital,
            trade_pct=buy_allocation / 100
        )



        # --- Find trade intervals ---
        buy_dates = trades_df.index[trades_df["Buy"] == True]
        sell_dates = trades_df.index[trades_df["Sell"] == True]

        trade_regions = []
        profits = []

        for buy_date in buy_dates:
            sell_after = sell_dates[sell_dates > buy_date]
            if not sell_after.empty:
                sell_date = sell_after[0]
                start_val = trades_df.loc[buy_date]["Portfolio Value"]
                end_val = trades_df.loc[sell_date]["Portfolio Value"]
                pct_gain = ((end_val - start_val) / start_val) * 100
                profits.append(pct_gain)
                trade_regions.append((buy_date, sell_date, pct_gain))

        # --- Create Plotly Figure (Cleaned Up) ---
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trades_df.index,
            y=trades_df["Portfolio Value"],
            mode='lines',
            name='Portfolio Value',
            line=dict(color='blue')
        ))

        # Raw stock price
        stock_prices = ticker_obj.historical_prices["Close"]
        scaled_prices = stock_prices / stock_prices.iloc[0] * initial_capital

        fig.add_trace(go.Scatter(
            x=scaled_prices.index,
            y=scaled_prices,
            mode='lines',
            name=f"{ticker_obj.symbol} (Scaled)",
            line=dict(color='gray', dash='dot')
        ))


        # --- Add clean shaded regions ---
        for start, end, gain in trade_regions:
            color = 'green' if gain >= 0 else 'red'
            fig.add_vrect(
                x0=start,
                x1=end,
                fillcolor=color,
                opacity=0.2,
                layer="below",
                line_width=0
            )

        fig.update_layout(
            title="📈 Portfolio Value Over Time",
            height=500,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=False,
            xaxis_title="Date",
            yaxis_title="Portfolio Value"
        )

        st.plotly_chart(fig, use_container_width=True)

        # --- Histogram of Trade Returns ---
        if profits:
            hist_fig = px.histogram(
                profits,
                nbins=20,
                title="📉 Distribution of Trade Returns",
                labels={'value': 'Return per Trade (%)'},
                opacity=0.75
            )
            hist_fig.update_layout(
                xaxis_title="Trade Return (%)",
                yaxis_title="Frequency",
                bargap=0.1,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(hist_fig, use_container_width=True)
        else:
            st.info("No completed trades to display in histogram.")

        # --- Metrics ---
        max_gain = max(profits) if profits else 0
        max_loss = min(profits) if profits else 0
        num_trades = len(profits)

        # Total return from first to last day
        start_value = trades_df["Portfolio Value"].iloc[0]
        end_value = trades_df["Portfolio Value"].iloc[-1]
        total_return = ((end_value - start_value) / start_value) * 100

        spy = Ticker("^GSPC", backtest_period)
        spy_prices = spy.historical_prices["Close"]

        # Your strategy's daily returns
        portfolio_returns = trades_df["Portfolio Value"].pct_change()

        # S&P 500 daily returns
        spy_returns = spy_prices.pct_change()

        # Align both series
        combined = pd.concat([portfolio_returns, spy_returns], axis=1)
        combined.columns = ["Portfolio", "SPY"]
        combined.dropna(inplace=True)
        correlation = combined["Portfolio"].corr(combined["SPY"])


        metrics_df = pd.DataFrame({
            "Metric": [
                "Total Return (%)",
                "Most Profitable Trade (%)",
                "Biggest Loss Trade (%)",
                "Total Trades",
                "Correlation w S&P"
            ],
            "Value": [
                f"{total_return:.2f}",
                f"{max_gain:.2f}",
                f"{max_loss:.2f}",
                num_trades,
                correlation
            ]
        })

        st.subheader("📊 Backtest Metrics")
        st.table(metrics_df)

        st.dataframe(trades_df)




    except Exception as e:
        st.error(f"❌ Backtest failed: {e}")