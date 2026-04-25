from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from courses.models import Category,Course,Lesson,Material
from courses.serializers import CategorySerializers,CourseSerializers,LessonSerializers,MaterialSerializers

from api.permissions import IsAdminOrReadOnly
from courses.permissions import IsInstructorOrReadOnly,IsLessonManagerOrStudent,IsMaterialManagerorStudent
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
        
class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializers
    permission_classes = [IsLessonManagerOrStudent]
    
    def get_queryset(self):
     user = self.request.user
     course_id = self.kwargs.get('course_pk')
     role = getattr(user, 'role', None)

     if user.is_staff or role == 'admin':
        qs = Lesson.objects.all()
     elif role == 'teacher':
      
        qs = Lesson.objects.filter(course__instructor=user)
     elif role == 'student':
        qs = Lesson.objects.filter(
            course__enrollments__student=user,
            course__enrollments__is_active=True
        ).distinct()
     else:
        return Lesson.objects.none()


     if course_id:
        qs = qs.filter(course_id=course_id)

     return qs


class MaterialViewSet(ModelViewSet):
    serializer_class = MaterialSerializers
    permission_classes = [IsMaterialManagerorStudent]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        course_id = self.kwargs.get('course_pk')

        if user.is_staff or role == 'admin':
            qs = Material.objects.all()
        

        elif role == 'teacher':
            qs = Material.objects.filter(course__instructor=user)
        
        elif role == 'student':
            qs = Material.objects.filter(
                course__enrollments__student=user,
                course__enrollments__is_active=True
            ).distinct()
        else:
            return Material.objects.none()

        
        if course_id:
            qs = qs.filter(course_id=course_id)
            
        return qs
       
     
       
     

       
       



      
       
    
        



