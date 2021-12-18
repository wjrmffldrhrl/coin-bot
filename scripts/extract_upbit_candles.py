import os
import time
from datetime import datetime, timedelta

from coin_data_manager.api.api_caller import UpbitApiCaller
from coin_data_manager.repositories.candle import CandleRepository, AlreadyExistError
from coin_data_manager.util import CandleUnit, TooManyRequestsError
from config.config import CONFIG


if __name__ == '__main__':
    market = os.environ["MARKET"]
    print("market", market)
    api_caller = UpbitApiCaller()

    database_config = CONFIG["database"]

    database = database_config["database"]
    host = database_config["host"]
    port = database_config["port"]
    user = database_config["user"]
    password = database_config["password"]

    candle_repository = CandleRepository(database, host, port, user, password)
    last_candle_time = datetime.now()

    candles = [" "]
    while len(candles) > 0:

        try:
            candles = api_caller.get_candles(market, 200, CandleUnit.MIN_1, last_candle_time.strftime("%Y-%m-%d %H:%M:00"))

            for candle in candles:
                print(candle.datetime)
                try:
                    candle_repository.add(candle)
                except AlreadyExistError as e:
                    print("Already")

            last_candle_time = last_candle_time - timedelta(minutes=200)

        except TooManyRequestsError as e:
            print(e)

        time.sleep(0.05)

    print("Extract done")
