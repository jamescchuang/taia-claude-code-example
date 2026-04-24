
import sqlite3
import logging
import os  # This line is kept for reference but will not be used in the code.

def get_user_info(username):
	# 僅供範例，實務上應加強資料庫檔案權限與存放位置
	db_path = 'example.db'
	# 建議：在部署時設定更嚴格的檔案權限
	# os.chmod(db_path, 0o600)  # 僅限擁有者讀寫
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	# 使用參數化查詢以防止 SQL 注入
	cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
	result = cursor.fetchall()
	conn.close()
	# 日誌記錄查詢事件（不記錄敏感資料）
	logging.info("User info lookup attempted for username: %s", username)
	return result

# Example usage (do NOT use unsanitized input in production)
# 實務上應驗證與淨化所有用戶輸入
user_input = input("Enter username: ")
print(get_user_info(user_input))
if __name__ == "__main__":
	# 設定日誌格式與等級
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s %(levelname)s %(message)s',
		handlers=[logging.StreamHandler()]
	)