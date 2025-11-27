"""
WSGI config for pawshome project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pawshome.settings')

application = get_wsgi_application()
