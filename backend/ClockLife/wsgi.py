import os, socketio
from django.core.wsgi import get_wsgi_application
from ClockLife.socket import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ClockLife.settings")

application = get_wsgi_application()
application = socketio.WSGIApp(sio, application)
