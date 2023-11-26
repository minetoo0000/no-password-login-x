from django.urls import path;
from django.contrib.auth import views as auth_views;
from . import views;

urlpatterns = [
  path("regist/", views.regist_account, name="regist"),
  path("logout/", auth_views.LogoutView.as_view(), name="logout"),
  path("login/", views.login_account, name="login"),
  path("login-bridge/<str:login_req_id>/<str:login_account_id>", views.login_bridge, name="login_bridge"),
  path("login-allow/<str:login_req_id>/<str:login_account_id>", views.login_allow, name="login_allow"),
];