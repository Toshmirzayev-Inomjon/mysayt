import random
import importlib.util
import smtplib
import socket
import json
import urllib.parse
import urllib.request
from datetime import datetime, time, timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import activate

from .forms import (
    BookingRequestForm,
    ContactMessageForm,
    NewsletterSubscribeForm,
    OTPTokenForm,
    SafePasswordResetForm,
    SignUpForm,
)
from .models import (
    BlogPost,
    EmailVerificationToken,
    FunnelEvent,
    HeroExperimentEvent,
    NewsletterSubscriber,
    Project,
    ProjectCategory,
    ServicePackage,
    ProjectTag,
    ProjectViewEvent,
    SearchQueryEvent,
    Testimonial,
    UserPreference,
)
from .tasks import send_contact_notifications_task, send_newsletter_notification_task, send_verification_email_task
from .ui_i18n import normalize_language, t as ui_t

HAS_OTP = importlib.util.find_spec('django_otp') is not None
if HAS_OTP:
    from django_otp.plugins.otp_totp.models import TOTPDevice


HERO_VARIANTS = {
    'A': {
        'title': {
            'uz': "Loyiha g'oyasidan productiongacha",
            'en': "From idea to production",
            'ru': 'От идеи до production',
        },
        'lead': {
            'uz': "Men Django asosida API va web ilovalar ishlab chiqaman. Bu sahifada har bir loyiha qanday ishlashi, qaysi texnologiyalar ishlatilgani va natijasi ko'rsatilgan.",
            'en': 'I build API and web apps with Django. On this page, each project shows implementation details, stack, and outcome.',
            'ru': 'Я разрабатываю API и веб-приложения на Django. На этой странице показаны детали реализации, стек и результаты проектов.',
        },
    },
    'B': {
        'title': {
            'uz': 'Kodingizni biznes natijaga aylantiraman',
            'en': 'I turn code into business outcomes',
            'ru': 'Превращаю код в бизнес-результат',
        },
        'lead': {
            'uz': "Mening fokusim: tezkor backend, toza arxitektura va ishonchli deploy. Quyida case-study formatida real loyihalarimni ko'rishingiz mumkin.",
            'en': 'My focus is fast backends, clean architecture, and reliable deploys. Below are real case studies.',
            'ru': 'Мой фокус: быстрый backend, чистая архитектура и надежный деплой. Ниже реальные кейсы.',
        },
    },
}


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def _parse_hour_minute(value):
    try:
        parts = value.split(':', 1)
        hour = int(parts[0])
        minute = int(parts[1])
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return hour, minute
    except Exception:
        pass
    return None


def _build_booking_slots():
    tz = timezone.get_current_timezone()
    today = timezone.localdate()
    slots = []

    for day_offset in range(max(1, settings.BOOKING_SLOT_DAYS)):
        slot_date = today + timedelta(days=day_offset)
        if slot_date.weekday() >= 5:
            continue
        for value in settings.BOOKING_SLOT_HOURS:
            parsed = _parse_hour_minute(value)
            if not parsed:
                continue
            hour, minute = parsed
            slot_dt = timezone.make_aware(datetime.combine(slot_date, time(hour=hour, minute=minute)), tz)
            slots.append(
                {
                    'value': slot_dt.strftime('%Y-%m-%dT%H:%M'),
                    'label': slot_dt.strftime('%a, %d %b %H:%M'),
                    'iso': slot_dt.isoformat(),
                }
            )
    return slots[:36]


def _verify_recaptcha(request):
    if not settings.RECAPTCHA_SITE_KEY or not settings.RECAPTCHA_SECRET_KEY:
        return True

    token = request.POST.get('g-recaptcha-response', '').strip()
    if not token:
        return False

    payload = urllib.parse.urlencode(
        {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': token,
            'remoteip': _client_ip(request),
        }
    ).encode('utf-8')
    req = urllib.request.Request(settings.RECAPTCHA_VERIFY_URL, data=payload, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
    except Exception:
        return False

    if not data.get('success'):
        return False

    score = data.get('score')
    if score is not None:
        try:
            return float(score) >= settings.RECAPTCHA_MIN_SCORE
        except Exception:
            return False
    return True


def _healthcheck_alert(error_details):
    if not settings.HEALTHCHECK_ALERT_EMAIL:
        return
    cache_key = 'healthcheck-alert-sent'
    if cache.get(cache_key):
        return

    body = (
        f"Healthcheck failed for {settings.SITE_URL}\n"
        f"Time: {timezone.now().isoformat()}\n\n"
        f"Details:\n{error_details}"
    )
    send_mail(
        subject='[Portfolio] Healthcheck alert',
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.HEALTHCHECK_ALERT_EMAIL],
        fail_silently=True,
    )
    cache.set(cache_key, 1, timeout=settings.HEALTHCHECK_ALERT_COOLDOWN_SECONDS)


def _is_rate_limited(cache_key, limit, window_seconds):
    current = cache.get(cache_key, 0)
    if current >= limit:
        return True, max(1, window_seconds // 60)
    return False, 0


def _increase_rate_limit(cache_key, window_seconds):
    current = cache.get(cache_key, 0) + 1
    cache.set(cache_key, current, timeout=window_seconds)
    return current


def _get_or_set_ab_variant(request):
    variant = request.COOKIES.get('hero_variant')
    if variant not in HERO_VARIANTS:
        variant = random.choice(['A', 'B'])
    return variant


def _track_variant_event(request, variant):
    marker = request.COOKIES.get('hero_variant_logged')
    today = timezone.localdate().isoformat()
    if marker == today:
        return False

    HeroExperimentEvent.objects.create(variant=variant, page='home')
    return True


def _track_funnel_event(request, stage, variant=''):
    FunnelEvent.objects.create(stage=stage, variant=variant, ip_address=_client_ip(request) or None)


def _hero_text(variant, language):
    data = HERO_VARIANTS.get(variant, HERO_VARIANTS['A'])
    lang = language if language in {'uz', 'en', 'ru'} else 'uz'
    title = data['title'].get(lang, data['title']['uz'])
    lead = data['lead'].get(lang, data['lead']['uz'])
    return title, lead


class SafePasswordResetView(PasswordResetView):
    form_class = SafePasswordResetForm

    def post(self, request, *args, **kwargs):
        ip_addr = _client_ip(request) or 'unknown'
        cache_key = f'password-reset-limit:{ip_addr}'
        limited, wait_minutes = _is_rate_limited(
            cache_key,
            settings.PASSWORD_RESET_RATE_LIMIT_ATTEMPTS,
            settings.PASSWORD_RESET_RATE_LIMIT_WINDOW_SECONDS,
        )
        if limited:
            messages.error(
                request,
                ui_t('msg.password_reset_rate_limited', request=request, wait_minutes=wait_minutes),
            )
            return redirect('portfolio:password_reset')

        _increase_rate_limit(cache_key, settings.PASSWORD_RESET_RATE_LIMIT_WINDOW_SECONDS)
        if not _verify_recaptcha(request):
            messages.error(request, ui_t('msg.recaptcha_failed', request=request))
            return redirect('portfolio:password_reset')
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except (smtplib.SMTPException, OSError, socket.gaierror):
            # Development fallback: show reset URL directly when SMTP is unreachable.
            if settings.DEBUG:
                email = form.cleaned_data.get('email', '')
                user = next(form.get_users(email), None)
                if user:
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    link = self.request.build_absolute_uri(
                        reverse('portfolio:password_reset_confirm', args=[uid, token])
                    )
                    messages.warning(
                        self.request,
                        ui_t('msg.smtp_fallback', request=self.request, link=link),
                    )
                    return redirect('portfolio:password_reset')
            messages.error(
                self.request,
                ui_t('msg.smtp_error', request=self.request),
            )
            return redirect('portfolio:password_reset')


class SafeLoginView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            ip_addr = _client_ip(request) or 'unknown'
            cache_key = f'login-failure-limit:{ip_addr}'
            limited, wait_minutes = _is_rate_limited(
                cache_key,
                settings.LOGIN_RATE_LIMIT_ATTEMPTS,
                settings.LOGIN_RATE_LIMIT_WINDOW_SECONDS,
            )
            if limited:
                messages.error(
                    request,
                    ui_t('msg.login_rate_limited', request=request, wait_minutes=wait_minutes),
                )
                return redirect('portfolio:login')

            if not _verify_recaptcha(request):
                messages.error(request, ui_t('msg.recaptcha_failed', request=request))
                return redirect('portfolio:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        ip_addr = _client_ip(self.request) or 'unknown'
        cache.delete(f'login-failure-limit:{ip_addr}')
        return super().form_valid(form)

    def form_invalid(self, form):
        ip_addr = _client_ip(self.request) or 'unknown'
        cache_key = f'login-failure-limit:{ip_addr}'
        _increase_rate_limit(cache_key, settings.LOGIN_RATE_LIMIT_WINDOW_SECONDS)
        return super().form_invalid(form)


def home(request):
    projects = Project.objects.select_related('category').prefetch_related('screenshots', 'tags').all()
    categories = ProjectCategory.objects.all()
    tags = ProjectTag.objects.all()
    testimonials = Testimonial.objects.filter(is_published=True)[:6]
    client_logos = sorted({item.company.strip() for item in testimonials if item.company and item.company.strip()})
    packages = ServicePackage.objects.filter(is_active=True)[:6]
    newsletter_form = NewsletterSubscribeForm()
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    tag_slug = request.GET.get('tag', '').strip()
    if query:
        projects = projects.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(technologies__icontains=query)
            | Q(result_metrics__icontains=query)
        )
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    if tag_slug:
        projects = projects.filter(tags__slug=tag_slug).distinct()
    if query:
        SearchQueryEvent.objects.create(
            query=query[:200],
            result_count=projects.count(),
            ip_address=_client_ip(request) or None,
        )

    form = ContactMessageForm()
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            if not _verify_recaptcha(request):
                messages.error(request, ui_t('msg.recaptcha_failed', request=request))
                return redirect('portfolio:home')

            ip_addr = _client_ip(request) or 'unknown'
            throttle_key = f'contact-submit:{ip_addr}'
            current_attempts = cache.get(throttle_key, 0)
            if current_attempts >= settings.CONTACT_THROTTLE_LIMIT:
                wait_minutes = max(1, settings.CONTACT_THROTTLE_WINDOW_SECONDS // 60)
                messages.error(
                    request,
                    ui_t('msg.contact_throttle', request=request, wait_minutes=wait_minutes),
                )
                return redirect('portfolio:home')

            message_obj = form.save()
            message_obj.hero_variant = request.COOKIES.get('hero_variant', '')
            message_obj.save(update_fields=['hero_variant'])
            send_contact_notifications_task(message_obj.pk)
            _track_funnel_event(request, 'contact_submit', message_obj.hero_variant)
            cache.set(
                throttle_key,
                current_attempts + 1,
                timeout=settings.CONTACT_THROTTLE_WINDOW_SECONDS,
            )
            messages.success(request, ui_t('msg.contact_sent', request=request))
            return redirect('portfolio:home')

    featured_projects = projects.filter(is_featured=True)[:3]
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]

    variant = _get_or_set_ab_variant(request)
    _track_funnel_event(request, 'home_view', variant)
    session_language = ''
    if hasattr(request, 'session'):
        session_language = request.session.get(settings.LANGUAGE_COOKIE_NAME, '')
    language = normalize_language(session_language or getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE))
    if request.user.is_authenticated and not session_language:
        pref = UserPreference.objects.filter(user=request.user).only('language').first()
        if pref and pref.language:
            language = normalize_language(pref.language)
    hero_title, hero_lead = _hero_text(variant, language)
    context = {
        'projects': projects,
        'featured_projects': featured_projects,
        'query': query,
        'selected_category': category_slug,
        'selected_tag': tag_slug,
        'categories': categories,
        'tags': tags,
        'form': form,
        'hero_title': hero_title,
        'hero_lead': hero_lead,
        'hero_variant': variant,
        'latest_posts': latest_posts,
        'testimonials': testimonials,
        'client_logos': client_logos,
        'packages': packages,
        'newsletter_form': newsletter_form,
        'has_otp': HAS_OTP,
    }
    response = render(request, 'portfolio/home.html', context)
    response.set_cookie('hero_variant', variant, max_age=60 * 60 * 24 * 30)
    if _track_variant_event(request, variant):
        response.set_cookie('hero_variant_logged', timezone.localdate().isoformat(), max_age=60 * 60 * 24)
    return response


def project_detail(request, pk):
    project = get_object_or_404(Project.objects.prefetch_related('screenshots'), pk=pk)
    steps = [line.strip() for line in project.how_it_works.splitlines() if line.strip()]
    ProjectViewEvent.objects.create(project=project, ip_address=_client_ip(request) or None)
    _track_funnel_event(request, 'project_view', request.COOKIES.get('hero_variant', ''))
    return render(
        request,
        'portfolio/project_detail.html',
        {'project': project, 'steps': steps},
    )


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'portfolio/blog_list.html', {'page_obj': page_obj})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'portfolio/blog_detail.html', {'post': post})


def health_check(request):
    checks = {'db': 'ok'}
    status = 'ok'
    details = []

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
    except Exception as exc:
        checks['db'] = 'error'
        status = 'degraded'
        details.append(f'db: {exc}')

    if status != 'ok':
        _healthcheck_alert('\n'.join(details) or 'unknown health error')

    return JsonResponse(
        {
            'status': status,
            'checks': checks,
            'timestamp': timezone.now().isoformat(),
        },
        status=200 if status == 'ok' else 503,
    )


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        f'Sitemap: {request.build_absolute_uri("/sitemap.xml")}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def signup(request):
    if request.user.is_authenticated:
        return redirect('portfolio:home')

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = settings.SIGNUP_AUTO_ACTIVATE
            user.is_staff = settings.SIGNUP_AUTO_STAFF
            user.is_superuser = settings.SIGNUP_AUTO_SUPERUSER
            user.save(update_fields=['is_active', 'is_staff', 'is_superuser'])

            if user.is_active:
                messages.success(request, ui_t('msg.signup_active', request=request))
                return redirect('portfolio:login')

            token = EmailVerificationToken.objects.create(user=user)
            current_site_url = request.build_absolute_uri('/').rstrip('/')
            send_verification_email_task(user.pk, str(token.token), current_site_url)
            messages.success(request, ui_t('msg.signup_verify', request=request))
            return redirect('portfolio:login')

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    preference, _ = UserPreference.objects.get_or_create(user=request.user)
    return render(
        request,
        'portfolio/profile.html',
        {
            'preference': preference,
            'otp_enabled': HAS_OTP and TOTPDevice.objects.filter(user=request.user, confirmed=True).exists() if HAS_OTP else False,
            'has_otp': HAS_OTP,
        },
    )


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('portfolio:home')


def verify_email(request, token):
    token_obj = EmailVerificationToken.objects.filter(token=token, is_used=False).select_related('user').first()
    if not token_obj:
        messages.error(request, ui_t('msg.verify_invalid', request=request))
        return redirect('portfolio:login')

    user = token_obj.user
    user.is_active = True
    user.save(update_fields=['is_active'])
    token_obj.is_used = True
    token_obj.save(update_fields=['is_used'])
    messages.success(request, ui_t('msg.verify_success', request=request))
    return redirect('portfolio:login')


def newsletter_subscribe(request):
    if request.method != 'POST':
        return redirect('portfolio:home')
    form = NewsletterSubscribeForm(request.POST)
    if form.is_valid():
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=form.cleaned_data['email'].strip().lower(),
            defaults={'is_active': True, 'source': 'website'},
        )
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save(update_fields=['is_active'])
        send_newsletter_notification_task(subscriber.email)
        messages.success(request, ui_t('msg.newsletter_success', request=request))
    else:
        messages.error(request, ui_t('msg.newsletter_error', request=request))
    return redirect('portfolio:home')


def booking_request_view(request):
    if settings.BOOKING_EXTERNAL_URL:
        return redirect(settings.BOOKING_EXTERNAL_URL)
    form = BookingRequestForm()
    booking_slots = _build_booking_slots()
    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            if not _verify_recaptcha(request):
                messages.error(request, ui_t('msg.recaptcha_failed', request=request))
                return redirect('portfolio:booking')
            form.save()
            messages.success(request, ui_t('msg.booking_success', request=request))
            return redirect('portfolio:home')
    return render(
        request,
        'portfolio/booking.html',
        {
            'form': form,
            'booking_slots': booking_slots,
        },
    )


@login_required
def set_theme(request):
    if request.method != 'POST':
        return redirect('portfolio:profile')
    theme = request.POST.get('theme', 'dark')
    if theme not in ('dark', 'light'):
        theme = 'dark'
    pref, _ = UserPreference.objects.get_or_create(user=request.user)
    pref.theme = theme
    pref.save(update_fields=['theme', 'updated_at'])
    return redirect('portfolio:profile')


def set_language_preference(request):
    if request.method not in ('POST', 'GET'):
        return redirect('portfolio:home')
    data = request.POST if request.method == 'POST' else request.GET
    code = data.get('language', settings.LANGUAGE_CODE)
    supported = {item[0] for item in settings.LANGUAGES}
    if code not in supported:
        code = settings.LANGUAGE_CODE
    activate(code)
    request.session[settings.LANGUAGE_COOKIE_NAME] = code
    if request.user.is_authenticated:
        pref, _ = UserPreference.objects.get_or_create(user=request.user)
        pref.language = code
        pref.save(update_fields=['language', 'updated_at'])
    next_url = data.get('next') or request.META.get('HTTP_REFERER', '')
    if not next_url.startswith('/'):
        next_url = reverse('portfolio:home')
    response = redirect(next_url)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        code,
        max_age=getattr(settings, 'LANGUAGE_COOKIE_AGE', 60 * 60 * 24 * 365),
        path=getattr(settings, 'LANGUAGE_COOKIE_PATH', '/'),
    )
    return response


@login_required
def otp_setup(request):
    if not HAS_OTP:
        messages.error(request, ui_t('msg.otp_package_missing', request=request))
        return redirect('portfolio:profile')
    device = TOTPDevice.objects.filter(user=request.user, name='default').first()
    if not device:
        device = TOTPDevice.objects.create(user=request.user, name='default', confirmed=False)
    config_url = device.config_url
    return render(request, 'portfolio/otp_setup.html', {'device': device, 'config_url': config_url})


@login_required
def otp_verify(request):
    if not HAS_OTP:
        return redirect('portfolio:profile')
    device = TOTPDevice.objects.filter(user=request.user, name='default').first()
    if not device:
        messages.error(request, ui_t('msg.otp_setup_first', request=request))
        return redirect('portfolio:otp_setup')
    form = OTPTokenForm()
    if request.method == 'POST':
        form = OTPTokenForm(request.POST)
        if form.is_valid():
            if device.verify_token(form.cleaned_data['token']):
                device.confirmed = True
                device.save(update_fields=['confirmed'])
                request.session['otp_verified'] = True
                messages.success(request, ui_t('msg.otp_enabled', request=request))
                return redirect('portfolio:profile')
            messages.error(request, ui_t('msg.otp_invalid', request=request))
    return render(request, 'portfolio/otp_verify.html', {'form': form})


def manifest_json(request):
    data = {
        "name": "Inomjon Portfolio",
        "short_name": "Portfolio",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#081321",
        "theme_color": "#16c784",
        "icons": [
            {"src": settings.STATIC_URL + "brand/favicon.svg", "sizes": "any", "type": "image/svg+xml"}
        ],
    }
    return JsonResponse(data)


def service_worker(request):
    js = """
self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (event) { event.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', function () {});
"""
    return HttpResponse(js, content_type='application/javascript')
