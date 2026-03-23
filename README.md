# Face Recognition Attendance System

A comprehensive web application built with Django, OpenCV, and the `face_recognition` library. It allows you to register users via webcam, perform real-time facial recognition to log their attendance, review history on a dashboard, and export the logs to CSV.

## Features
- **Modern UI**: Clean and aesthetically pleasing responsive design.
- **Webcam Registration**: Use your browser to capture face encodings and save them to the database.
- **Real-time Recognition**: Continuous facial scanning with automatic attendance logging.
- **Dashboard & History**: View daily statistics and an interactive table of all attendance records.
- **CSV Export**: Click of a button to download attendance records.

## Project Structure
- `core/`: Django project settings and URLs.
- `attendance/`: Core application containing models, views, and utility functions.
- `templates/`: HTML templates with Vanilla CSS and specialized JavaScript.
- `db.sqlite3`: The local SQLite database where data is stored.

## Setup Instructions

### Prerequisites
- Python 3.9+
- A working webcam

*(Note: The `face_recognition` and `dlib` libraries require C++ build tools on Windows. If you run into build errors during installation, ensure you have Visual Studio Build Tools installed with the "Desktop development with C++" workload).*

### 1. Open Terminal and Navigate to the Project
```bash
cd "c:\Users\MUHAMMAD SHAN\Desktop\TesstFace"
```

### 2. Create and Activate a Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
Initialize the SQLite database schema for our models:
```bash
python manage.py makemigrations attendance
python manage.py migrate
```

### 5. Run the Server
```bash
python manage.py runserver
```

### 6. Access the Application
Open your browser and navigate to:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage Steps
1. **Register a User**: Go to "Register User", allow camera permissions, enter a name, and capture the face.
2. **Mark Attendance**: Go to "Mark Attendance", hit "Start Scanning", and look into the camera to log the attendance for the day.
3. **View History**: Look at your Dashboard or the Records page to see the saved logs, and click "Download CSV" to export them.
