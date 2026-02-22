from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.template.response import TemplateResponse
from django.urls import path
from django.utils import timezone
from datetime import timedelta

from .models import (
    AuditLog,
    BlogPost,
    BookingRequest,
    ContactMessage,
    EmailVerificationToken,
    FunnelEvent,
    HeroExperimentEvent,
    NewsletterSubscriber,
    Project,
    ProjectCategory,
    ProjectScreenshot,
    ProjectTag,
    ProjectViewEvent,
    ServicePackage,
    SearchQueryEvent,
    Testimonial,
    UserPreference,
)


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'created_at', 'order', 'demo_video_url', 'metric_before', 'metric_after')
    list_filter = ('is_featured', 'created_at', 'category', 'tags')
    search_fields = ('title', 'short_description', 'technologies', 'result_metrics', 'metric_before', 'metric_after')
    list_editable = ('is_featured', 'order')
    inlines = [ProjectScreenshotInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'created_at')
    search_fields = ('full_name', 'email', 'message')
    readonly_fields = ('full_name', 'email', 'message', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_at', 'meta_title')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'summary', 'content', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating', 'created_at')
    search_fields = ('full_name', 'company', 'feedback')


@admin.register(ServicePackage)
class ServicePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_label', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'features')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'source', 'created_at')
    list_filter = ('is_active', 'source', 'created_at')
    search_fields = ('email',)


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'language', 'updated_at')
    search_fields = ('user__username', 'user__email')


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'is_used', 'created_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('token', 'created_at')


@admin.register(FunnelEvent)
class FunnelEventAdmin(admin.ModelAdmin):
    list_display = ('stage', 'variant', 'ip_address', 'created_at')
    list_filter = ('stage', 'variant', 'created_at')
    readonly_fields = ('stage', 'variant', 'ip_address', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'method', 'path', 'user', 'ip_address', 'created_at')
    list_filter = ('method', 'created_at')
    search_fields = ('action', 'path', 'user__username')
    readonly_fields = ('action', 'method', 'path', 'user', 'ip_address', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'preferred_datetime', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('full_name', 'email', 'note')
    list_editable = ('status',)


@admin.register(HeroExperimentEvent)
class HeroExperimentEventAdmin(admin.ModelAdmin):
    list_display = ('variant', 'page', 'created_at')
    list_filter = ('variant', 'page', 'created_at')
    readonly_fields = ('variant', 'page', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProjectViewEvent)
class ProjectViewEventAdmin(admin.ModelAdmin):
    list_display = ('project', 'ip_address', 'created_at')
    list_filter = ('project', 'created_at')
    readonly_fields = ('project', 'ip_address', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(SearchQueryEvent)
class SearchQueryEventAdmin(admin.ModelAdmin):
    list_display = ('query', 'result_count', 'ip_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('query',)
    readonly_fields = ('query', 'result_count', 'ip_address', 'created_at')

    def has_add_permission(self, request):
        return False


def analytics_dashboard_view(request):
    top_projects = (
        Project.objects.annotate(view_count=Count('view_events'))
        .order_by('-view_count', 'title')[:10]
    )
    top_queries = (
        SearchQueryEvent.objects.values('query')
        .annotate(total=Count('id'))
        .order_by('-total', 'query')[:10]
    )

    variants = {}
    for variant in ('A', 'B'):
        exposures = HeroExperimentEvent.objects.filter(variant=variant).count()
        conversions = ContactMessage.objects.filter(hero_variant=variant).count()
        rate = round((conversions / exposures) * 100, 2) if exposures else 0
        variants[variant] = {
            'exposures': exposures,
            'conversions': conversions,
            'conversion_rate': rate,
        }
    funnel = {
        'home_view': FunnelEvent.objects.filter(stage='home_view').count(),
        'project_view': FunnelEvent.objects.filter(stage='project_view').count(),
        'contact_submit': FunnelEvent.objects.filter(stage='contact_submit').count(),
    }

    funnel_rows = [
        ('Home view', funnel['home_view']),
        ('Project view', funnel['project_view']),
        ('Contact submit', funnel['contact_submit']),
    ]
    max_funnel = max([value for _, value in funnel_rows] + [1])
    funnel_chart = [
        {
            'label': label,
            'value': value,
            'percent': round((value / max_funnel) * 100, 2) if max_funnel else 0,
        }
        for label, value in funnel_rows
    ]

    start_day = timezone.localdate() - timedelta(days=13)
    days = [start_day + timedelta(days=index) for index in range(14)]

    daily_funnel = (
        FunnelEvent.objects.filter(created_at__date__gte=start_day)
        .annotate(day=TruncDate('created_at'))
        .values('day', 'stage')
        .annotate(total=Count('id'))
    )
    day_map = {day.isoformat(): {'home_view': 0, 'project_view': 0, 'contact_submit': 0} for day in days}
    for row in daily_funnel:
        key = row['day'].isoformat()
        if key in day_map:
            day_map[key][row['stage']] = row['total']

    daily_rows = []
    daily_max = 1
    for day in days:
        values = day_map[day.isoformat()]
        total = values['home_view'] + values['project_view'] + values['contact_submit']
        daily_max = max(daily_max, total)
        daily_rows.append(
            {
                'day': day.strftime('%d %b'),
                'home_view': values['home_view'],
                'project_view': values['project_view'],
                'contact_submit': values['contact_submit'],
                'total': total,
            }
        )
    for row in daily_rows:
        row['total_percent'] = round((row['total'] / daily_max) * 100, 2) if daily_max else 0

    context = {
        **admin.site.each_context(request),
        'title': 'Portfolio analytics',
        'top_projects': top_projects,
        'top_queries': top_queries,
        'variants': variants,
        'funnel': funnel,
        'funnel_chart': funnel_chart,
        'daily_rows': daily_rows,
    }
    return TemplateResponse(request, 'admin/portfolio_analytics.html', context)


_original_get_urls = admin.site.get_urls


def _analytics_urls():
    return [path('portfolio-analytics/', admin.site.admin_view(analytics_dashboard_view), name='portfolio_analytics')]


def _patched_get_urls():
    return _analytics_urls() + _original_get_urls()


admin.site.get_urls = _patched_get_urls
