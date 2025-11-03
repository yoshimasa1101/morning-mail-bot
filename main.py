import schedule
import time
from morning_mail import send_morning_mail

def job():
    send_morning_mail()

# 毎朝 8:00 に実行（日本時間）
schedule.every().day.at("08:00").do(job)

print("朝の挨拶メールボットが起動しました。")

while True:
    schedule.run_pending()
    time.sleep(60)
