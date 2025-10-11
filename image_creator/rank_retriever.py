from framework.mysql_db import MySQLDatabase
from db.config import DB_CONFIG

async def get_rank_data_range(account):
    mysql_db = MySQLDatabase(DB_CONFIG)
    return await mysql_db.get_rank_month_history(account)