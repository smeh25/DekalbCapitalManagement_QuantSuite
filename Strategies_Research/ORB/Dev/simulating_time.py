import numpy as np
import pandas as pd
from datetime import datetime, timezone

async def collect_opening_range(start_time, n_minutes, data_stream):
    """
    Collects open, close, high, low prices for the n-minute window
    starting from start_time, based on timestamps in incoming data.
    
    Args:
        start_time: timestamp object
        n_minutes: duration in minutes
        data_stream: async generator yielding (timestamp, price)
    
    Returns:
        (Open, Close, nH, nL)
    """

    Open, Close, nH, nL = None, None, None, None

    if isinstance(start_time, datetime):
        start_time = start_time.timestamp()  # Convert to timestamp if datetime   
    
    end_time = start_time + (n_minutes * 60)
 
    async for timestamp, price in data_stream:
        if timestamp < start_time:
            continue
        if timestamp >= end_time:
            break

        if Open is None:
            Open = price
            nH, nL = price, price

        nH = max(nH, price)
        nL = min(nL, price)
        Close = price

    return Open, Close, nH, nL



def get_orb_order(Open, Close, nH, nL):
    """
    Determines trade signal from ORB logic.
    """
    if Close > Open:
        return f"BUY stop order @ {nH}"
    elif Close < Open:
        return f"SELL stop order @ {nL}"
    else:
        return "No trade — C == O"



import time

async def create_data(start_time, end_time, tick_size=60):
    """
    Simulates async tick stream with epoch timestamps.
    Args:
        start_time: starting timestamp in seconds
        end_time: ending timestamp in seconds
        tick_size: interval in seconds for each tick (default 60 seconds)
    """


    while start_time <= end_time:
        price_str = input(f"Enter next price at {time.strftime('%H:%M:%S', time.gmtime(start_time))}: ")
        try:
            price = float(price_str)
        except ValueError:
            print("Invalid input, please enter a number.")
            continue

        yield start_time, price
        start_time += tick_size



async def main():
    start_dt = datetime(2025, 8, 12, 9, 30, 0, tzinfo=timezone.utc)
    start_time = start_dt.timestamp()
    end_time = start_time + (5*60)  # 5 minutes later

    data_stream = create_data(start_time, end_time, tick_size=60)
    Open, Close, nH, nL = await collect_opening_range(start_time, 5, data_stream)

    if Open is not None and Close is not None and nH is not None and nL is not None:
        order = get_orb_order(Open, Close, nH, nL)
        print(f"Order signal: {order}")
    else:
        print("No valid data collected for ORB.")


import asyncio

if __name__ == "__main__":
    asyncio.run(main())