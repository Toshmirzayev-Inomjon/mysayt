from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import BlogPost, Project


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return ['portfolio:home', 'portfolio:blog_list', 'portfolio:booking']

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.created_at


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at
