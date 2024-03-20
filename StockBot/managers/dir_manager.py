from pathlib import Path


class PathManager:
    catalog_dir:        Path
    stock_database_dir: Path
    logger_dir:         Path

    def __init__(self, path: Path):
        self.catalog_dir          = path.absolute().resolve()
        self.stock_database_dir   = self.catalog_dir / "stocks"
        self.logger_dir           = self.catalog_dir
        self.create_dirs()
        return

    def create_dirs(self):
        self.catalog_dir.mkdir(exist_ok=True, parents=True)
        self.stock_database_dir.mkdir(exist_ok=True, parents=True)
        return

