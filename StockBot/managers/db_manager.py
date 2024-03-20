import sqlite3
import os
from warnings import warn


class Database:
    db_cursor: sqlite3.Cursor
    db: sqlite3.Connection
    tables = []
    database_name: str

    def __init__(self, database_location: os.PathLike):
        self.rise_warn(database_location)
        self.db = sqlite3.connect(database_location)
        """db is a connection to database"""
        self.db_cursor = self.db.cursor()
        """db_cursor is simply a cursor used to navigate threw .db"""
        self.database_name = os.path.splitext(database_location)[0]
        self.list_tables()
        return

    @staticmethod
    def rise_warn(database_location: os.PathLike) -> None:
        if not os.path.splitext(database_location)[-1].lower() == '.db':
            warn(f"[!!!] {database_location} is not .db file, loading make sure to check it!", category=UserWarning)

    def get_data_series(self, request: str) -> list:
        """Use to get a lot of data, returns list of tuple"""
        self.db_cursor.execute(request)
        return self.db_cursor.fetchall()

    def list_tables(self) -> None:
        """List tables in database"""
        self.tables = []
        self.db_cursor.execute("SELECT name FROM sqltie_master WHERE type='table'")
        tables_cursor = self.db_cursor.fetchall()
        """expected output: [(table_name_1, ), (table_name_2,), ...]"""
        for table in tables_cursor:
            self.tables.append(table[0])

    def get_distinct_data(self, data, table):
        return print(self.get_data_series(f"SELECT DISTINCT {data} FROM {table}"))

    def execute(self, command: str) -> None:
        self.db_cursor.execute(command)
        self.db.commit()

    def disconnect(self) -> None:
        """Closes database - MAKE SURE TO ALWAYS USE IT AT AFTER USING DB"""
        self.db_cursor.close()
        self.db.close()
        print(f"Database {self.database_name} closed.")

    def __del__(self) -> None:
        self.disconnect()


