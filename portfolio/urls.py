import importlib.util

from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy

from . import views
from .feeds import LatestPostsFeed

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/feed/', LatestPostsFeed(), name='blog_feed'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('healthz/', views.health_check, name='health_check'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/login/', views.SafeLoginView.as_view(), name='login'),
    path('accounts/logout/', views.signout, name='logout'),
    path('accounts/otp/setup/', views.otp_setup, name='otp_setup'),
    path('accounts/otp/verify/', views.otp_verify, name='otp_verify'),
    path('accounts/theme/', views.set_theme, name='set_theme'),
    path('accounts/language/', views.set_language_preference, name='set_language'),
    path(
        'accounts/password-reset/',
        views.SafePasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url=reverse_lazy('portfolio:password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'accounts/password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url=reverse_lazy('portfolio:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'accounts/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete',
    ),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('booking/', views.booking_request_view, name='booking'),
    path('manifest.json', views.manifest_json, name='manifest_json'),
    path('sw.js', views.service_worker, name='service_worker'),
]

if importlib.util.find_spec('rest_framework') is not None:
    from . import api_views

    urlpatterns += [
        path('api/projects/', api_views.ProjectListAPIView.as_view(), name='api_project_list'),
        path('api/projects/<int:pk>/', api_views.ProjectDetailAPIView.as_view(), name='api_project_detail'),
        path('api/blog/', api_views.BlogPostListAPIView.as_view(), name='api_blog_list'),
        path('api/blog/<slug:slug>/', api_views.BlogPostDetailAPIView.as_view(), name='api_blog_detail'),
        path('api/services/', api_views.ServicePackageListAPIView.as_view(), name='api_service_list'),
    ]
