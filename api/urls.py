from django.urls import path, include
from rest_framework_nested import routers

from courses.views import (
    CategoryViewSet,
    CoursesViewSet,
    LessonViewSet,
    MaterialViewSet,
    EnrollmentViewSet
)

#  Main router
router = routers.DefaultRouter()
router.register('courses', CoursesViewSet, basename='courses')
router.register('category', CategoryViewSet, basename='category')


courses_router = routers.NestedDefaultRouter( router,'courses',  lookup='course')
courses_router.register('lessons',   LessonViewSet,    basename='course-lessons') 

courses_router.register('metrials',MaterialViewSet,basename="course-materials") 
courses_router.register('enrollments', EnrollmentViewSet, basename='course-enrollments')
  
urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)), 
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
]
 
  


  


