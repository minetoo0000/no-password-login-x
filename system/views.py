from django.shortcuts import render
from . import models;

# Create your views here.
def home( req ):
  data = {};
  if req.user.is_authenticated==True:
    get_dev = models.Device.objects.get(DP_AT_device_id=req.user.username);
    get_acc = get_dev.account;
    data = {
      "account_id":get_acc.DP_account_id,
      "device_id":req.user.username,
    };
  return( render(req, "home.html", data) );