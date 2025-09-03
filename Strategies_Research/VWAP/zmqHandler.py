import asyncio
import zmq
import zmq.asyncio
import json
import Strategies_Research.VWAP.queueHandler as queueHandler   # import your strategy logic

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

    # start event loop
    loop = asyncio.get_event_loop()
    loop.create_task(tick_listener(tick_socket))
    loop.run_forever()


if __name__ == "__main__":
    main()
