from StockBot.managers.connection_ssl_app import ConnectionSSLAPP
from StockBot.managers.connection_ws_app import ConnectionWSAPP
from StockBot.managers.connection_abstract import ConnectionManager
from StockBot.managers.dir_manager import PathManager
from StockBot.managers.db_manager import Database
from StockBot.utilities.logger_setup import setup_logger
from StockBot.utilities.db_state_dict import create_state_dict
from StockBot.utilities.dir_chekcer import check_all
from StockBot.values import values
from StockBot.values.host_values import HOSTS
from StockBot.program_structs.candle import Candle
from StockBot.factory import table_factory
from StockBot.factory.command_factory_interface import COMMAND_FACTORY
from StockBot.interpreters.interpreters_interface import INTERPRETERS
from StockBot.interpreters.stream_interpreter_xtb import STREAM
from pathlib import Path
import asyncio
import threading
import json
import time


class User:
    host: str
    dir_manager: PathManager
    connection: ConnectionManager
    state_dict: dict
    commands: COMMAND_FACTORY
    interpreter: INTERPRETERS

    def __init__(self, debug: bool, files_dir: Path, host: str):
        self.host = host
        self.dir_manager = PathManager(files_dir)
        if debug:
            setup_logger(self.dir_manager.logger_dir)

        # Setting up state dict
        asyncio.run(self.create_state_dict())

        # Commands handling
        self.commands = COMMAND_FACTORY[self.host]()
        self.interpreter = INTERPRETERS[self.host]()

        # Connection manager
        if HOSTS[self.host].DEFAULT_CONNECTION_MANAGER == "ssl":
            self.connection = ConnectionSSLAPP((HOSTS[self.host].HOST, HOSTS[self.host].CLIENT_PORT_DEMO),
                                            (HOSTS[self.host].HOST, HOSTS[self.host].STREAMING_PORT_DEMO), HOSTS[self.host].HOST)
        if HOSTS[self.host].DEFAULT_CONNECTION_MANAGER == "ws":
            self.connection = ConnectionWSAPP(HOSTS[self.host].CLIENT_WEB_SOCKET_DEMO,
                                           HOSTS[self.host].STREAMING_WEB_SOCKET_DEMO, self.host)
        time.sleep(0.7)
        self.login()
        threading.Thread(target=self.stream).start()

    def login(self) -> None:
        """Log into API and assign stream session id to host value"""
        self.connection.send_client(self.commands.login(HOSTS[self.host].USER_ID, HOSTS[self.host].PASSWORD))
        while self.connection.client_queue.empty():
            continue
        HOSTS[self.host].STREAM_SESSION_ID = self.interpreter.stream_session_id(self.connection.client_queue.get())
        print(HOSTS[self.host].STREAM_SESSION_ID)

    def subscribe(self, stock: str) -> None:
        """Sings up for """
        self.connection.send_stream(self.commands.get_candles(HOSTS[self.host].STREAM_SESSION_ID,
                                                              HOSTS[self.host].STOCKS[stock]))

    def subscribe_all(self) -> None:
        for stock in HOSTS[self.host].STOCKS:
            self.subscribe(stock)
            time.sleep(0.05)

    def open_database(self, database_name):
        """Test function - creates db and table or changes state dict"""
        self.create_state_dict()
        path = self.dir_manager.stock_database_dir / (database_name + ".db")
        database = Database(path)

        for key in values.STOCK_INTERVALS_VALUES:
            table = key + "_" + database_name
            if self.state_dict.get(table) is None or self.state_dict[table] is False:
                database.execute(table_factory.create_table(key, table_factory.TABLE_TYPES["stock"]))
                self.state_dict[table] = True
                database.list_tables()
                print(database.tables)
                print(self.state_dict)

    def stream(self) -> None:
        while True:
            while self.connection.stream_queue.empty():
                continue
            message = self.connection.stream_queue.get()
            msg_list = message.split('\n')
            for msg in msg_list:
                if len(msg) > 0:
                    (response, size) = json.JSONDecoder().raw_decode(msg)
                    self.stream_message_handler(response)
                    time.sleep(0.1)

    def stream_message_handler(self, message: json):
        if message["command"] == "candle":
            try:
                candle = STREAM[(message["command"])](message["data"], values.STOCK_INTERVALS_VALUES["PERIOD_M1"])
                print(candle)
                self.handle_candle(candle)
            except Exception as e:
                print(e)
        else:
            """So i wont get errors displayed"""
            print(self.state_dict)

    def handle_candle(self, candle: Candle):
        period_name = values.STOCK_INTERVALS_NAMES[(candle.close_time - candle.open_time) / 60000]
        database_name = candle.symbol
        db = Database(self.dir_manager.stock_database_dir / (database_name + ".db"))
        table_name = period_name + "_" + database_name

        if self.state_dict.get(table_name) is None or self.state_dict[table_name] is False:
            db.execute(table_factory.create_table(table_name, table_factory.TABLE_TYPES["stock"]))
            self.state_dict[table_name] = True

        request = f"SELECT close_time from {table_name} ORDER BY close_time DESC limit 1"
        last_candle_close_time = (db.get_data_series(request))
        if not last_candle_close_time:
            last_candle_close_time = candle.open_time
        else:
            last_candle_close_time = last_candle_close_time[0][0]
        difference  = (candle.open_time - int(last_candle_close_time))/60000
        if difference <= 0:
            self.push_candle_to_db(candle, db, table_name)
            del db
            return
        print(f"Database is missing {difference} candles") #TODO HANDLE DAY DIFFRENCE
        self.connection.send_client(self.commands.get_chart_data(chart=candle.symbol,
                                                                  start_date=last_candle_close_time,
                                                                  end_date=candle.open_time,
                                                                  period=values.STOCK_INTERVALS_VALUES[period_name]))
        while self.connection.client_queue.empty():
            continue

        message = self.connection.client_queue.get()
        candles = message["returnData"]['rateInfos']
        if not candles:
            print("[!!!]EOD exception?")
            self.push_candle_to_db(candle, db, table_name)
            del db
            return
        for i, fill_candle in enumerate(candles):
            fill_candle['open'] = fill_candle['open']/10
            fill_candle['close'] = fill_candle['open'] + fill_candle['close']
            fill_candle['high'] = fill_candle['open'] + fill_candle['high']
            fill_candle['low'] = fill_candle['open'] + fill_candle['low']
            filling_up_candle = STREAM["candle"](fill_candle, values.STOCK_INTERVALS_VALUES["PERIOD_M1"], candle.symbol)
            print("------------")
            print(filling_up_candle)
            self.push_candle_to_db(filling_up_candle, db, table_name)
            print(f"Filled {i + 1}/{int(difference)} candles")
            print("------------")
            time.sleep(0.5/difference)

        self.push_candle_to_db(candle, db, table_name)
        del db

    def push_candle_to_db(self, candle: Candle, db: Database, table: str):
        command = f"INSERT or IGNORE INTO {table} VALUES ({candle.open_time}, {candle.close_time}, " \
                  f"{candle.open_price}, {candle.close_price}, {candle.max_price}, " \
                  f"{candle.min_price}, {candle.volume})"
        db.execute(command)

    async def check_files(self):
        await check_all(self.dir_manager)

    async def create_state_dict(self):
        """Creates state_dict in RAM"""
        await self.check_files()
        self.state_dict = create_state_dict(self.dir_manager.stock_database_dir)
        print(self.state_dict)

    def __del__(self):
        self.connection.send_client(self.commands.logout())
        del self.connection


