from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from courses.models import Category,Course,Lesson,Material,Enrollment
from courses.serializers import CategorySerializers,CourseSerializers,LessonSerializers,MaterialSerializers,EnrollmentSerializers

from api.permissions import IsAdminOrReadOnly
from courses.permissions import IsInstructorOrReadOnly,IsLessonManagerOrStudent,IsMaterialManagerorStudent,EnrollmentPermission
from courses.filters import CourseFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import generics

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
     
class EnrollmentViewSet(ModelViewSet):
    serializer_class = EnrollmentSerializers
    permission_classes = [ EnrollmentPermission]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Enrollment.objects.all()

        if user.role == 'teacher':
     
            return Enrollment.objects.filter(course__teacher=user)

      
        return Enrollment.objects.filter(student=user)
     
     
    def perform_create(self, serializer):
       course_id = self.kwargs.get('course_pk')
       
       from .models import Course
       course_obj = Course.objects.get(id=course_id)
       
       serializer.save(  
            student=self.request.user, 
            course=course_obj,
            price=course_obj.price
        )
      
       
       
        
        
       
      
      
        
     

       
       



      
       
    
        



