
import os

command = 'echo from core.models import User; User.objects.create_superuser("admin", "admin@example.com", "pass") | py manage.py shell'
os.system(command)