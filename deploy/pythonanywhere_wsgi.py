# ─────────────────────────────────────────────────────────────
# Focacceria — PythonAnywhere WSGI configuration
# Paste this into the WSGI file linked from the PA "Web" tab
# (e.g. /var/www/YOURUSER_pythonanywhere_com_wsgi.py).
# Replace YOURUSER with your PythonAnywhere username.
# ─────────────────────────────────────────────────────────────
import os
import sys

path = '/home/YOURUSER/Focacceria'
if path not in sys.path:
    sys.path.insert(0, path)

# Production environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'focacceria.settings'
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = 'YOURUSER.pythonanywhere.com'
os.environ['CSRF_TRUSTED_ORIGINS'] = 'https://YOURUSER.pythonanywhere.com'
os.environ['SECRET_KEY'] = 'CHANGE-ME-to-a-long-random-string'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
