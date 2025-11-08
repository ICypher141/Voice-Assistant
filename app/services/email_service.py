import smtplib
from email.mime.text import MIMEText
from app.core.config import get_settings

class EmailService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def send_email(self, to: str, subject: str, body: str) -> None:
        if not to or not subject or not body:
            raise ValueError("to, subject, and body are required")
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.settings.smtp_user
        msg["To"] = to

        if self.settings.smtp_use_tls:
            server = smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(self.settings.smtp_host, self.settings.smtp_port)

        try:
            server.login(self.settings.smtp_user, self.settings.smtp_password)
            server.sendmail(self.settings.smtp_user, [to], msg.as_string())
        finally:
            server.quit()