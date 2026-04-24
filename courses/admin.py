from django.contrib import admin
from courses.models import Category,Course,Enrollment,Material,Lesson,CourseImage
# Register your models here.


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Material)
admin.site.register(Enrollment)
