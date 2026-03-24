import os
import django
import sys

# Set up Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

# Create admin if it doesn't exist, or update password if it does
user = User.objects.filter(username='admin').first()
if not user:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("SUCCESS: Default 'admin' user created with password 'admin'.")
else:
    user.set_password('admin')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("SUCCESS: 'admin' user password reset to 'admin'.")
