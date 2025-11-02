import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import os

def send_morning_mail():
    """朝のメールを送信する関数"""

    from_email = os.environ.get("FROM_EMAIL")
    from_password = os.environ.get("FROM_PASSWORD")
    to_email = os.environ.get("TO_EMAIL")

    subject = "おはようございます 🌅"
    body = "今日も1日頑張りましょう！\n\nこのメールは自動送信されています。"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Date"] = formatdate(localtime=True)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, from_password)
            server.send_message(msg)
        print("✅ メール送信完了！")
    except Exception as e:
        print("❌ メール送信に失敗しました:", e)

