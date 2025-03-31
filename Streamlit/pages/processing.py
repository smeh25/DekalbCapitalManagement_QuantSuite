import streamlit as st
import pandas as pd
import os
import time

from structure import Ticker, Portfolio, StockPosition, OptionPosition

st.set_page_config(page_title="Loading Portfolio...")

st.title("✅ File Uploaded Successfully")
st.markdown("We're now retrieving financial data and building your portfolio. Please wait...")

# Optional short pause to show message
time.sleep(1)

# Step 1: Load the saved CSV
csv_path = os.path.join("raw_data", "uploadedInformation.csv")

try:
    df = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"❌ Failed to read uploaded file: {e}")
    st.stop()

# Step 2: Create Portfolio
portfolio = Portfolio()

# Step 3: Store in session
st.session_state["portfolio"] = portfolio

# Countdown
for seconds_left in range(2, 0, -1):
    st.info(f"🔁 Redirecting to dashboard in {seconds_left} second(s)...")
    time.sleep(1)

# Step 4: Redirect to dashboard
st.switch_page("pages/dashboard.py")
