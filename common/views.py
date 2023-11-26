from django.http import HttpResponse;
from django.shortcuts import render, redirect;
from django.contrib.auth import login, authenticate, logout;
from django.contrib.auth.models import User;
from system import models;
from . import forms;
import io;
import base64;
import qrcode;
import qrcode.image.svg;

# DOMAIN = "192.168.174.79:8000";
DOMAIN = "192.168.1.12:80";


def prev_page():
  return( HttpResponse("<script>window.history.back();</script>") );


# Create your views here.
def regist_account( req )->None:
  if req.method=="GET":
    new_form = forms.RegistForm();
    data = { "form":new_form };
    return( render(req, "regist.html", data) );

  elif req.method=="POST":
    get_form = forms.RegistForm(req.POST);
    if get_form.is_valid()==False:
      data = {
        "error":"이미 존재하는 계정 아이디이거나 입력하지 않았습니다.",
      };
      return( render(req, "error.html", data) );

    ## Account 생성 및 저장.
    new_acc = models.Account();
    new_acc.DP_account_id = get_form.cleaned_data.get("DP_account_id");
    new_acc.save();

    ## Device 생성 및 저장.
    new_dev = models.Device();
    #? 최상위 권한.
    new_dev.permission_level = 0;
    new_dev.account = new_acc;
    new_dev.save();

    ## Client(User과 Device를 연결시켜줌) 생성 및 저장.
    new_client = User();
    new_client.username = new_dev.DP_AT_device_id;
    new_client.set_password(new_dev.AT_login_token);
    new_client.save();

    ## 생성된 계정으로(Device) 로그인하기.
    login_client = authenticate(
      username=new_dev.DP_AT_device_id,
      password=new_dev.AT_login_token,
    );
    login(req, login_client);

    return( redirect("home") );
  
  else:
    return( redirect("home") );

def logout_to_client_device_delete( req ):
  if req.user.is_authenticated==False:
    return( redirect("home") );

  ## Client 및 Device 삭제.
  get_dev = models.Device.objects.get(DP_AT_device_id=req.user.username);
  get_dev.delete();
  req.user.delete();

  return( redirect("client_break") );


def login_allow( req, login_req_id:str, login_account_id:str ):
  decode_login_req_id = base64.urlsafe_b64decode(login_req_id).decode("UTF-8");

  if req.method=="GET":
    get_bridge = models.LoginBridge.objects.get(
      DP_AT_login_req_id=decode_login_req_id,
      DP_login_account_id=login_account_id,
    );
    get_dev = models.Device.objects.get(DP_AT_device_id=req.user.username);

    ## 존재하는 요청인지 검사.
    if not get_bridge or not get_dev:
      data = {
        "error":"만료된 요청입니다.",
      };
      return( render(req, "error.html", data) );
  
    ## 이미 허용된 브릿지인지 확인.
    if get_bridge.NA_allow_device!=None:
      data = {
        "error":"만료된 요청입니다.",
      };
      return( render(req, "error.html", data) );

    ## 동일한 사용자인지 확인.
    if req.user.is_authenticated==False:
      data = {
        "error":"요청이 유효하지 않습니다.",
      };
      return( render(req, "error.html", data) );
    
    if login_account_id!=get_dev.account.DP_account_id:
      data = {
        "error":"요청이 유효하지 않습니다.",
      };
      return( render(req, "error.html", data) );

    ## 동일 사용자임이 확인됨.
    ## 로그인 허용 업데이트.
    get_bridge.NA_allow_device = get_dev;
    get_bridge.save();

    return( render(req, "login_allow.html") );
  
  else:
    data = {
      "error":"잘못된 요청입니다.",
    };
    return( render(req, "error", data) );


def login_bridge( req, login_account_id:str, login_req_id:str ):
  ## login_account_id 디코딩 하기.
  decode_login_req_id = base64.urlsafe_b64decode(login_req_id).decode("UTF-8");
  
  if req.method=="GET":
    ## LoginBridge 에서 객체 찾기.
    try:
      get_bridge = models.LoginBridge.objects.get(
        DP_AT_login_req_id=decode_login_req_id,
        DP_login_account_id=login_account_id,
      );
    except:
      return( prev_page() );

    ## 로그인 허용 여부 검사:로그인 안됨.
    if get_bridge.NA_allow_device==None:
      img = qrcode.make(
        f"http://{ DOMAIN }/account/login-allow/{ login_req_id }/{ login_account_id }",
        image_factory=qrcode.image.svg.SvgImage,
        box_size=18,
      );
      buf = io.BytesIO();
      img.save(buf);
      data = {
        "qr_img_base64":base64.b64encode(buf.getvalue()).decode("UTF-8"),
        "login_req_id":decode_login_req_id,
        "encoded_login_req_id":login_req_id,
      };
      return( render(req, "login_bridge.html", data) );

    ## 로그인 허용 됨.
    else:
      ## 로그인을 허용시킨 기기의 하위 권한으로 Device 생성 및 저장.
      new_dev = models.Device();
      new_dev.permission_level = get_bridge.NA_allow_device.permission_level+1;
      new_dev.account = get_bridge.NA_allow_device.account;
      new_dev.save();

      ## 로그인 시킬 Client(User) 생성 및 저장.
      new_client = User();
      new_client.username = new_dev.DP_AT_device_id;
      new_client.set_password(new_dev.AT_login_token);
      new_client.save();

      ## 생성된 Client로 기기 로그인 하기.
      login_client = authenticate(
        username=new_dev.DP_AT_device_id,
        password=new_dev.AT_login_token,
      );
      login(req, login_client);
            
      return( redirect("home") );


def login_account( req ):
  if req.method=="GET":
    new_form = forms.LoginForm();
    data = { "form":new_form };
    return( render(req, "login.html", data) );

  elif req.method=="POST":
    get_form = forms.LoginForm(req.POST);
    if get_form.is_valid()==False:
      return( redirect("login") );
    
    ## LoginBridge 생성 및 저장.
    new_bridge = models.LoginBridge();
    new_bridge.DP_login_account_id = get_form.cleaned_data.get("account_id");
    new_bridge.save();

    ## 로그인 요청 받는 페이지로 이동.
    encode_login_req_id = base64.urlsafe_b64encode(
      new_bridge.DP_AT_login_req_id.encode("UTF-8")
    ).decode("ascii");
    return(
      redirect(
        "login_bridge",
        login_req_id=encode_login_req_id,
        login_account_id=new_bridge.DP_login_account_id,
      )
    );
  else:
    return( redirect("login") );


def account_control( req ):
  if req.method=="GET":
    ## device_id로 Account 객체 가져오기.
    get_dev = models.Device.objects.get(DP_AT_device_id=req.user.username);
    get_acc = get_dev.account;

    ## Account와 연결된 다른 Device 목록 전부 가져오기.
    _get_devs = models.Device.objects.filter(account=get_acc);

    ## 현재 Device보다 권한이 낮은 Device만 가져오기.
    get_devs = [];
    for dev in _get_devs:
      if dev.permission_level>get_dev.permission_level:
        get_devs.append(dev);
    
    ## 렌더링.
    data = {
      "device_list":get_devs,
    };
    return( render(req, "account_control.html", data) );
