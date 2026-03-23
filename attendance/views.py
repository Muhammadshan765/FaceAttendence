import csv
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

from .models import Student, Attendance
from .utils import get_face_encoding, match_face, encoding_to_string, string_to_encoding

def dashboard(request):
    recent_attendance = Attendance.objects.select_related('student').order_by('-date', '-time')[:10]
    context = {
        'recent_attendance': recent_attendance,
        'total_students': Student.objects.count(),
        'today_attendance': Attendance.objects.filter(date=datetime.now().date()).count()
    }
    return render(request, 'attendance/dashboard.html', context)

def register(request):
    return render(request, 'attendance/register.html')

def recognize(request):
    return render(request, 'attendance/recognize.html')

def history(request):
    attendance_records = Attendance.objects.select_related('student').order_by('-date', '-time')
    return render(request, 'attendance/history.html', {'records': attendance_records})

@csrf_exempt
def register_face(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            image_b64 = data.get('image')

            if not name or not image_b64:
                return JsonResponse({'status': 'error', 'message': 'Name and image are required'})

            encoding, error = get_face_encoding(image_b64)
            if error:
                return JsonResponse({'status': 'error', 'message': error})

            # Check if user already exists
            if Student.objects.filter(name=name).exists():
                return JsonResponse({'status': 'error', 'message': 'Student with this name already exists'})

            # Check if face already exists
            students = list(Student.objects.all())
            if students:
                known_encodings = [string_to_encoding(emp.face_encoding) for emp in students]
                match_idx = match_face(encoding, known_encodings)
                if match_idx is not None:
                    matched_student = students[match_idx]
                    return JsonResponse({'status': 'error', 'message': f'Face already registered to {matched_student.name}'})

            # Save to DB
            encoding_str = encoding_to_string(encoding)
            Student.objects.create(name=name, face_encoding=encoding_str)

            return JsonResponse({'status': 'success', 'message': f'Successfully registered {name}'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def recognize_face(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_b64 = data.get('image')

            if not image_b64:
                return JsonResponse({'status': 'error', 'message': 'Image is required'})

            unknown_encoding, error = get_face_encoding(image_b64)
            if error:
                return JsonResponse({'status': 'error', 'message': error})

            # Get all known encodings
            students = list(Student.objects.all())
            if not students:
                return JsonResponse({'status': 'error', 'message': 'No registered students found'})

            known_encodings = [string_to_encoding(emp.face_encoding) for emp in students]
            
            # Match
            match_idx = match_face(unknown_encoding, known_encodings)
            
            if match_idx is not None:
                matched_student = students[match_idx]
                
                # Mark attendance
                today = datetime.now().date()
                if Attendance.objects.filter(student=matched_student, date=today).exists():
                    return JsonResponse({
                        'status': 'warning', 
                        'message': f'Attendance already marked for {matched_student.name} today',
                        'name': matched_student.name
                    })
                
                Attendance.objects.create(student=matched_student)
                return JsonResponse({
                    'status': 'success', 
                    'message': f'Attendance marked for {matched_student.name}',
                    'name': matched_student.name
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Unknown person'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_records.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Date', 'Time'])

    attendance_records = Attendance.objects.select_related('student').order_by('-date', '-time')
    for record in attendance_records:
        writer.writerow([record.student.name, record.date, record.time])

    return response
