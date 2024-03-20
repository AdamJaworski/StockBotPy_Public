import json
from .command_factory_abstract import CommandFactory


class CommandFactoryXTB(CommandFactory):
    API_NAME = 'XTB'

    @staticmethod
    def create_command(command_name: str, arguments: dict) -> json:
        command = dict([('command', command_name), ('arguments', arguments)])
        return command

    def login(self, user_id: str, password: str) -> json:
        arguments = dict(userId=user_id, password=password, appName='Stock bot v1.0 made in Python by Adam Jaworski')
        return self.create_command('login', arguments)

    def logout(self) -> json:
        print("Logging off.")
        arguments = dict()
        return self.create_command('logout', arguments)

    def get_chart_data(self, chart: str, start_date: int, end_date: int, period: int):
        arguments = dict(info=dict(end=end_date, period=period, start=start_date, symbol=chart, ticks=0))
        return self.create_command('getChartRangeRequest', arguments)

    def get_all_symbols(self) -> json:
        arguments = dict()
        return self.create_command('getAllSymbols', arguments)

    def get_calendar(self) -> json:
        arguments = dict()
        return self.create_command('getCalendar', arguments)

    def get_chart_last_request(self, period: int, start: int, symbol: str) -> json:
        arguments = dict(period=period, start=start, symbol=symbol)
        return self.create_command('getCalendar', arguments)

    @staticmethod
    def get_candles(streamSessionId: str, symbol: str) -> json:
        return dict(command='getCandles', streamSessionId=streamSessionId, symbol=symbol)
