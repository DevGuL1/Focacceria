#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Focacceria — PythonAnywhere one-time setup
# Run this INSIDE a PythonAnywhere Bash console.
# Replace YOURUSER with your PythonAnywhere username before running.
# ─────────────────────────────────────────────────────────────
set -e

PA_USER="YOURUSER"
PROJECT_DIR="$HOME/Focacceria"
VENV_DIR="$HOME/.virtualenvs/focacceria"

echo "==> 1/6 Cloning repo"
if [ ! -d "$PROJECT_DIR" ]; then
  git clone https://github.com/DevGuL1/Focacceria.git "$PROJECT_DIR"
else
  cd "$PROJECT_DIR" && git pull
fi

echo "==> 2/6 Creating virtualenv (Python 3.10)"
if [ ! -d "$VENV_DIR" ]; then
  python3.10 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

echo "==> 3/6 Installing dependencies"
cd "$PROJECT_DIR"
pip install --upgrade pip
pip install -r requirements.txt

echo "==> 4/6 Migrating + seeding database"
python manage.py migrate --no-input
python manage.py seed_data || true

echo "==> 5/6 Collecting static files"
python manage.py collectstatic --no-input

echo "==> 6/6 Ensuring admin user"
python manage.py shell <<'PYEOF'
import os
from django.contrib.auth import get_user_model
U = get_user_model()
if not U.objects.filter(username='admin').exists():
    U.objects.create_superuser('admin', 'admin@focacceria.ge', 'focacceria2024')
    print('Created admin / focacceria2024')
else:
    print('admin already exists')
PYEOF

echo ""
echo "✅ Setup complete!"
echo "Project:  $PROJECT_DIR"
echo "Virtualenv: $VENV_DIR"
echo ""
echo "Next: configure the Web tab (see DEPLOY_PYTHONANYWHERE.md)."
