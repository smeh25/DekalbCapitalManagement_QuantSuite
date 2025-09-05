import asyncio
import zmq
import zmq.asyncio
import json
import random
import time
from datetime import datetime, timezone

ctx = zmq.asyncio.Context()

# sockets
input_socket = ctx.socket(zmq.PULL)   # where subs/orders arrive
input_socket.bind("tcp://127.0.0.1:5556")

output_socket = ctx.socket(zmq.PUB)   # where ticks are published
output_socket.bind("tcp://127.0.0.1:5555")


async def handle_incoming():
    while True:
        msg = await input_socket.recv_json()
        print(f"[INCOMING] {msg}")

        cmd = msg.get("command")
        if cmd == "SUBSCRIBE_MARKET_DATA":
            symbol = msg["payload"]["symbol"]

            # wait 1 second then send fake tick
            await asyncio.sleep(1)
            tick = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {
                    "symbol": symbol,
                    "price": round(random.uniform(100, 300), 2),
                    "size": random.choice([50, 100, 200])
                }
            }
            await output_socket.send_json(tick)
            print(f"[TICK SENT] {tick}")

        elif cmd == "CREATE_ORDER":
            # just log orders
            print(f"[ORDER RECEIVED] {msg}")

        else:
            print(f"[UNKNOWN CMD] {msg}")


async def main():
    print("ZMQ Test harness running...")
    print("Listening on tcp://127.0.0.1:5556, publishing on tcp://127.0.0.1:5555")
    await handle_incoming()


if __name__ == "__main__":
    asyncio.run(main())
