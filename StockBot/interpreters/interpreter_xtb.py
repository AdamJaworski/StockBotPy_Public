from .interpreter_abstract import Interpreter
from StockBot.program_structs.candle import Candle
from StockBot.managers.time_manager import TimeManager
import json


class InterpreterXTB(Interpreter):

    def chart_data(self) -> list:
        pass

    @staticmethod
    def stream_session_id(login_output: json) -> str:
        return login_output["streamSessionId"]

    @staticmethod
    def get_candle(message: json, period: int, symbol=None) -> Candle:
        if symbol is None:
            symbol = message['symbol']
        return Candle(message['ctm'], (TimeManager.add(int(message['ctm']), adding_minutes=period)), message['open'],
                      message['close'], message['high'], message['low'], message['vol'], symbol)

