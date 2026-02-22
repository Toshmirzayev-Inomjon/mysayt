from django.contrib.syndication.views import Feed
from django.urls import reverse

from .models import BlogPost


class LatestPostsFeed(Feed):
    title = "Inomjon Portfolio Blog"
    link = "/blog/feed/"
    description = "Backend bo'yicha yangi maqolalar va case studylar."

    def items(self):
        return BlogPost.objects.filter(is_published=True)[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.meta_description or item.summary

    def item_link(self, item):
        return reverse('portfolio:blog_detail', args=[item.slug])
