import importlib.util
import smtplib
import unittest
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core import mail
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import (
    BlogPost,
    ContactMessage,
    EmailVerificationToken,
    HeroExperimentEvent,
    NewsletterSubscriber,
    Project,
    ProjectCategory,
    ProjectTag,
    ProjectViewEvent,
    SearchQueryEvent,
)


class CoreEndpointsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = ProjectCategory.objects.create(name='E-commerce', slug='ecommerce')
        self.tag = ProjectTag.objects.create(name='django', slug='django')
        self.project = Project.objects.create(
            title='CRM Backend',
            short_description='Powerful backend',
            how_it_works='Step 1\nStep 2',
            technologies='Django, PostgreSQL',
            result_metrics='Latency -35%',
            category=self.category,
            created_at='2026-02-01',
        )
        self.project.tags.add(self.tag)
        self.post = BlogPost.objects.create(
            title='Test post',
            slug='test-post',
            summary='Summary',
            content='Body',
            meta_title='SEO title',
            meta_description='SEO desc',
            is_published=True,
            published_at='2026-02-01',
        )

    def tearDown(self):
        cache.clear()

    def test_healthz_endpoint(self):
        response = self.client.get(reverse('portfolio:health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('status'), 'ok')

    def test_sitemap_available(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertIn('xml', response['Content-Type'])

    def test_blog_pages_open(self):
        self.assertEqual(self.client.get(reverse('portfolio:blog_list')).status_code, 200)
        detail_response = self.client.get(reverse('portfolio:blog_detail', args=[self.post.slug]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'SEO title')
        self.assertContains(detail_response, 'SEO desc')

    def test_home_sets_ab_cookie(self):
        response = self.client.get(reverse('portfolio:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('hero_variant', response.cookies)

    def test_project_filter_by_category_and_tag(self):
        response = self.client.get(reverse('portfolio:home'), {'category': self.category.slug, 'tag': self.tag.slug})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)

    def test_project_detail_tracks_view_event(self):
        self.assertEqual(ProjectViewEvent.objects.count(), 0)
        response = self.client.get(reverse('portfolio:project_detail', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProjectViewEvent.objects.count(), 1)

    def test_project_detail_shows_before_after_metrics(self):
        self.project.metric_before = 'Latency 1.8s'
        self.project.metric_after = 'Latency 280ms'
        self.project.save(update_fields=['metric_before', 'metric_after'])
        response = self.client.get(reverse('portfolio:project_detail', args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Latency 1.8s')
        self.assertContains(response, 'Latency 280ms')

    def test_language_switch_to_english_updates_ui(self):
        response = self.client.get(
            reverse('portfolio:set_language'),
            {'language': 'en', 'next': reverse('portfolio:home')},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projects')
        self.assertContains(response, 'Contact')

    def test_language_switch_to_russian_updates_ui(self):
        response = self.client.get(
            reverse('portfolio:set_language'),
            {'language': 'ru', 'next': reverse('portfolio:home')},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Проекты')
        self.assertContains(response, 'Контакты')

    def test_search_tracks_query_event(self):
        self.assertEqual(SearchQueryEvent.objects.count(), 0)
        response = self.client.get(reverse('portfolio:home'), {'q': 'CRM'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SearchQueryEvent.objects.count(), 1)
        self.assertEqual(SearchQueryEvent.objects.first().query, 'CRM')

    def test_contact_honeypot_blocks_submission(self):
        payload = {
            'full_name': 'Bot',
            'email': 'bot@example.com',
            'message': 'Spam',
            'website': 'http://spam',
        }
        response = self.client.post(reverse('portfolio:home'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    @override_settings(CONTACT_THROTTLE_LIMIT=1, CONTACT_THROTTLE_WINDOW_SECONDS=600)
    def test_contact_throttle_blocks_repeated_submissions(self):
        HeroExperimentEvent.objects.create(variant='A', page='home')
        payload = {
            'full_name': 'Ali',
            'email': 'ali@example.com',
            'message': 'Salom',
            'website': '',
        }
        first = self.client.post(reverse('portfolio:home'), data=payload, follow=True)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)

        second = self.client.post(reverse('portfolio:home'), data=payload, follow=True)
        self.assertEqual(second.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_rss_feed_available(self):
        response = self.client.get(reverse('portfolio:blog_feed'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('xml', response['Content-Type'])

    def test_manifest_available(self):
        response = self.client.get(reverse('portfolio:manifest_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('name'), 'Inomjon Portfolio')

    def test_newsletter_subscribe(self):
        payload = {'email': 'news@example.com'}
        response = self.client.post(reverse('portfolio:newsletter_subscribe'), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(NewsletterSubscriber.objects.filter(email='news@example.com').exists())


@unittest.skipUnless(importlib.util.find_spec('rest_framework') is not None, 'DRF not installed')
class ApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        project = Project.objects.create(
            title='API project',
            short_description='API project desc',
            how_it_works='Step',
            technologies='Django',
            created_at='2026-02-01',
        )
        BlogPost.objects.create(
            title='API post',
            slug='api-post',
            summary='summary',
            content='body',
            is_published=True,
            published_at='2026-02-01',
        )
        self.project_id = project.pk

    def test_project_api_list(self):
        response = self.client.get(reverse('portfolio:api_project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_blog_api_detail(self):
        response = self.client.get(reverse('portfolio:api_blog_detail', args=['api-post']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('slug'), 'api-post')


class AuthFlowTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='StrongPass123',
        )

    def test_signup_page_open(self):
        response = self.client.get(reverse('portfolio:signup'))
        self.assertEqual(response.status_code, 200)

    @override_settings(
        SIGNUP_AUTO_ACTIVATE=False,
        SIGNUP_AUTO_STAFF=False,
        SIGNUP_AUTO_SUPERUSER=False,
    )
    def test_signup_creates_user(self):
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'AnotherStrong123',
            'password2': 'AnotherStrong123',
        }
        response = self.client.post(reverse('portfolio:signup'), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertFalse(User.objects.get(username='newuser').is_active)
        self.assertTrue(EmailVerificationToken.objects.filter(user__username='newuser').exists())

    @override_settings(
        SIGNUP_AUTO_ACTIVATE=True,
        SIGNUP_AUTO_STAFF=True,
        SIGNUP_AUTO_SUPERUSER=True,
    )
    def test_signup_auto_promotes_when_flags_enabled(self):
        payload = {
            'username': 'autoadmin',
            'email': 'autoadmin@example.com',
            'password1': 'AnotherStrong123',
            'password2': 'AnotherStrong123',
        }
        response = self.client.post(reverse('portfolio:signup'), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username='autoadmin')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertFalse(EmailVerificationToken.objects.filter(user=user).exists())

    @override_settings(
        SIGNUP_AUTO_ACTIVATE=True,
        SIGNUP_AUTO_STAFF=True,
        SIGNUP_AUTO_SUPERUSER=True,
    )
    def test_new_user_created_outside_signup_also_gets_auto_flags(self):
        user = User.objects.create_user(
            username='externalcreate',
            email='externalcreate@example.com',
            password='StrongPass123',
        )
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    @override_settings(
        SIGNUP_AUTO_ACTIVATE=False,
        SIGNUP_AUTO_STAFF=False,
        SIGNUP_AUTO_SUPERUSER=False,
    )
    def test_new_user_created_outside_signup_respects_disabled_flags(self):
        user = User.objects.create_user(
            username='externalcreate2',
            email='externalcreate2@example.com',
            password='StrongPass123',
        )
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('portfolio:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_opens_for_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('portfolio:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tester')

    def test_booking_page_shows_slot_section(self):
        response = self.client.get(reverse('portfolio:booking'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tayyor slotlar")

    def test_authenticated_user_can_switch_language_from_header_select(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('portfolio:set_language'),
            {'language': 'ru', 'next': reverse('portfolio:home')},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Проекты')
        self.assertContains(response, 'Контакты')

    def test_password_reset_flow_pages_open(self):
        form_response = self.client.get(reverse('portfolio:password_reset'))
        self.assertEqual(form_response.status_code, 200)
        done_response = self.client.post(
            reverse('portfolio:password_reset'),
            {'email': 'tester@example.com'},
            follow=True,
        )
        self.assertEqual(done_response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(
        DEBUG=True,
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    )
    @patch(
        'portfolio.forms.EmailMultiAlternatives.send',
        side_effect=smtplib.SMTPAuthenticationError(535, b'Bad credentials'),
    )
    def test_password_reset_debug_fallback_when_smtp_fails(self, _send_mock):
        response = self.client.post(
            reverse('portfolio:password_reset'),
            {'email': 'tester@example.com'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.get('PATH_INFO'), reverse('portfolio:password_reset'))
        self.assertContains(response, 'SMTP ishlamadi. Vaqtinchalik reset link:')
        self.assertContains(response, '/accounts/reset/')

    @override_settings(
        DEBUG=False,
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
    )
    @patch(
        'portfolio.forms.EmailMultiAlternatives.send',
        side_effect=smtplib.SMTPAuthenticationError(535, b'Bad credentials'),
    )
    def test_password_reset_error_message_when_smtp_fails(self, _send_mock):
        response = self.client.post(
            reverse('portfolio:password_reset'),
            {'email': 'tester@example.com'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.get('PATH_INFO'), reverse('portfolio:password_reset'))
        self.assertContains(response, 'Email yuborishda xatolik.')

    @override_settings(RECAPTCHA_SITE_KEY='test-site-key')
    def test_login_page_renders_recaptcha_widget_when_enabled(self):
        response = self.client.get(reverse('portfolio:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'g-recaptcha')

    @override_settings(LOGIN_RATE_LIMIT_ATTEMPTS=1, LOGIN_RATE_LIMIT_WINDOW_SECONDS=600)
    def test_login_rate_limit_blocks_repeated_failures(self):
        first = self.client.post(reverse('portfolio:login'), {'username': 'tester', 'password': 'wrong-pass'}, follow=True)
        self.assertEqual(first.status_code, 200)
        second = self.client.post(reverse('portfolio:login'), {'username': 'tester', 'password': 'wrong-pass'}, follow=True)
        self.assertEqual(second.status_code, 200)
        self.assertContains(second, 'Kirish urinishlari cheklangan.')

    @override_settings(PASSWORD_RESET_RATE_LIMIT_ATTEMPTS=1, PASSWORD_RESET_RATE_LIMIT_WINDOW_SECONDS=600)
    def test_password_reset_rate_limit_blocks_repeated_requests(self):
        first = self.client.post(reverse('portfolio:password_reset'), {'email': 'tester@example.com'}, follow=True)
        self.assertEqual(first.status_code, 200)
        second = self.client.post(reverse('portfolio:password_reset'), {'email': 'tester@example.com'}, follow=True)
        self.assertEqual(second.status_code, 200)
        self.assertContains(second, 'Parol tiklash urinishlari ko')
