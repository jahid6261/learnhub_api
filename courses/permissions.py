from rest_framework import permissions
from courses.models import Course
class IsInstructorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
     
        if request.method in permissions.SAFE_METHODS:
            return True

     
        if request.method == 'POST':
            return request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_staff
            )

        
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
     
        if request.method in permissions.SAFE_METHODS:
            return True

       
        if request.user.is_staff or request.user.role == 'admin':
            return True

        return obj.instructor == request.user


class IsLessonManagerOrStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user = request.user
        role = getattr(user, 'role', None)

        
        if user.is_staff or role == 'admin':
            return True

     
        if role == 'teacher':
            course_id = view.kwargs.get('course_pk') 
            if course_id:
                try:
                    course = Course.objects.get(pk=course_id)
                   
                    return course.instructor == user
                except Course.DoesNotExist:
                    return False
            return True 
      
        if role == 'student':
            return request.method in permissions.SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        role = getattr(user, 'role', None)

        if user.is_staff or role == 'admin':
            return True

        if role == 'teacher':
            return obj.course.instructor == user

        if role == 'student' and request.method in permissions.SAFE_METHODS:
            return obj.course.enrollments.filter(student=user, is_active=True).exists()

        return False
         
 
class IsMaterialManagerorStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if  not request.user.is_authenticated:
            return False
        
        user = request.user
        role = getattr (user,'role',None)
        
        if user.is_staff or role == 'admin':
            
            return True
        if role == 'teacher':
            course_id = view.kwargs.get('course_pk') 
            if course_id:
                try:
                    course = Course.objects.get(pk=course_id)
                   
                    return course.instructor == user
                except Course.DoesNotExist:
                    return False
            return True 
        
        
        if role == "student":
            return request.method in permissions.SAFE_METHODS
        
        return False
    
    
    def has_object_permission(self, request, view, obj):
        user=request.user
        role=getattr(user,'role',None)
        if user.is_staff or role == 'admin':
            return True
        
        if role == "teacher":
            return obj.course.instructor == user
        if role == "student" and request.method in permissions.SAFE_METHODS:
            return object.course.enrollments.filter(student=user,is_active=True).extsts()       
            
         
        return False
    



  

     
      
