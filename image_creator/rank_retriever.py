from framework.mysql_db import MySQLDatabase

async def get_rank_data_range(account):
    return await MySQLDatabase.instance.get_rank_month_history(account)