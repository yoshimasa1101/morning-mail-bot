import os
import schedule
import time
from morning_mail import send_morning_mail

# === 起動確認ログ ===
print("=== main.py started ===")
print("Supabase URL:", os.getenv("SUPABASE_URL"))
print("Environment loaded successfully")

def job():
    print("🟡 Job started: calling send_morning_mail()")
    try:
        send_morning_mail()
        print("✅ Job finished successfully.")
    except Exception as e:
        print("❌ Error in job():", e)

# === スケジューラー設定 ===
# Render は UTC タイムゾーンなので、JST 8:00 は UTC 23:00
schedule.every().day.at("23:00").do(job)

print("🕒 Morning Mail Bot Scheduler started. Waiting for next run...")

# === 即時実行テスト用 ===
# コメントアウトを外すと手動実行可能
# job()

# === スケジューラーを維持 ===
while True:
    schedule.run_pending()
    time.sleep(60)
