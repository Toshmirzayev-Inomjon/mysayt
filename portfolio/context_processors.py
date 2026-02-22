from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode

from .models import UserPreference
from .ui_i18n import normalize_language


def global_settings(request):
    theme = 'dark'
    session_language = ''
    if hasattr(request, 'session'):
        session_language = request.session.get(settings.LANGUAGE_COOKIE_NAME, '')

    # Browser/session choice should be reflected immediately in the header select.
    language = normalize_language(session_language or getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE))
    if request.user.is_authenticated:
        pref = UserPreference.objects.filter(user=request.user).first()
        if pref:
            theme = pref.theme
            if not session_language and pref.language:
                language = normalize_language(pref.language)

    current_path = request.get_full_path() if request else '/'
    language_switch_urls = {}
    alternate_language_urls = []
    set_lang_url = reverse('portfolio:set_language')
    for code, _label in settings.LANGUAGES:
        query = urlencode({'language': code, 'next': current_path})
        switch_url = f'{set_lang_url}?{query}'
        language_switch_urls[code] = switch_url
        alternate_language_urls.append(
            {
                'code': code,
                'url': request.build_absolute_uri(switch_url) if request else f'{settings.SITE_URL}{switch_url}',
            }
        )

    whatsapp_digits = ''.join(ch for ch in settings.WHATSAPP_NUMBER if ch.isdigit())
    whatsapp_url = f'https://wa.me/{whatsapp_digits}' if whatsapp_digits else ''
    telegram_username = settings.TELEGRAM_USERNAME.lstrip('@')
    telegram_url = f'https://t.me/{telegram_username}' if telegram_username else ''
    static_base = settings.STATIC_URL if settings.STATIC_URL.startswith('/') else f'/{settings.STATIC_URL}'

    return {
        'site_url': settings.SITE_URL,
        'default_og_image': f'{settings.SITE_URL}{static_base}brand/og-image.svg',
        'cv_download_url': settings.CV_DOWNLOAD_URL,
        'booking_external_url': settings.BOOKING_EXTERNAL_URL,
        'available_languages': settings.LANGUAGES,
        'language_switch_urls': language_switch_urls,
        'alternate_language_urls': alternate_language_urls,
        'current_language': language,
        'preferred_theme': theme,
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
        'whatsapp_url': whatsapp_url,
        'telegram_url': telegram_url,
    }
