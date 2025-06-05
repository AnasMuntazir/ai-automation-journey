import os
import imaplib
import email
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_latest_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()

    summaries = []

    for e_id in email_ids[-5:]:
        _, msg_data = mail.fetch(e_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg["subject"]
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            summary = ask_groq(subject, body)
                            summaries.append((subject, summary))
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                    summary = ask_groq(subject, body)
                    summaries.append((subject, summary))

    return summaries

def ask_groq(subject, body):
    prompt = f"""You are an email assistant. Read the email below and summarize it in 3 bullet points.\n\nSubject: {subject}\n\nEmail:\n{body}"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    print("📧 Fetching your latest emails...\n")
    summaries = get_latest_emails()
    for subject, summary in summaries:
        print(f"\n📌 Subject: {subject}")
        print("🔎 Summary:")
        print(summary)
        print("-" * 40)

if __name__ == "__main__":
    main()
