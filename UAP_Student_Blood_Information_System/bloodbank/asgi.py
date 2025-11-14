import os
from django.core.asgi import get_asgi_application

# Set the settings module to the one in the bloodbank folder
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UAP_Student_Blood_Information_System.bloodbank.settings')

application = get_asgi_application()
