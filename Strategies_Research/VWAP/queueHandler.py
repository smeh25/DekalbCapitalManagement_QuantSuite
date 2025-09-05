# Run this file and it will execture VWAP based on input from the config file
# This is setup in more of oop style because we need static variables
import vwap_async as vp
import zmq
import zmq.asyncio
import asyncio
  
queues = {}



def on_tick(tick: dict):
    price = tick["data"]["price"]
    symbol = tick["data"]["symbol"]

    if symbol in queues:
        # Push the price into the correct queue
        queues[symbol].put_nowait(price)
    else:
        print(f"[WARN] No queue registered for {symbol}")

    return


async def register_task(symbol, vwap, place_order):

    if symbol not in queues:
        queues[symbol] = asyncio.Queue()

    queue = queues[symbol]

    # If you want to do this for a continous amount of ticks, place this inside a while true
    current_price = await queue.get()
    result = await vp.vwapCheck(symbol, current_price, vwap)
    place_order(result) # Need to import from trading engine 
    return



# Read config details
import json
import os
import sys
def load_config(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Configuration file not found at: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
        return config
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {filepath}: {e}")
        sys.exit(1)



def initialize(config, place_order):
    # List all of the stocks to run the VWAP for in the main method, I would like to make this a parameter, lets discuss
    # config_file_path = 'config.json'
    # config = load_config(config_file_path)
    stocks = config["stocks"]
    days = config["days"]
    tasks = []
    
    vwaps = {}
    for stock in stocks:
        history = vp.getVWAPSpecificData(stock, days)
        vwaps[stock] = vp.computeVWAP(history).iloc[-1]
        tasks.append(register_task(stock, vwap=vwaps[stock], place_order=place_order))

        # asyncio.create_task(register_task(stock, vwap=vwaps[stock], place_order= place_order))
    return tasks
    
    
    """
    1) define list of stocks
    2) for each stock compute the VWAP
    3) run the vwapCheck method. Implement return values from ontick as the session continues, and with each value, call the checkVWAP method. Have the return be the json object
    4) place order 
    5) Attempt to parallelize each item
    """
    