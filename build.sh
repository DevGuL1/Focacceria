#!/usr/bin/env bash
# Render build script for Focacceria
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Seed initial data only if the DB is empty (idempotent)
python manage.py seed_data || true

# Create the admin user from env vars if it does not exist yet
python manage.py shell <<'PYEOF'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@focacceria.ge')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'focacceria2024')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Created superuser: {username}')
else:
    print(f'Superuser {username} already exists')
PYEOF
