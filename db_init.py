"""инициация БД, для отдельного запуска"""
import os
import logging
from db_models import Base
from utils import init_logging
from db_functions import db_log, get_engine

init_logging('INFO', os.environ.get('LOG_DIR', 'tmp'))

logging.info('db_init: STARTED')

Base.metadata.create_all(bind=get_engine())

db_log('db_init OK')
logging.info('db_init: DONE')
print('DONE')
