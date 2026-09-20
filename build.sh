#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Create test user for reviewers (idempotent - won't fail if user already exists)
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model

User = get_user_model()
username = "user"
password = "user12345"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email="user@example.com")
    print(f"Created test user: {username}")
else:
    print(f"Test user {username} already exists, skipping")
EOF