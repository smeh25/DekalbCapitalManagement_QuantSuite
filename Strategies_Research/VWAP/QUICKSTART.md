# VWAP Trading Algorithm

This project provides utilities for **calculating VWAP (Volume Weighted Average Price)** using historical stock data and then checking for trade signals at the market open asynchronously. Read the below documentation to understand the methods and see some example implementations.

---

## Helper Methods

Located within *vwap.py*:

#### `getVWAPSpecificData(ticker: str, days: int) -> pd.DataFrame`
Fetches historical stock data for a given ticker symbol over the last `days` days which is then used to calculate VWAP. 

**Returns:**
The method returns a *pd.DataFrame* with columns
- `Date` (index)
- `Open`
- `High`
- `Low`
- `Close`
- `Volume`
- `Dividends`
- `Stock Splits`

#### `computeVWAP(history: pd.DataFrame) -> pd.Series`
Calculated the VWAP (Volume Weighted Average Price) using historical price data

**Parameters:**
- `history` *(pd.DataFrame)*: Historical stock data. **Required columns:**
  - `High` — daily high price
  - `Low` — daily low price
  - `Close` — daily closing price
  - `Volume` — trading volume

**Returns:**
- `pd.Series` — a single column containing the VWAP for each row in the input DataFrame.  
  This Series can be added to the original DataFrame as a new column if desired, e.g., `history['VWAP'] = computeVWAP(history)`.

---

## Main Method

#### `vwapCheck(current: Union[float, Awaitable[float]], vwap: float, is_async: bool)`
Outputs a trading signal based on comparson of the current market price of a stock to its VWAP. The function supports both **regular float prices** and **asynchronous price objects**.
**Note:** The output is expected to be a json object that corresponds to a market order. For now it is not complete and simply prints the action to console

**Parameters:**
- `current` — The current price to compare against the VWAP. Can be either:
  - **float** — a regular numeric price if `is_async=False`
  - **awaitable / coroutine** — an async object returning a numeric price if `is_async=True`
- `vwap` *(float)* — The VWAP reference price.
- `is_async` *(bool)* — Whether `current` is an async object that needs to be awaited.


**Async Example**

```python
import asyncio
async def get_price():
    # Implement the market stream to retrieve the current price
    price = 125
    return price

asyncio.run(vwapCheck(get_price(), 120, is_async=True))
```

**Example Using Helper Methods**
```python
historyAAPL = getVWAPSpecificData("AAPL", 5)
historyAAPL["VWAP"] = computeVWAP(historyAAPL)
lastVwap = historyAAPL["VWAP"].iloc[-1]
vwapCheck(229.25, lastVwap)
```


