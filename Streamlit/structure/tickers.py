import yfinance as yf

class Ticker:
    def __init__(self, symbol: str, period: str = "1y", interval: str = "1d"):
        self.symbol = symbol.upper()
        self.ydata = yf.Ticker(self.symbol)

        # Fetch historical prices once
        self.historical_prices = self._fetch_history(period, interval)
        self.current_price = self._extract_latest_close()

        # Fetch options chain for the first available expiration date
        self.calls, self.puts = self._fetch_options()

    def _fetch_history(self, period, interval):
        try:
            return self.ydata.history(
                period=period,
                interval=interval,
                auto_adjust=True,
                raise_errors=False
            )
        except Exception as e:
            print(f"[Ticker:{self.symbol}] Error fetching history: {e}")
            return None

    def _extract_latest_close(self):
        if self.historical_prices is not None and not self.historical_prices.empty:
            return self.historical_prices["Close"].iloc[-1]
        return 0.0

    def _fetch_options(self):
        try:
            if not self.ydata.options:
                return None, None
            first_expiration = self.ydata.options[0]
            option_chain = self.ydata.option_chain(first_expiration)
            return option_chain.calls, option_chain.puts
        except Exception as e:
            print(f"[Ticker:{self.symbol}] Error fetching options: {e}")
            return None, None

    def summary(self):
        return {
            "Symbol": self.symbol,
            "Current Price": self.current_price,
            "Price History Rows": len(self.historical_prices) if self.historical_prices is not None else 0,
            "Options Available": self.calls is not None and self.puts is not None
        }

    def __repr__(self):
        return f"<Ticker {self.symbol} - ${self.current_price:.2f}>"
