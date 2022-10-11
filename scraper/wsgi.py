"""
WSGI config for scraper project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

# project_folder = os.path.expanduser('C:\Users\prava\OneDrive\Desktop\Project')  # adjust as appropriate
# print('\n\n\n\n\n\n')
# print(project_folder)
a = load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
print(SECRET_KEY)
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper.settings')

application = get_wsgi_application()
