"""
Utility used to save in dict info about tables in stocks db. example:
    "PERIOD_M15_WIG_20": true
    "PERIOD_M10_WIG_20": false

    later usage:
    if not state_dict["PERIOD_M10_WIG_20"]:
        db.manager.execute(create_table('PERIOD_M10', tables_factory.TABLE_TYPES["stock"]))
"""

import os
from ..values import values
from pathlib import Path
from StockBot.managers.db_manager import Database


def create_state_dict(database_path: Path) -> dict:
    state_dict = dict()
    db_list = os.listdir(database_path)

    for database_file in db_list:
        database = Database(database_path / str(database_file))
        database.list_tables()
        for period in values.STOCK_INTERVALS_VALUES:
            name = f"{period}_{(os.path.splitext(database_file)[0])}"
            if name in database.tables: 
                state_dict[name] = True
            else:
                state_dict[name] = False

        del database
    return state_dict

