import asyncio

from db.config import TABLE_NAME
import mysql.connector

class MySQLDatabase:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = mysql.connector.connect(**db_config)

    async def get_last_rank(self, accountid):
        self.conn.reconnect()
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT rank
                FROM {TABLE_NAME}
                WHERE accountid = %s
                ORDER BY snapshot_date DESC
                LIMIT 1
            """, (accountid,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                return None
            
    async def get_rank_history(self, accountid):
        self.conn.reconnect()
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT snapshot_date, rank
                FROM {TABLE_NAME}
                WHERE accountid = %s
                ORDER BY snapshot_date DESC
            """, (accountid,))
            return cur.fetchall()

    def close(self):
        self.conn.close()
