from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    department = models.CharField(max_length=100)   
    admission_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.IntegerField()
    is_active = models.BooleanField(default=True)
    instructor = models.ForeignKey('Instructor', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.code}: {self.name}"

class Enrollment(models.Model):
    class Status(models.TextChoices):
        ENROLLED = 'EN', 'Enrolled'
        COMPLETED = 'CO', 'Completed'
        DROPPED = 'DR', 'Dropped'
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ENROLLED)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'], 
                name='unique_myapp_student_course_enrollment')
        ]   

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.name}"

class Instructor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name