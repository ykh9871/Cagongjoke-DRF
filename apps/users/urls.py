from django.urls import path
from .views import (
    SignupAPIView,
    AuthAPIView,
    google_login,
    google_callback,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    # post - 회원가입
    path("signup/", SignupAPIView.as_view(), name="signup"),
    # post - 로그인, get - 회원 정보, delete - 로그아웃
    path("auth/", AuthAPIView.as_view()),
    # jwt 토큰 재발급
    path("auth/refresh/", TokenRefreshView.as_view()),
    # 구글 소셜로그인
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
]
