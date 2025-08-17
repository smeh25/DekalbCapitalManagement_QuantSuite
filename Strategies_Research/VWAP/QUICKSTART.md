# VWAP Trading Algorithm

This project provides utilities for **calculating VWAP (Volume Weighted Average Price)** using historical stock data and then checking for trade signals at the market open asynchronously. Read the below documentation to understand the methods and see some example implementations.

---

## Methods

Located within *vwap.py*:

### `getVWAPSpecificData(ticker: str, days: int) -> pd.DataFrame`
Fetches historical stock data for a given ticker symbol over the last `days` days which is then used to calculate VWAP. The method returns a pandas dataframe with columns
- `Date` (index)
- `Open`
- `High`
- `Low`
- `Close`
- `Volume`
- `Dividends`
- `Stock Splits`

### `computeVWAP(history: pd.DataFrame) -> pd.Series`

**Parameters:**
- `history` *(pd.DataFrame)*: Historical stock data. **Required columns:**
  - `High` — daily high price
  - `Low` — daily low price
  - `Close` — daily closing price
  - `Volume` — trading volume

**Returns:**
- `pd.Series` — a single column containing the VWAP for each row in the input DataFrame.  
  This Series can be added to the original DataFrame as a new column if desired, e.g., `history['VWAP'] = computeVWAP(history)`.




