

import os
import globals

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', F'{globals.PROJECT_NAME}.settings')

application = get_wsgi_application()
