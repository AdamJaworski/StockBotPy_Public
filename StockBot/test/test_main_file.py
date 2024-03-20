import time

from StockBot.values import values
from test_user_class import User
from threading import Thread


def main():
    user = User(True, values.TEST_PATH, 'xtb')
    time.sleep(1)
    user.subscribe_all()
    stream = Thread(target=user.stream())
    stream.start()


if __name__ == '__main__':
    main()