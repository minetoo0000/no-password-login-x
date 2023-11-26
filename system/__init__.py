# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproj.settings")
# django.setup()

# from django.utils import timezone as tm;
# from system.func import setInterval;
# from . import models;


# def deleteAutoLoginBridge():
#   get_bridges = models.LoginBridge.objects.all();
#   for bridge in get_bridges:
#     ## 만료된 경우 삭제.
#     if tm.now()>bridge.AT_lifetime:
#       bridge.delete();
  
# inter_delete_login_bridge = setInterval(10, deleteAutoLoginBridge);
