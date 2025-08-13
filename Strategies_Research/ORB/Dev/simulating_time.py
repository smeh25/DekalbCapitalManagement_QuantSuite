from orb import collect_opening_range, get_orb_order
from datetime import datetime, timezone

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