import json
import os
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.mail import send_mail


def send_contact_notifications(message_obj):
    _send_email_notification(message_obj)
    _send_telegram_notification(message_obj)


def _send_email_notification(message_obj):
    recipient = os.getenv('CONTACT_NOTIFY_EMAIL', '').strip()
    if not recipient:
        return

    subject = f"[Portfolio] New contact from {message_obj.full_name}"
    body = (
        f"Name: {message_obj.full_name}\n"
        f"Email: {message_obj.email}\n\n"
        f"Message:\n{message_obj.message}\n"
    )
    send_mail(subject, body, os.getenv('DEFAULT_FROM_EMAIL', recipient), [recipient], fail_silently=True)


def _send_telegram_notification(message_obj):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    if not bot_token or not chat_id:
        return

    text = (
        "New portfolio contact\n"
        f"Name: {message_obj.full_name}\n"
        f"Email: {message_obj.email}\n"
        f"Message: {message_obj.message}"
    )

    payload = urllib.parse.urlencode({'chat_id': chat_id, 'text': text}).encode()
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{bot_token}/sendMessage',
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            json.loads(resp.read().decode('utf-8'))
    except Exception:
        # Notification failure should not break contact form flow.
        pass


def send_verification_email(user, token, site_url=''):
    if not user.email:
        return
    base_url = (site_url or settings.SITE_URL).rstrip('/')
    verify_url = f'{base_url}/accounts/verify-email/{token}/'
    subject = "Portfolio account: email verification"
    body = (
        f"Salom {user.username},\n\n"
        "Akkauntingizni faollashtirish uchun quyidagi havolaga o'ting:\n"
        f"{verify_url}\n\n"
        "Agar bu siz bo'lmasangiz, xabarni e'tiborsiz qoldiring."
    )
    send_mail(subject, body, os.getenv('DEFAULT_FROM_EMAIL', ''), [user.email], fail_silently=True)


def send_newsletter_subscribe_notification(email):
    recipient = os.getenv('CONTACT_NOTIFY_EMAIL', '').strip()
    if recipient:
        subject = "[Portfolio] New newsletter subscriber"
        body = f"New subscriber: {email}"
        send_mail(subject, body, os.getenv('DEFAULT_FROM_EMAIL', recipient), [recipient], fail_silently=True)

    # Placeholder for campaign providers integration.
    provider = os.getenv('NEWSLETTER_CAMPAIGN_PROVIDER', 'none').strip().lower()
    api_key = os.getenv('NEWSLETTER_CAMPAIGN_API_KEY', '').strip()
    if provider == 'mailchimp' and api_key:
        pass
