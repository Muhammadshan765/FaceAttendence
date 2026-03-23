import os

files_to_update = [
    'attendance/views.py',
    'templates/attendance/register.html',
    'templates/attendance/dashboard.html',
    'templates/attendance/history.html'
]

for file_path in files_to_update:
    full_path = os.path.join(r'C:\Users\MUHAMMAD SHAN\Desktop\TesstFace', file_path)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('Employee', 'Student').replace('employee', 'student')
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_path}")
    else:
        print(f"File not found: {file_path}")
