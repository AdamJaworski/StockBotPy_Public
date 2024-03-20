"""
Utility used to setup debug logger for a program. Logger will register every console output and save into file
"""
import logging
import sys
import warnings
import websocket
from datetime import datetime
from pathlib import Path


class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf) -> None:
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


def setup_logger(logger_path: Path) -> None:
    file_name = "logs_" + str(datetime.today().date()) + "_" + str(datetime.today().time().strftime('%H_%M')) + ".log"
    logging.basicConfig(filename=(logger_path / file_name), level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    websocket.enableTrace(True)
    logging.captureWarnings(True)
    warnings.filterwarnings = warning_filter
    warnings.showwarning = _warning
    sys.stdout = StreamToLogger(logging.getLogger('stdout'), logging.INFO)
    sys.stderr = StreamToLogger(logging.getLogger('stderr'), logging.ERROR)


def _warning(message, category, filename, lineno, file=None, line=None):
    print(message)


def warning_filter(message):
    return "WARNING! " in str(message)
