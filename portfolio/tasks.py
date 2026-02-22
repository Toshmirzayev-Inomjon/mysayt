import importlib.util

from .notifications import (
    send_contact_notifications,
    send_newsletter_subscribe_notification,
    send_verification_email,
)

CELERY_AVAILABLE = importlib.util.find_spec('celery') is not None

if CELERY_AVAILABLE:
    from celery import shared_task

    @shared_task
    def send_contact_notifications_task(message_id):
        from .models import ContactMessage
        message_obj = ContactMessage.objects.filter(pk=message_id).first()
        if message_obj:
            send_contact_notifications(message_obj)

    @shared_task
    def send_verification_email_task(user_id, token, site_url=''):
        from django.contrib.auth.models import User
        user = User.objects.filter(pk=user_id).first()
        if user:
            send_verification_email(user, token, site_url=site_url)

    @shared_task
    def send_newsletter_notification_task(email):
        send_newsletter_subscribe_notification(email)

else:
    def send_contact_notifications_task(message_id):
        from .models import ContactMessage
        message_obj = ContactMessage.objects.filter(pk=message_id).first()
        if message_obj:
            send_contact_notifications(message_obj)

    def send_verification_email_task(user_id, token, site_url=''):
        from django.contrib.auth.models import User
        user = User.objects.filter(pk=user_id).first()
        if user:
            send_verification_email(user, token, site_url=site_url)

    def send_newsletter_notification_task(email):
        send_newsletter_subscribe_notification(email)
