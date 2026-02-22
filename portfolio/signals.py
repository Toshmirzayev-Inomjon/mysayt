from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=User)
def apply_user_defaults_on_create(sender, instance, **kwargs):
    """
    Apply environment-driven defaults for brand-new users across all creation
    paths (signup, admin add form, shell, etc.).
    """
    if not instance._state.adding:
        return

    if settings.SIGNUP_AUTO_SUPERUSER:
        instance.is_active = True
        instance.is_staff = True
        instance.is_superuser = True
        return

    if settings.SIGNUP_AUTO_STAFF:
        instance.is_active = True
        instance.is_staff = True
        return

    if settings.SIGNUP_AUTO_ACTIVATE:
        instance.is_active = True
