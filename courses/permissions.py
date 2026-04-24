from rest_framework import permissions

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

