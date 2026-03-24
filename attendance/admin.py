from django.contrib import admin
from .models import Student, Attendance

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'year', 'created_at')
    search_fields = ('name', 'student_id')
    list_filter = ('year',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'time')
    list_filter = ('date', 'student__year')
    date_hierarchy = 'date'
    search_fields = ('student__name', 'student__student_id')
