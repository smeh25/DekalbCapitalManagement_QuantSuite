import asyncio
import zmq
import zmq.asyncio
import vwap_async as vp
import uuid
from datetime import datetime, timezone

class VWAPRunner:
    def __init__(self, ticker: str, days: int, zmq_in_port: int, zmq_out_port: int):
        self.ticker = ticker
        self.days = days
        self.vwap = None

        # Setup ZMQ context
        self.ctx = zmq.asyncio.Context()

        # Incoming ticks (SUB)
        self.sub_socket = self.ctx.socket(zmq.SUB)
        self.sub_socket.connect(f"tcp://127.0.0.1:{zmq_in_port}") # 5555
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        # Outgoing orders (PUB)
        self.pub_socket = self.ctx.socket(zmq.PUB)
        self.pub_socket.connect(f"tcp://127.0.0.1:{zmq_out_port}")

    def initialize(self):
        """Compute VWAP for the stock at startup."""
        history = vp.getVWAPSpecificData(self.ticker, self.days)
        self.vwap = vp.computeVWAP(history).iloc[-1]
        print(f"[INIT] {self.ticker} VWAP = {self.vwap:.2f}")

    async def on_tick(self, tick: dict):
        """Handle a single tick from ZMQ."""
        price = tick["data"]["price"]
        symbol = tick["data"]["symbol"]

        order = vp.vwapCheck(symbol, price, self.vwap)
        if order:
            await self.place_order(order)

    async def place_order(self, order: dict):
        """Send order to outbound PUB socket."""
        await self.pub_socket.send_json(order)
        print(f"[ORDER SENT] {order}")



    async def listen(self):
        """Subscribe to market data and then listen for ticks."""
        # --- send subscription request ---
        payload = {
            "command": "SUBSCRIBE_MARKET_DATA",
            "correlation_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {
                "symbol": self.ticker,
                "data_types": ["TICK"]
            }
        }
        self.pub_socket.send_json(payload)
        print(f"[SUBSCRIBE] Sent subscription for {self.ticker}")

        # --- listen loop for ticks ---
        print(f"[LISTENING] ticks on {self.ticker}...")
        while True:
            msg = await self.sub_socket.recv_json()
            print(f"[TICK RECEIVED] {msg}")
            await self.on_tick(msg)



async def main():
    runner = VWAPRunner(ticker="AAPL", days=5, zmq_in_port=5555, zmq_out_port=5556)
    runner.initialize()
    await runner.listen()


if __name__ == "__main__":
    asyncio.run(main())
