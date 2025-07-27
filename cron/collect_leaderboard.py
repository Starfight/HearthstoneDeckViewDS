import requests
import mysql.connector
from datetime import date
import time
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection settings
DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

# API config
API_URL_TEMPLATE = "https://hearthstone.blizzard.com/en-us/api/community/leaderboardsData?region=EU&leaderboardId=standard&page={page}"

# PostgreSQL table
TABLE_NAME = "leaderboard_month_history"

def create_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                snapshot_date DATE NOT NULL,
                accountid VARCHAR(24) CHARACTER SET utf16 COLLATE utf16_unicode_ci NOT NULL,
                rank INTEGER NOT NULL,
                PRIMARY KEY (snapshot_date, accountid)
            );
        """)
        conn.commit()

def fetch_leaderboard_page(page):
    url = API_URL_TEMPLATE.format(page=page)
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        raise Exception(f"Erreur API page {page} : {resp.status_code}")

def insert_data(conn, data):
    with conn.cursor() as cur:
        cur.executemany(f"""
            INSERT INTO {TABLE_NAME} (snapshot_date, accountid, rank)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE rank = VALUES(rank);
        """, data)
        conn.commit()

def main():
    today = date.today()

    # MySQL connexion
    conn = mysql.connector.connect(**DB_CONFIG)
    create_table_if_not_exists(conn)

    # Drop data first day of the month
    if today.day == 1:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {TABLE_NAME};")
            conn.commit()
            print("Month data deleted!")

    # First page to get the total number of pages
    first_page = fetch_leaderboard_page(1)
    total_pages = first_page['leaderboard']['pagination']['totalPages']

    print(f"Total pages to fetch: {total_pages}")
    all_rows = []

    for page in range(1, total_pages + 1):
        try:
            data = fetch_leaderboard_page(page)
            rows = data['leaderboard']['rows']
            for row in rows:
                rank = row['rank']
                accountid = row['accountid']
                all_rows.append((today, accountid, rank))
                if len(all_rows) >= 100:
                    insert_data(conn, all_rows)
                    all_rows = []
            print(f"Fetched page {page}/{total_pages} ({len(rows)} rows)")
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            continue

        time.sleep(0.2)  # To not overload the API

    # Insert last batch
    if all_rows:
        insert_data(conn, all_rows)

    print("Insertion done!")
    conn.close()

if __name__ == "__main__":
    main()
