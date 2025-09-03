import asyncio
import zmq
import zmq.asyncio
import json
import queueHandler   # import your strategy logic

ctx = zmq.asyncio.Context()


def make_order_socket(address: str):
    sock = ctx.socket(zmq.PUSH)
    sock.connect(address)
    return sock


def make_tick_socket(address: str):
    sock = ctx.socket(zmq.SUB)
    sock.connect(address)
    sock.setsockopt_string(zmq.SUBSCRIBE, "")  # subscribe to all
    return sock


async def tick_listener(tick_socket):
    while True:
        msg = await tick_socket.recv_json()
        queueHandler.on_tick(msg)

import json
import uuid
from datetime import datetime, timezone

def subscribe(order_socket, tickers: list[str]):

    for symbol in tickers:
        payload = {
            "command": "SUBSCRIBE_MARKET_DATA",
            "correlation_id": str(uuid.uuid4()),  # unique ID per request
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {
                "symbol": symbol,
                "data_types": ["TICK"]
            }
        }
        order_socket.send_json(payload)
        print(f"[SUBSCRIBE] Sent subscription for {symbol}")


def main():
    # load config
    with open("config.json", "r") as f:
        config = json.load(f)

    # setup sockets from config
    tick_socket = make_tick_socket(config["tickSocket"])
    order_socket = make_order_socket(config["outputSocket"])

    # define sync place_order for queueHandler
    def place_order(order: dict):
        order_socket.send_json(order)  # blocking send is fine here
        print(f"[ORDER SENT] {order}")

    # start strategy (sync call)
    queueHandler.initialize(config, place_order)

    tickers = config["stocks"]
    subscribe(order_socket, tickers)

    # start event loop
    loop = asyncio.get_event_loop()
    loop.create_task(tick_listener(tick_socket))
    loop.run_forever()


if __name__ == "__main__":
    main()
