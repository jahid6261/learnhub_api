from django.urls import path, include
from rest_framework_nested import routers
from courses.views import (
    CategoryViewSet, 
    CoursesViewSet, 
    LessonViewSet, 
    MaterialViewSet, 
    EnrollmentViewSet
)

# 1. Main Router setup
router = routers.DefaultRouter()
router.register('courses', CoursesViewSet, basename='courses')
router.register('category', CategoryViewSet, basename='category')







urlpatterns = [
    path('', include(router.urls)),
    
]