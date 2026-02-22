from io import BytesIO
from pathlib import Path
import uuid

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image
from django.urls import reverse


class ProjectCategory(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name='Kategoriya nomi')
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Project category'
        verbose_name_plural = 'Project categories'

    def __str__(self):
        return self.name


class ProjectTag(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name='Tag nomi')
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Project tag'
        verbose_name_plural = 'Project tags'

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=120, verbose_name='Nomi')
    short_description = models.TextField(verbose_name='Qisqa tavsif')
    result_metrics = models.TextField(
        blank=True,
        default='',
        verbose_name='Natija metrikalari',
        help_text='Masalan: Response time 40% ga qisqardi, conversion 18% oshdi.',
    )
    metric_before = models.CharField(
        max_length=180,
        blank=True,
        default='',
        verbose_name='Before metrika',
        help_text='Masalan: API response 1.8s',
    )
    metric_after = models.CharField(
        max_length=180,
        blank=True,
        default='',
        verbose_name='After metrika',
        help_text='Masalan: API response 320ms',
    )
    how_it_works = models.TextField(
        verbose_name='Qanday ishlaydi',
        help_text='Har bir bosqichni yangi qatordan yozing.',
    )
    technologies = models.CharField(
        max_length=255,
        verbose_name='Texnologiyalar',
        help_text='Masalan: Django, DRF, PostgreSQL',
    )
    github_url = models.URLField(blank=True, verbose_name='GitHub havolasi')
    live_url = models.URLField(blank=True, verbose_name='Demo havolasi')
    demo_video_url = models.URLField(blank=True, default='', verbose_name='Demo video URL')
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name='Rasm')
    is_featured = models.BooleanField(default=False, verbose_name='Asosiy loyihami?')
    category = models.ForeignKey(
        ProjectCategory,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='projects',
        verbose_name='Kategoriya',
    )
    tags = models.ManyToManyField(ProjectTag, blank=True, related_name='projects', verbose_name='Taglar')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')
    created_at = models.DateField(verbose_name='Yaratilgan sana')

    class Meta:
        ordering = ('order', '-created_at')
        verbose_name = 'Loyiha'
        verbose_name_plural = 'Loyihalar'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', args=[self.pk])

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.lower().endswith('.webp'):
            img = Image.open(self.image)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            output = BytesIO()
            img.save(output, format='WEBP', quality=82, optimize=True)
            output.seek(0)

            base_name = Path(self.image.name).stem
            self.image.save(f'{base_name}.webp', ContentFile(output.read()), save=False)

        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=120, verbose_name='F.I.O')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Xabar')
    hero_variant = models.CharField(max_length=1, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yuborilgan vaqt')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Xabar'
        verbose_name_plural = 'Xabarlar'

    def __str__(self):
        return f'{self.full_name} - {self.email}'


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='project_screenshots/', verbose_name='Screenshot')
    caption = models.CharField(max_length=160, blank=True, verbose_name='Izoh')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')

    class Meta:
        ordering = ('order', 'id')
        verbose_name = 'Project screenshot'
        verbose_name_plural = 'Project screenshots'

    def __str__(self):
        return f'{self.project.title} - screenshot'


class BlogPost(models.Model):
    title = models.CharField(max_length=180, verbose_name='Sarlavha')
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.TextField(verbose_name='Qisqa mazmun')
    content = models.TextField(verbose_name='Kontent')
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name='Cover rasm')
    meta_title = models.CharField(max_length=180, blank=True, default='', verbose_name='SEO title')
    meta_description = models.CharField(max_length=260, blank=True, default='', verbose_name='SEO description')
    is_published = models.BooleanField(default=True, verbose_name='Nashr qilinganmi')
    published_at = models.DateField(verbose_name='Nashr sanasi')

    class Meta:
        ordering = ('-published_at',)
        verbose_name = 'Blog post'
        verbose_name_plural = 'Blog posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:blog_detail', args=[self.slug])


class HeroExperimentEvent(models.Model):
    variant = models.CharField(max_length=1, choices=(('A', 'A'), ('B', 'B')))
    page = models.CharField(max_length=120, default='home')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Hero experiment event'
        verbose_name_plural = 'Hero experiment events'

    def __str__(self):
        return f'{self.page}:{self.variant}'


class ProjectViewEvent(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='view_events')
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Project view event'
        verbose_name_plural = 'Project view events'

    def __str__(self):
        return f'{self.project.title} view'


class SearchQueryEvent(models.Model):
    query = models.CharField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    result_count = models.PositiveIntegerField(default=0)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Search query event'
        verbose_name_plural = 'Search query events'

    def __str__(self):
        return self.query


class Testimonial(models.Model):
    full_name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True, default='')
    company = models.CharField(max_length=120, blank=True, default='')
    feedback = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.full_name} ({self.rating}/5)'


class ServicePackage(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField()
    price_label = models.CharField(max_length=120, help_text='Masalan: $499 yoki Kelishiladi')
    features = models.TextField(help_text='Har bir feature yangi qatorda')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('order', 'name')

    def __str__(self):
        return self.name


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    source = models.CharField(max_length=80, default='website')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.email


class UserPreference(models.Model):
    THEME_CHOICES = (('dark', 'Dark'), ('light', 'Light'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='dark')
    language = models.CharField(max_length=10, default='uz')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} preference'


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user.username} verification token'


class FunnelEvent(models.Model):
    STAGE_CHOICES = (
        ('home_view', 'Home View'),
        ('project_view', 'Project View'),
        ('contact_submit', 'Contact Submit'),
    )
    stage = models.CharField(max_length=40, choices=STAGE_CHOICES)
    variant = models.CharField(max_length=1, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.stage}:{self.variant}'


class AuditLog(models.Model):
    action = models.CharField(max_length=160)
    path = models.CharField(max_length=260)
    method = models.CharField(max_length=10)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.method} {self.path}'


class BookingRequest(models.Model):
    STATUS_CHOICES = (('new', 'New'), ('done', 'Done'), ('canceled', 'Canceled'))
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    preferred_datetime = models.DateTimeField()
    note = models.TextField(blank=True, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.full_name} ({self.preferred_datetime})'
