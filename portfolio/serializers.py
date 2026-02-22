from rest_framework import serializers

from .models import BlogPost, Project, ProjectCategory, ProjectTag, ServicePackage


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = ('name', 'slug')


class ProjectTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTag
        fields = ('name', 'slug')


class ProjectSerializer(serializers.ModelSerializer):
    category = ProjectCategorySerializer(read_only=True)
    tags = ProjectTagSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'short_description',
            'result_metrics',
            'technologies',
            'demo_video_url',
            'category',
            'tags',
            'created_at',
            'url',
        )

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return obj.get_absolute_url()
        return request.build_absolute_uri(obj.get_absolute_url())


class BlogPostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = (
            'id',
            'title',
            'slug',
            'summary',
            'meta_title',
            'meta_description',
            'published_at',
            'url',
        )

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return obj.get_absolute_url()
        return request.build_absolute_uri(obj.get_absolute_url())


class ServicePackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePackage
        fields = ('id', 'name', 'slug', 'description', 'price_label', 'features')
