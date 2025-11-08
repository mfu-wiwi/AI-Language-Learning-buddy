                                        """
Quick setup script to create a demo user for testing
Run this with: python setup_demo.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'language_learning_platform.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

# Create demo user
username = 'demo'
password = 'demo1234'
email = 'demo@example.com'

if User.objects.filter(username=username).exists():
    print(f"✓ Demo user '{username}' already exists!")
else:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    print(f"✓ Demo user created successfully!")
    print(f"  Username: {username}")
    print(f"  Password: {password}")
    print(f"  Email: {email}")

# Create admin user
admin_username = 'admin'
admin_password = 'admin1234'
admin_email = 'admin@example.com'

if User.objects.filter(username=admin_username).exists():
    print(f"✓ Admin user '{admin_username}' already exists!")
else:
    admin = User.objects.create_superuser(
        username=admin_username,
        email=admin_email,
        password=admin_password
    )
    print(f"✓ Admin user created successfully!")
    print(f"  Username: {admin_username}")
    print(f"  Password: {admin_password}")
    print(f"  Email: {admin_email}")

print("\n" + "="*50)
print("Setup complete! You can now:")
print("1. Login as demo user: demo / demo1234")
print("2. Login as admin: admin / admin1234")
print("3. Access admin panel: http://127.0.0.1:8000/admin/")
print("="*50)
