from rest_framework import serializers
from courses.models import Category,Course,CourseImage,Enrollment,Lesson,Material



class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title','description']
        
class CourseSerializers(serializers.ModelSerializer):
    class Meta :
        model=Course
        fields=['id','title','category','description','price','duration','instructor','is_active','created_at','updated_at']        

class IamgeSerializers(serializers.ModelSerializer):
    class Meta :
        model=CourseImage
        fields=['id','course','images']

class LessonSerializers(serializers.ModelSerializer):
    class Meta :
        model=Lesson
        fields=['id','title','course','description','video','is_active','created_at','updated_at']
    

class MaterialSerializers(serializers.ModelSerializer):
    class Meta :
        model=Material
        fields=['id','title','course','description','file','file_type','created_at','updated_at','is_active']

class EnrollmentSerializers(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.email')
    course_title = serializers.ReadOnlyField(source='course.title')
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['student', 'price','progress', 'is_completed',
                             'is_certificate_ready','total_mark','is_active']