from email.mime.text import MIMEText
import smtplib
from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..core.config import settings

_env = Environment(
    loader=FileSystemLoader('app/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def send_confirmation_email(to_email: str, token: str) -> None:
    template = _env.get_template('confirm_email.html')
    confirm_url = f"{settings.FRONTEND_URL}/confirm-email?token={token}"
    html = template.render(confirm_url=confirm_url)
    msg = MIMEText(html, 'html')
    msg['Subject'] = 'Email confirmation'
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = to_email
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        if settings.SMTP_USER:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.EMAIL_FROM, [to_email], msg.as_string())
