"""
Utility used to check if there are any unknown files in db localizations that could interrupt program
"""
import os
import asyncio
import time
from pathlib import Path
from StockBot.managers.dir_manager import PathManager


async def check_all(path_manager: PathManager) -> None:
    task_database = asyncio.create_task(check_db_dir(path_manager.stock_database_dir))
    await task_database


async def check_db_dir(database_dir: Path) -> None:
    files_in_dir = os.listdir(database_dir)

    for file in files_in_dir:
        if not os.path.splitext(file)[-1].lower() == '.db':
            print("[!!!] File " + str(file) + " is unknown and may cause harm to the program!")
