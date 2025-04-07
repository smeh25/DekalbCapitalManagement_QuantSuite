import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from structure import Portfolio, StockPosition


st.set_page_config(page_title="📈 Portfolio Dashboard", layout="wide")
st.title("📊 Portfolio Performance Over the Past Year")

# Ensure portfolio is in session state
if "portfolio" not in st.session_state:
    st.error("No portfolio loaded. Please upload your file on the main page.")
    st.stop()

portfolio = st.session_state["portfolio"]

def plot_portfolio_performance(portfolio):
    combined_df = None

    for position in portfolio.positions:
        if isinstance(position, StockPosition):
            df = position.ticker.get_history(period="1y", interval="1d")
            if df is None or df.empty:
                continue

            # Multiply closing price by shares held
            value_series = df["Close"] * position.shares
            value_series.name = position.ticker.symbol  # Label for the column

            # Combine into one DataFrame
            if combined_df is None:
                combined_df = value_series.to_frame()
            else:
                combined_df = combined_df.join(value_series, how="outer")

    if combined_df is None or combined_df.empty:
        st.warning("No historical data found for any stock positions.")
        return

    combined_df.fillna(0, inplace=True)
    combined_df["Total Value"] = combined_df.sum(axis=1)

    # Plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=combined_df.index,
        y=combined_df["Total Value"],
        mode='lines',
        name='Total Portfolio Value',
        line=dict(width=3)
    ))

    fig.update_layout(
        title="Portfolio Value Over the Past Year",
        xaxis_title="Date",
        yaxis_title="Value (USD)",
        hovermode="x unified",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

# Plot the chart
plot_portfolio_performance(portfolio)
