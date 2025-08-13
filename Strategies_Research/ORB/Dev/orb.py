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
        return f"LONG with stop order price of {nH}"
    elif Close < Open:
        return f"SHORT stop order price of {nL}"
    else:
        return "No trade. Close = Open"
