import os
import shutil
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'focacceria.settings')

BASE_DIR = Path(__file__).resolve().parent.parent
BUNDLED_DB = BASE_DIR / 'Focacceria_project_v1.db'
RUNTIME_DB = Path('/tmp/Focacceria_project_v1.db')

if BUNDLED_DB.exists() and not RUNTIME_DB.exists():
    shutil.copy2(BUNDLED_DB, RUNTIME_DB)

from django.core.management import call_command

call_command('migrate', verbosity=0, interactive=False)

from focacceria.wsgi import application

app = application
