from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models, forms;

# Register your models here.
admin.site.register(models.Account);
admin.site.register(models.Device);
admin.site.register(models.LoginBridge);