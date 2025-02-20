"""функции работы с БД"""
import os
from datetime import datetime, timezone
import logging
from typing import Iterable
from sqlalchemy import Engine, create_engine, insert, update
from sqlalchemy.orm import Session
from db_models import Base, DbLog


__engine: Engine = None


def get_engine() -> Engine:
    """пуолучение подключения к БД"""
    global __engine
    if __engine is None:
        db_connection_string = (f"mysql+mysqlconnector://"
                                f"{os.environ.get('DB_USER_NAME', '')}:{os.environ.get('DB_USER_PWD', '')}"
                                f"@{os.environ.get('DB_HOST', '127.0.0.1')}:{os.environ.get('DB_PORT', 3306)}"
                                f"/{os.environ.get('DB_SCHEMA', 't25')}"
                                )
        print(db_connection_string)
        __engine = create_engine(db_connection_string, echo=False)
        logging.info('get_engine: OK')
    return __engine


def table_insert_or_update_by_id_inner(db: Session, table: Base, dct: dict) -> None:
    """добавить или обновить одну запись по ID"""
    logging.info(dct)
    id_value = dct['id']
    # TODO перевести на upsert
    r = db.query(table).filter(table.id == id_value).first()
    if r is None:
        db.execute(insert(table).values(dct))
    else:
        db.execute(update(table).where(table.id == id_value).values(dct))


def table_insert_or_update_by_id(table: Base, dct: dict) -> None:
    """добавить или обновить одну запись по ID"""
    with Session(autoflush=False, bind=get_engine()) as db:
        table_insert_or_update_by_id_inner(db, table, dct)
        db.commit()


def table_insert_or_update_by_id_many_inner(db: Session,
                                            table: Base,
                                            dct_list: Iterable[dict]) -> None:
    """добавить или обновить список записей по ID"""
    for dct in dct_list:
        table_insert_or_update_by_id_inner(db, table, dct)


def table_insert_or_update_by_id_many(table: Base, dct_list: Iterable[dict]) -> None:
    """добавить или обновить список записей по ID"""
    with Session(autoflush=False, bind=get_engine()) as db:
        table_insert_or_update_by_id_many_inner(db, table, dct_list)
        db.commit()


def table_insert_inner(db: Session, table: Base, dct: dict) -> None:
    """вставка новой записи"""
    logging.info('%s: |%s|', table, dct)
    record = table(**dct)
    db.add(record)


def table_insert(table: Base, dct: dict) -> None:
    """вставка новой записи"""
    with Session(autoflush=False, bind=get_engine()) as db:
        table_insert_inner(db, table, dct)
        db.commit()


def db_log(txt: str) -> None:
    """сохранение теста в таблицу лога"""
    table_insert(DbLog, {
        'log_string': txt, 'created_at': datetime.now(timezone.utc)})
