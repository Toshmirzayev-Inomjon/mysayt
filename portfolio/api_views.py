from rest_framework import generics

from .models import BlogPost, Project, ServicePackage
from .serializers import BlogPostSerializer, ProjectSerializer, ServicePackageSerializer


class ProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.select_related('category').prefetch_related('tags').all()
    serializer_class = ProjectSerializer


class ProjectDetailAPIView(generics.RetrieveAPIView):
    queryset = Project.objects.select_related('category').prefetch_related('tags').all()
    serializer_class = ProjectSerializer


class BlogPostListAPIView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(is_published=True).all()
    serializer_class = BlogPostSerializer


class BlogPostDetailAPIView(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = BlogPost.objects.filter(is_published=True).all()
    serializer_class = BlogPostSerializer


class ServicePackageListAPIView(generics.ListAPIView):
    queryset = ServicePackage.objects.filter(is_active=True).all()
    serializer_class = ServicePackageSerializer
