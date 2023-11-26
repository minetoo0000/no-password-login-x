"""
WSGI config for no_password_login project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'no_password_login.settings')

application = get_wsgi_application()


# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "no_password_login.settings")
# django.setup()

from django.utils import timezone as tm;
from system.func import setInterval;
from system import models;


def deleteAutoLoginBridge():
  get_bridges = models.LoginBridge.objects.all();
  for bridge in get_bridges:
    ## 만료된 경우 삭제.
    if tm.now()>bridge.AT_lifetime:
      bridge.delete();
  
inter_delete_login_bridge = setInterval(10, deleteAutoLoginBridge);
