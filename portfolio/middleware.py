import importlib.util

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import AuditLog

HAS_OTP = importlib.util.find_spec('django_otp') is not None
if HAS_OTP:
    from django_otp.plugins.otp_totp.models import TOTPDevice


def _client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


class RequestRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = _client_ip(request) or 'unknown'
        key = f'global-rate-limit:{ip}'
        current = cache.get(key, 0)
        if current >= settings.GLOBAL_RATE_LIMIT_PER_MINUTE:
            return JsonResponse({'detail': 'Too many requests'}, status=429)
        cache.set(key, current + 1, timeout=60)
        return self.get_response(request)


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "media-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "script-src 'self' https://www.google.com https://www.gstatic.com; "
            "frame-src 'self' https://www.google.com https://www.gstatic.com; "
            "connect-src 'self' https://www.google.com https://www.gstatic.com;"
        )
        return response


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            try:
                AuditLog.objects.create(
                    action='request',
                    method=request.method,
                    path=request.path[:260],
                    user=request.user if request.user.is_authenticated else None,
                    ip_address=_client_ip(request) or None,
                )
            except Exception:
                pass
        return response


class OTPEnforceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if HAS_OTP and request.user.is_authenticated:
            protected_prefixes = ('/accounts/profile', '/project/', '/api/')
            skip_prefixes = ('/accounts/otp/', '/accounts/logout/', '/admin/', '/static/', '/sw.js', '/manifest.json')
            if request.path.startswith(skip_prefixes):
                return self.get_response(request)
            if request.path.startswith(protected_prefixes):
                has_device = TOTPDevice.objects.filter(user=request.user, confirmed=True).exists()
                if has_device and not request.session.get('otp_verified'):
                    return redirect('portfolio:otp_verify')
        return self.get_response(request)
