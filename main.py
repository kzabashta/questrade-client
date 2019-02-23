import logging

import asyncio

from client import QTClient

logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s:%(levelname)s:%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s",
                        handlers=[logging.FileHandler("/mnt/finances.log"),
                                  logging.StreamHandler()])

if __name__ == '__main__':
    f = open("/mnt/refresh_token.txt", "r")
    refresh_token = f.read()

    client = QTClient(refresh_token)

    account_id = client.get_account()['accounts'][0]['number']
    logging.info('Account Number: %s' % account_id)

    candles = client.get_candles('8049', '2017-10-01T00:00:00-05:00', '2018-10-01T00:00:00-05:00', 'OneDay')
    logging.info(candles)

    async def printer(message):
        logging.info('From main' + message)

    asyncio.get_event_loop().run_until_complete(client.subscribe(['8049'], printer))