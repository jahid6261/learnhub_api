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
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import IntegrityError
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
    def get_queryset(self):
        user = self.request.user
        
 
        if user.is_authenticated and user.role == 'teacher':
            return Course.objects.filter(instructor=user)
        
        
        return Course.objects.all()
        
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
     
class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializers
    permission_classes = [EnrollmentPermission]
    
    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        course_id = self.kwargs.get('course_pk')
        
        
        if user.is_staff or role == 'admin':
            qs = Enrollment.objects.all()
        

        elif role == 'teacher':
            qs = Enrollment.objects.filter(course__instructor=user)
        
        
        elif role == 'student':
            qs = Enrollment.objects.filter(student=user, is_active=True)
        
        else:
            return Enrollment.objects.none()
        
       
        if course_id:
            qs = qs.filter(course_id=course_id)
        
        return qs
    
    def create(self, request, *args, **kwargs):
        """Student নিজে নিজে এনরোল করবে"""
        user = request.user
        role = getattr(user, 'role', None)
        course_id = self.kwargs.get('course_pk')
        
     
        if role != 'student':
            return Response(
                {'error': 'Only students can enroll themselves'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {'error': 'Course not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
       
        if course.instructor == user:
            return Response(
                {'error': 'You cannot enroll in your own course'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        
        if Enrollment.objects.filter(student=user, course=course).exists():
            return Response(
                {'error': 'Already enrolled in this course'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
       
        try:
            enrollment = Enrollment.objects.create(
                student=user,
                course=course,
                price=course.price
            )
            serializer = self.get_serializer(enrollment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        
       
      
      
        
     

       
       



      
       
    
        



