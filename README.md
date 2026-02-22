# Django Portfolio (Premium)

![Django](https://img.shields.io/badge/Django-5.2.11-0C4B33?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Deploy](https://img.shields.io/badge/Deploy-Gunicorn%20%2B%20Nginx-2563eb)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-181717?logo=githubactions&logoColor=white)

Premium portfolio sayt: loyihalar, blog, case-study, A/B hero test, monitoring, backup va production deploy bilan.

Demo GIF joyi (`/assets/demo.gif`) uchun README placeholder:

```md
![Demo](assets/demo.gif)
```

## 1–10 topshiriqlar holati
1. Real kontent: `result_metrics` maydoni qo'shildi, loyiha natijalari ko'rsatiladi.
2. Screenshotlar: `ProjectScreenshot` modeli va detail sahifada galereya.
3. Domain + SSL: `deploy/nginx/portfolio-ssl.conf` tayyor.
4. Security: `django-axes` (bruteforce), `django-otp` (2FA infra) qo'llab-quvvatlash.
5. Blog: `blog/` list/detail + RSS (`/blog/feed/`) va SEO maydonlari (`meta_title`, `meta_description`).
6. Contact notification + anti-spam: email/Telegram, honeypot va throttle.
7. Core Web Vitals: Lighthouse script (`scripts/lighthouse.sh`), lazy-load/WebP optimizatsiya.
8. A/B test: hero variant A/B cookie + event tracking (`HeroExperimentEvent`) va konversiya tracking.
9. Backup/restore test: `scripts/verify_backup_restore.sh`.
10. Showcase repo: badge, demo-gif slot, deploy/CI/CD hujjatlangan.

## Yangi qo'shimchalar
- Project taxonomy: `ProjectCategory`, `ProjectTag` hamda home sahifada category/tag filter.
- Analytics dashboard: `/admin/portfolio-analytics/` (eng ko'rilgan loyihalar, top qidiruvlar, A/B conversion).
- API (DRF o'rnatilgan bo'lsa):
  - `/api/projects/`
  - `/api/projects/<id>/`
  - `/api/blog/`
  - `/api/blog/<slug>/`
- Auth:
  - `accounts/signup/` ro'yxatdan o'tish
  - `accounts/verify-email/<token>/` email verifikatsiya
  - `accounts/login/`, `accounts/logout/`
  - `accounts/password-reset/` va to'liq reset flow
  - `accounts/profile/` foydalanuvchi profili
- 2FA: `accounts/otp/setup/`, `accounts/otp/verify/` (`django-otp` bilan).
- Services + pricing: `ServicePackage` modeli, home sahifada paketlar.
- Booking: `booking/` (external URL yoki ichki form).
- Newsletter: `newsletter/subscribe/`.
- i18n: `uz/en/ru` til tanlash.
- Theme preference: user bo'yicha server-side saqlanadi (`UserPreference`).
- Funnel analytics: `FunnelEvent` (`home_view -> project_view -> contact_submit`).
- Async notifications: Celery task wrapper (`portfolio/tasks.py`).
- Audit log: `AuditLog` middleware orqali POST/PUT/PATCH/DELETE requestlar.
- Project demo video: `Project.demo_video_url`.
- PWA: `manifest.json`, `sw.js`.
- Security hardening: CSP/permissions/referrer headers + global rate limit middleware.

## Lokal ishga tushirish
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata portfolio/fixtures/sample_projects.json
python manage.py createsuperuser
python manage.py runserver
```

## Muhim URL'lar
- Home: `http://127.0.0.1:8000/`
- Blog: `http://127.0.0.1:8000/blog/`
- Admin: `http://127.0.0.1:8000/admin/`
- Health: `http://127.0.0.1:8000/healthz/`
- Sitemap: `http://127.0.0.1:8000/sitemap.xml`
- Blog RSS: `http://127.0.0.1:8000/blog/feed/`
- Login: `http://127.0.0.1:8000/accounts/login/`
- Signup: `http://127.0.0.1:8000/accounts/signup/`
- Profile: `http://127.0.0.1:8000/accounts/profile/`
- Booking: `http://127.0.0.1:8000/booking/`
- Manifest: `http://127.0.0.1:8000/manifest.json`
- Service worker: `http://127.0.0.1:8000/sw.js`

## Production deploy (Nginx + Gunicorn + systemd)
1. `.env.example` asosida `.env` yarating.
2. Migratsiya va static:
```bash
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```
3. systemd service:
```bash
sudo cp deploy/systemd/portfolio.service /etc/systemd/system/portfolio.service
sudo systemctl daemon-reload
sudo systemctl enable --now portfolio
```
4. SSL nginx config:
```bash
sudo cp deploy/nginx/portfolio-ssl.conf /etc/nginx/sites-available/portfolio.conf
sudo ln -s /etc/nginx/sites-available/portfolio.conf /etc/nginx/sites-enabled/portfolio.conf
sudo nginx -t && sudo systemctl reload nginx
```

## CI/CD
- Workflow: `.github/workflows/ci-cd.yml`
- `main` branch push: test + remote deploy.

## Backup
- Backup: `scripts/backup.sh`
- Restore: `scripts/restore.sh`
- Verify restore: `scripts/verify_backup_restore.sh`
- systemd timer: `deploy/systemd/portfolio-backup.timer`

## Performance audit
```bash
./scripts/lighthouse.sh http://127.0.0.1:8000
```
Report: `lighthouse-reports/report.html`
