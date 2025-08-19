#!/usr/bin/env python3
"""Nightly ETL from operational DB to warehouse schema.

etl_nightly.py v0.1.0 (2025-08-19)
"""
import logging
import os
from sqlalchemy import create_engine, text

LOG_DIR = os.path.join('logs', 'data-warehouse')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, 'etl.log')
logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


def run():
    """Run ETL transferring orders and positions into warehouse schema."""
    src_dsn = os.getenv('OP_DB_DSN', 'postgresql://postgres@localhost:5432/cashmachiine')
    engine = create_engine(src_dsn)
    logging.info('Starting ETL run')
    with engine.begin() as conn:
        conn.execute(text(
            "INSERT INTO warehouse.dw_orders "
            "(id, user_id, symbol, qty, price, created_at) "
            "SELECT id, user_id, symbol, qty, price, created_at FROM public.orders"
        ))
        conn.execute(text(
            "INSERT INTO warehouse.dw_positions "
            "(id, account_id, symbol, qty, updated_at) "
            "SELECT id, account_id, symbol, qty, updated_at FROM public.positions"
        ))
    logging.info('ETL run complete')


if __name__ == '__main__':
    run()
