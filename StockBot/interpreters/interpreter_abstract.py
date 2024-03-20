import json
from StockBot.program_structs.candle import Candle


class Interpreter:
    def chart_data(self) -> list:
        """Creates list of candles for database"""
        raise NotImplementedError

    @staticmethod
    def get_candle(message: json, period: int) -> Candle:
        raise NotImplementedError
