import smtplib
from email.utils import formataddr
from email.message import EmailMessage
from django.conf import settings


class Util:
    @staticmethod
    def send_email(data):
        msg = EmailMessage()
        msg["Subject"] = data['email_subject']
        msg["From"] = formataddr(("Crypto Stock", settings.EMAIL_HOST_USER))
        msg["To"] = data['to_email']
        msg["BCC"] = settings.EMAIL_HOST_USER

        msg.set_content(data['content'])

        msg.add_alternative(data['alternative_content'], subtype="html", )

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, data['to_email'], msg.as_string())


