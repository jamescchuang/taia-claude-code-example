# ⚠️  教學示範用途 — 本檔故意包含 SQL Injection 漏洞，請勿用於生產環境。
# Demo only: this file contains an intentional SQL injection flaw for training.

import sqlite3

DB_PATH = "example.db"


def get_user_info(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ❌ 漏洞點：直接以字串串接組出 SQL，未使用參數化查詢。
    #    攻擊者可輸入   ' OR '1'='1   來繞過 WHERE 條件，dump 整張資料表。
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    result = cursor.fetchall()
    conn.close()
    return result


if __name__ == "__main__":
    user_input = input("Enter username: ")
    print(get_user_info(user_input))
