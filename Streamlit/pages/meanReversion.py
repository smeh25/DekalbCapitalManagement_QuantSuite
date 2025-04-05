import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from structure import Ticker  # Replace with correct import path
import plotly.graph_objects as go
import plotly.express as px

st.title("Mean Reversion Model")

# Inputs
symbol = st.text_input("Enter Ticker Symbol", value="UVXY")
pct_threshold = st.number_input("Enter Daily % Return Threshold (can be negative)", value=10.0)

if st.button("Run Model"):
    # Initialize Ticker object and get historical data
    ticker = Ticker(symbol)
    df = ticker.historical_prices[["Open", "Close"]].copy()
    df["Date"] = df.index
    df.reset_index(drop=True, inplace=True)

    # Calculate same-day percent return
    df["Daily Return %"] = ((df["Close"] - df["Open"]) / df["Open"]) * 100

    # Filter threshold-crossing days
    if pct_threshold > 0:
        trigger_days = df[df["Daily Return %"] >= pct_threshold]
    else:
        trigger_days = df[df["Daily Return %"] <= pct_threshold]

    reversion_data = []

    for idx in trigger_days.index:
        open_price = df.loc[idx, "Open"]
        close_price = df.loc[idx, "Close"]
        return_pct = ((close_price - open_price) / open_price) * 100
        trigger_date = df.loc[idx, "Date"]

        for fwd_idx in range(idx + 1, len(df)):
            fwd_close = df.loc[fwd_idx, "Close"]
            fwd_date = df.loc[fwd_idx, "Date"]

            if pct_threshold > 0 and fwd_close < open_price:
                reversion_data.append({
                    "Start Date": trigger_date,
                    "Start Open": open_price,
                    "Start Close": close_price,
                    "Return %": return_pct,
                    "Return Date": fwd_date,
                    "Return Close": fwd_close,
                    "Days to Revert": (fwd_date - trigger_date).days
                })
                break
            elif pct_threshold < 0 and fwd_close > open_price:
                reversion_data.append({
                    "Start Date": trigger_date,
                    "Start Open": open_price,
                    "Start Close": close_price,
                    "Return %": return_pct,
                    "Return Date": fwd_date,
                    "Return Close": fwd_close,
                    "Days to Revert": (fwd_date - trigger_date).days
                })
                break

    result_df = pd.DataFrame(reversion_data)

    if not result_df.empty:
        st.subheader("📈 Stock Time Series and Trigger Threshold")

        # 1. Close Price Over Time
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            name="Close Price",
            line=dict(color='blue')
        ))
        fig_price.update_layout(
            title=f"{symbol} Close Price Over Time",
            xaxis_title="Date",
            yaxis_title="Close Price",
            height=400
        )
        st.plotly_chart(fig_price, use_container_width=True)

        # 2. Daily Return % Over Time
        fig_return = go.Figure()
        fig_return.add_trace(go.Scatter(
            x=df["Date"],
            y=df["Daily Return %"],
            mode="lines",
            name="Daily Return %",
            line=dict(color='orange')
        ))
        fig_return.add_shape(
            type="line",
            x0=df["Date"].min(),
            y0=pct_threshold,
            x1=df["Date"].max(),
            y1=pct_threshold,
            line=dict(color="red", width=2, dash="dash"),
            name="Threshold"
        )
        fig_return.update_layout(
            title=f"{symbol} Daily Return % Over Time",
            xaxis_title="Date",
            yaxis_title="Daily Return %",
            height=400
        )
        st.plotly_chart(fig_return, use_container_width=True)

        # 3. Reversion Table
        st.subheader("📊 Reversion Statistics Table")
        st.dataframe(result_df.style.format({
            "Start Open": "{:.2f}",
            "Start Close": "{:.2f}",
            "Return %": "{:.2f}",
            "Return Close": "{:.2f}",
            "Days to Revert": "{:.0f}"
        }), use_container_width=True)

        # 4. Histogram of Days to Revert
        st.subheader("📈 Histogram of Days to Revert")
        fig_hist = px.histogram(result_df, x="Days to Revert")
        fig_hist.update_traces(xbins=dict(size=5))  # Set bin width to 5
        fig_hist.update_layout(
            xaxis_title="Days to Revert",
            yaxis_title="Frequency",
            height=400
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        # 5. Key Metrics
        st.subheader("📌 Key Metrics")
        st.write(f"**Average Days to Revert:** {result_df['Days to Revert'].mean():.2f}")
        st.write(f"**Total Events Detected:** {len(result_df)}")

    else:
        st.warning("No reversion events detected. Try a different threshold or stock.")


    # if not result_df.empty:
    #         # Show two charts side-by-side
    #     st.subheader("📈 Stock Time Series and Trigger Threshold")

    #     col1, col2 = st.columns(2)

    #     with col1:
    #         st.markdown("**Stock Close Price Over Time**")
    #         fig_price, ax1 = plt.subplots()
    #         ax1.plot(df["Date"], df["Close"], color='blue', label="Close Price")
    #         ax1.set_xlabel("Date")
    #         ax1.set_ylabel("Close Price")
    #         ax1.set_title(f"{symbol} Close Price")
    #         ax1.tick_params(axis='x', rotation=45)
    #         ax1.grid(True)
    #         st.pyplot(fig_price)

    #     with col2:
    #         st.markdown("**Daily Return % Over Time**")
    #         fig_return, ax2 = plt.subplots()
    #         ax2.plot(df["Date"], df["Daily Return %"], color='orange', label="Daily Return %")
    #         ax2.axhline(y=pct_threshold, linestyle='--', color='red', label="Threshold")
    #         ax2.set_xlabel("Date")
    #         ax2.set_ylabel("Daily Return %")
    #         ax2.set_title(f"{symbol} Daily Returns")
    #         ax2.tick_params(axis='x', rotation=45)
    #         ax2.grid(True)
    #         ax2.legend()
    #         st.pyplot(fig_return)



    #     st.subheader("📊 Reversion Statistics Table")
    #     st.dataframe(result_df)

    #     st.subheader("📈 Histogram of Days to Revert")
    #     fig, ax = plt.subplots()
    #     result_df['Days to Revert'].hist(ax=ax, bins=20)
    #     ax.set_xlabel("Days to Revert")
    #     ax.set_ylabel("Frequency")
    #     st.pyplot(fig)

    #     st.subheader("📌 Key Metrics")
    #     st.write(f"Average Days to Revert: {result_df['Days to Revert'].mean():.2f}")
    #     st.write(f"Total Events Detected: {len(result_df)}")

    #     st.subheader("📉 Sample Time Series")
    #     sample = result_df.head(1)
    #     if not sample.empty:
    #         start_date = sample.iloc[0]['Start Date']
    #         end_date = sample.iloc[0]['Return Date']
    #         time_series = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    #         fig2, ax2 = plt.subplots()
    #         ax2.plot(time_series['Date'], time_series['Close'], marker='o', label="Close Price")
    #         ax2.axhline(y=df[df["Date"] == start_date]["Open"].values[0], color='red', linestyle='--', label='Trigger Open Price')
    #         ax2.set_title("Price Reversion After Trigger")
    #         ax2.set_ylabel("Close Price")
    #         ax2.legend()
    #         st.pyplot(fig2)

    # else:
    #     st.warning("No reversion events detected. Try a different threshold or stock.")
