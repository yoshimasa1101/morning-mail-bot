import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import os

# ニュース取得
def get_news():
    url = "https://news.yahoo.co.jp/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    headlines = soup.select("a.sc-bZkfAO")
    news = [h.get_text() for h in headlines[:5]]
    return "\n".join(news)

# メール送信
def send_morning_mail():
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pass = os.getenv("GMAIL_PASS")
    to_email = os.getenv("TO_EMAIL")

    subject = "今日の朝のニュース！"
    body = get_news()

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Date"] = formatdate()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail_user, gmail_pass)
            server.send_message(msg)
        print("✅ メール送信に成功しました。")
    except Exception as e:
        print("❌ メール送信に失敗しました：", e)
