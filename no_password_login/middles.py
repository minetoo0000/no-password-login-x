from django.shortcuts import render, redirect;
from django.contrib.auth import logout;
from system import models;

class AuthErrorMiddle():
  def __init__( self, get_response ):
    self.get_response = get_response;

  def __call__( self, request ):
    try:
      if request.path.startswith("/admin"):
        pass;
      elif request.path.startswith("/account/client-break"):
        pass;
      elif request.user.is_authenticated:
        get_dev = models.Device.objects.get(DP_AT_device_id=request.user.username);
        get_acc = get_dev.account;
    except:
      if request.user.username!="admin":
        request.user.delete();
      return( redirect("client_break") );

    return( self.get_response(request) );
