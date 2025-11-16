import asyncio
from datetime import date

from db.config import TABLE_NAME
import mysql.connector

class MySQLDatabase:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MySQLDatabase, cls).__new__(cls)
        return cls.instance

    def __init__(self, db_config):
        if not hasattr(self, 'db_config_initialized'):
            self.conn = mysql.connector.connect(**db_config)
            self.db_config_initialized = True

    async def is_account_exist(self, accountid):
        # default date
        month = date.today().month
        year = date.today().year
        self.conn.reconnect()
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT count(*)
                FROM {TABLE_NAME}
                WHERE accountid = %s
                    AND MONTH(snapshot_date) = %s
                    AND YEAR(snapshot_date) = %s
            """, (accountid, month, year))
            result = cur.fetchone()
            if result[0] > 0:
                return True
            else:
                return False

    async def get_rank_month_history(self, accountid):
        # default date
        month = date.today().month
        year = date.today().year
        # Get the previous month and year
        previous_month = month - 1 if month > 1 else 12
        previous_year = year
        if previous_month == 12:
            previous_year -= 1
        self.conn.reconnect()
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT snapshot_date, rank
                FROM {TABLE_NAME}
                WHERE accountid = %s AND (
                    (MONTH(snapshot_date) = %s AND YEAR(snapshot_date) = %s)
                    OR
                    (MONTH(snapshot_date) = %s AND YEAR(snapshot_date) = %s)
                )
                ORDER BY snapshot_date ASC
            """, (accountid, month, year, previous_month, previous_year))
            return cur.fetchall()

    def close(self):
        self.conn.close()
