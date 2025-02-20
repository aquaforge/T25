"""стартовый модуль"""
import logging
import asyncio
import os

# https://apscheduler.readthedocs.io/
# pip install apscheduler
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db_functions import db_log
from utils import init_logging

init_logging(os.environ.get('LOG_LEVEL', 'WARNING'),
             os.environ.get('LOG_DIR', 'tmp'))

tick_interval = int(os.environ.get('TICK_INTERVAL_SEC_MAX', 1200))


async def main() -> None:
    """main"""
    logging.info('STARTED')

    try:
        while True:
            await asyncio.sleep(tick_interval)
            db_log('-l-')
    except asyncio.CancelledError:
        pass
    except BaseException:
        logging.exception("sleep", exc_info=True)

    db_log('FINISHED')
    logging.info('FINISHED')

if __name__ == '__main__':
    asyncio.run(main())
