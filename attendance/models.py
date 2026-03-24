from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('4th Year', '4th Year'),
    ]
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, null=True, blank=True)
    # Storing face encoding as a JSON string for SQLite compatibility
    face_encoding = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')  # One attendance per day

    def __str__(self):
        return f"{self.student.name} - {self.date}"
