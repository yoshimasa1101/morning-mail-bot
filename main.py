import os
import time
import schedule
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from supabase import create_client, Client

# --- メール送信処理 ---
def send_morning_mail():
    print("=== send_morning_mail started ===")

    try:
        # --- 環境変数の取得 ---
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        GMAIL_USER = os.getenv("GMAIL_USER")
        GMAIL_PASS = os.getenv("GMAIL_PASS")
        TO_EMAIL = os.getenv("TO_EMAIL")

        print("Connecting to Supabase...")
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

        print("Fetching data from table 'tasks'...")
        response = supabase.table("tasks").select("*").execute()
        data = response.data

        if not data:
            print("⚠️ No data found in 'tasks'")
            data_text = "No tasks found."
        else:
            data_text = "\n".join([f"- {row['title']}" for row in data])
            print(f"✅ Retrieved {len(data)} records from Supabase")

        subject = "🌅 Morning Mail Bot Report"
        body = f"""
        Good morning!

        Here is your latest task summary:

        {data_text}

        -- 
        Morning Mail Bot
        """

        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = TO_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        print("Connecting to Gmail SMTP...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print("✅ Mail sent successfully to:", TO_EMAIL)

    except Exception as e:
        print("❌ Error in send_morning_mail:", e)

    print("=== send_morning_mail finished ===")


# --- スケジューラー処理 ---
def job():
    send_morning_mail()

# 日本時間8:00に実行（RenderではUTC基準なので注意）
# RenderのタイムゾーンはUTC→日本時間-9時間
# → 日本8:00 = UTC23:00
schedule.every().day.at("23:00").do(job)

print("🌅 Morning Mail Bot Scheduler started. Waiting for next run...")

# --- 無限ループでスケジューラーを維持 ---
while True:
    schedule.run_pending()
    time.sleep(60)
