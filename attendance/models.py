from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=255)
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
