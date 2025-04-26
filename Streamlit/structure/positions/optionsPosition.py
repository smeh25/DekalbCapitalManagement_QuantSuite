from structure.positions.base import Position
import numpy as np
import yfinance as yf
from scipy.stats import norm
from datetime import datetime


class OptionPosition(Position):
    def __init__(self, ticker, shares, expiration, strike, option_type):
        super().__init__(ticker, shares)
        self.expiration = expiration
        self.strike = strike
        self.option_type = option_type
        self.current_price, self.iv = self.market_value()
        self.delta, self.gamma, self.vega, self.theta, self.rho = self.greeks_blackscholes(ticker.current_price,
                                                                                            strike,
                                                                                            self.time_to_maturity(expiration),
                                                                                            self.iv, option_type)
    def time_to_maturity(self, exp):
        today = datetime.today()
        expiration_date = datetime.strptime(exp, "%Y-%m-%d")
        
        delta = expiration_date - today
        days_to_maturity = delta.days + delta.seconds / (24 * 3600)
        
        # Assuming 365 days per year (you could use 365.25 if you want to adjust for leap years)
        return days_to_maturity / 365

    def market_value(self):
        df = self.ticker.calls if self.option_type == "call" else self.ticker.puts
        if df is not None:
            row = df[df["strike"] == self.strike]
            if not row.empty:
                last_price = row["lastPrice"].iloc[0]
                return self.shares * 100 * last_price, row["impliedVolatility"].squeeze()
        return 0.0, 0.0

    def greeks_blackscholes(self, S, K, T, sigma, option_type):
        """
        S: Spot Price 
        K: Strike
        T: TTM (years)
        r: risk-free ( will grab from bond rates)
        sig: IV
        """

        irx = yf.Ticker("^IRX")
        hist = irx.history(period="1d")

        if hist.empty:
            raise ValueError("Could not fetch ^IRX data from Yahoo Finance.")
        
        # The rate is annualized and in percent, so convert it to decimal
        r = hist["Close"].iloc[-1] / 100
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option_type == 'call':
            delta = norm.cdf(d1)
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) -
                    r * K * np.exp(-r * T) * norm.cdf(d2))
            rho = K * T * np.exp(-r * T) * norm.cdf(d2)
        else:  
            delta = -norm.cdf(-d1)
            theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) +
                    r * K * np.exp(-r * T) * norm.cdf(-d2))
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T)

        return delta, gamma, vega / 100,  theta / 365,  rho / 100

    def __repr__(self):
        return (f"<Option: {self.ticker.symbol} {self.option_type.upper()} "
                f"{self.strike} x {self.shares} @ {self.expiration}>")
