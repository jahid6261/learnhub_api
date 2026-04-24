from django.db import models
from users.models import User
# Create your models here.


class Category(models.Model):
    title=models.CharField(max_length=100,unique=True)
    description=models.TextField()
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
        
    
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    price = models.FloatField()
    duration = models.FloatField(help_text="Duration in minutes")

    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='course')

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class CourseImage(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='images')  
    image=models.ImageField(upload_to='courses/')  
    

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to='lessons_video/')
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    

  

  
  
class Material(models.Model):
    FILE_TYPES = (
        ('pdf', 'PDF'),
        ('doc', 'DOC'),
        ('ppt', 'PPT'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='materials'
    )

    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file = models.FileField(upload_to='materials/')

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    price = models.FloatField()
    progress = models.IntegerField(default=0)
    

    is_completed = models.BooleanField(default=False)
    total_mark = models.FloatField(default=0)
    is_certificate_ready = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'course']
        
        
    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

 

 

   