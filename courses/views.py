from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from courses.models import Category,Course
from courses.serializers import CategorySerializers,CourseSerializers

from api.permissions import IsAdminOrReadOnly
from courses.permissions import IsInstructorOrReadOnly
from courses.filters import CourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

# Create your views here.

class CategoryViewSet(ModelViewSet):
    
    queryset=Category.objects.annotate(course_count=Count ('course'))
    serializer_class=CategorySerializers
    permission_classes=[IsAdminOrReadOnly]
    
    
    
    
class CoursesViewSet(ModelViewSet):
    queryset=Course.objects.all()
    serializer_class=CourseSerializers
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=CourseFilter
    Search_fields=['name']
    ordering_fields=['price']
    
    permission_classes=[IsInstructorOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    
        



