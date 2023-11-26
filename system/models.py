from django.contrib.auth.models import User;
from django.db import models
from . import func;

class Account( models.Model ):
  DP_account_id = models.CharField(max_length=64, unique=True, null=False, blank=False);
  AT_account_password = models.CharField(
    max_length=128, null=False, blank=True,
    default=func.token,
  );

class Device( models.Model ):
  DP_AT_device_id = models.CharField(
    max_length=128, unique=True, null=False,
    default=func.id
  );
  AT_login_token = models.CharField(
    max_length=128, null=False,
    default=func.token,
  );
  permission_level = models.IntegerField();
  account = models.ForeignKey(Account, null=False, on_delete=models.CASCADE);

class LoginBridge( models.Model ):
  DP_AT_login_req_id = models.CharField(
    max_length=128, null=False,
    default=func.token,
  );
  DP_login_account_id = models.CharField(max_length=64, null=False);
  AT_lifetime = models.DateTimeField(null=False, default=func.lifetime);
  NA_allow_device = models.ForeignKey(Device, null=True, default=None, on_delete=models.CASCADE);
