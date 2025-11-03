import os
from morning_mail import send_morning_mail

# === 起動ログ ===
print("=== main.py started ===")
print("Supabase URL:", os.getenv("SUPABASE_URL"))
print("Environment loaded successfully")

# === メイン処理 ===
try:
    print("🚀 Job started: calling send_morning_mail()")
    send_morning_mail()
    print("✅ Job finished successfully.")
except Exception as e:
    print("❌ Error in job():", e)

print("=== main.py finished ===")
