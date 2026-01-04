from framework.mysql_db import MySQLDatabase

async def get_rank_data_range(account):
    data = await MySQLDatabase.instance.get_rank_month_history(account)
    last_date = data[-1][0]
    prev_month_rank = {}
    result = []
    for row in data:
        date, rank = row
        if date.month == last_date.month:
            result.append((*row, prev_month_rank.get(date.day)))
        else:
            prev_month_rank[date.day] = rank
    return result
