class Candle:
    """Structure for candle"""
    open_time:   int
    close_time:  int
    open_price:  float
    close_price: float
    max_price:   float
    min_price:   float
    volume:      int
    symbol:      str

    def __init__(self, open_time: int, close_time: int, open_price: float, close_price: float,
                 max_price: float, min_price: float, volume: int, symbol: str):
        self.open_time    = open_time
        self.close_time   = close_time
        self.open_price   = open_price
        self.close_price  = close_price
        self.max_price    = max_price
        self.min_price    = min_price
        self.volume       = volume
        self.symbol       = symbol

    def __str__(self):
        return f"Candle: open_time - {self.open_time}, close_time - {self.close_time}, "  \
               f"open_price - {self.open_price}, close_price - {self.close_price}, "      \
               f"max_price - {self.max_price}, min_price - {self.min_price}, "            \
               f"volume - {self.volume}, stock -  {self.symbol}"


