import logging
import json

import asyncio
from influxdb import InfluxDBClient

from client import QTClient

logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s:%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s",
                        handlers=[logging.FileHandler("/mnt/finances.log"),
                                  logging.StreamHandler()])

if __name__ == '__main__':
    logging.info("Reading refresh token")
    f = open("/mnt/refresh_token.txt", "r")
    refresh_token = f.read()

    logging.info("Connecting to Questrdate")
    client = QTClient(refresh_token)
    logging.info("Connecting to InfluxDB")
    influx_client = InfluxDBClient(host='influxdb', database='market')
    logging.info("OK")
    async def scraper(ticks):
        ticks = json.loads(ticks)
        if 'quotes' in ticks:
            for tick in ticks['quotes']:
                try:
                    json_body = [
                        {
                            "measurement": "market",
                            "tags": {
                                "symbol": tick['symbol']
                            },
                            "fields": {
                                "bidPrice": tick['bidPrice'],
                                "bidSize": tick['bidSize'],
                                "askPrice": tick['askPrice'],
                                "askSize": tick['askSize'],
                                "lastTradePrice": tick['lastTradePrice'],
                                "lastTradeSize": tick['lastTradeSize'],
                                "volume": tick['volume'],
                                "VWAP": tick['VWAP']
                            }
                        }
                    ]
                    influx_client.write_points(json_body)
                except Exception:
                    logging.exception("message")

    asyncio.get_event_loop().run_until_complete(client.subscribe(['8049', '9292'], scraper))