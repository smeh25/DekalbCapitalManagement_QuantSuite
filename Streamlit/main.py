import streamlit as st
import pandas as pd
from utils.csvFormat import validate_csv
import os
from datetime import datetime
import time
from utils.fidelity_parse import parse_fidelity_csv


st.set_page_config(page_title="Financial Dashboard", layout="wide")

st.title("📊 Upload Your Portfolio CSV")

st.markdown("""
Welcome to your personal financial dashboard!  
To get started:

1. Download or prepare a CSV file with your stock and/or option holdings.
2. Use the following format:

**CSV Columns:**
- `Type`: `stock` or `option`
- `Ticker`: Stock or option symbol (e.g., AAPL, TSLA)
- `Shares`: Number of shares or contracts
- `Expiration`: *(Only for options)* Expiration date in YYYY-MM-DD format
- `Strike`: *(Only for options)* Strike price
- `Option Type`: *(Only for options)* `call` or `put`

**Example:**
```csv
Type,Ticker,Shares,Expiration,Strike,Option Type
stock,AAPL,10,,,
option,TSLA,2,2024-06-21,250,call
            
""")

# Choose CSV Format
csv_type = st.selectbox(
    "📂 What kind of CSV are you uploading?",
    ["Fidelity Export", "Pre-Formatted"]
)

# Upload CSV
uploaded_file = st.file_uploader("📁 Upload your portfolio CSV file", type=["csv"])

# Confirmation Button
if uploaded_file:
    if st.button("📤 Upload Selected File"):
        try:
            df = pd.read_csv(uploaded_file)

            # If Fidelity format, parse it first
            if csv_type == "Fidelity Export":
                df = parse_fidelity_csv(df)
            
            is_valid, errors = validate_csv(df)

            if is_valid:
                st.success("✅ CSV uploaded and validated successfully!")
                st.dataframe(df)

                # Define paths
                SAVE_DIR = "raw_data"
                ARCHIVE_DIR = os.path.join(SAVE_DIR, "archive")
                FILENAME = "uploadedInformation.csv"
                FULL_PATH = os.path.join(SAVE_DIR, FILENAME)

                # Archive old file if it exists
                if os.path.exists(FULL_PATH):
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    archived_name = f"uploadedInformation_{timestamp}.csv"
                    archived_path = os.path.join(ARCHIVE_DIR, archived_name)
                    os.rename(FULL_PATH, archived_path)
                    st.info(f"📁 Existing file archived as `{archived_name}`")

                # Save the new upload
                df.to_csv(FULL_PATH, index=False)
                # st.success("File successfully saved as `uploadedInformation.csv` in `raw_data/.` Rerouting to dashboard…")

                # # Optional: wait for 1.5 seconds so user sees the success message
                # time.sleep(1.5)
                st.switch_page("pages/processing.py")
            else:
                st.error("❌ There were issues with your CSV:")
                for err in errors:
                    st.markdown(f"- {err}")

        except Exception as e:
            st.error(f"⚠️ Error reading CSV: {e}")



# if uploaded_file:
#     try:
#         df = pd.read_csv(uploaded_file)
#         is_valid, errors = validate_csv(df)

#         if is_valid:
#             st.success("✅ CSV uploaded and validated successfully!")
#             st.dataframe(df)

#             # Define paths
#             SAVE_DIR = "raw_data"
#             ARCHIVE_DIR = os.path.join(SAVE_DIR, "archive")
#             FILENAME = "uploadedInformation.csv"
#             FULL_PATH = os.path.join(SAVE_DIR, FILENAME)

#             # Archive old file if it exists
#             if os.path.exists(FULL_PATH):
#                 timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#                 archived_name = f"uploadedInformation_{timestamp}.csv"
#                 archived_path = os.path.join(ARCHIVE_DIR, archived_name)
#                 os.rename(FULL_PATH, archived_path)
#                 st.info(f"📁 Existing file archived as `{archived_name}`")

#             # Save the new upload
#             df.to_csv(FULL_PATH, index=False)
#             # st.success("File successfully saved as `uploadedInformation.csv` in `raw_data/.` Rerouting to dashboard…")

#             # # Optional: wait for 1.5 seconds so user sees the success message
#             # time.sleep(1.5)
#             st.switch_page("pages/processing.py")
#         else:
#             st.error("❌ There were issues with your CSV:")
#             for err in errors:
#                 st.markdown(f"- {err}")

#     except Exception as e:
#         st.error(f"⚠️ Error reading CSV: {e}")

