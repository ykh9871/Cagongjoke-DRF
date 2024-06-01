from django.urls import path
from .views import (
    SignupAPIView,
    AuthAPIView,
    WithdrawalViewAPIView,
    ChangePasswordAPIView,
    UpdateUserAPIView,
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
    # delete - 회원탈퇴
    path("withdrawal/", WithdrawalViewAPIView.as_view(), name="withdrawal"),
    # post - 비밀번호 변경
    path("changePassword/", ChangePasswordAPIView.as_view(), name="changePassword"),
    # patch - 회원정보 변경
    path("updateUser/", UpdateUserAPIView.as_view(), name="updateUser"),
    # jwt 토큰 재발급
    path("auth/refresh/", TokenRefreshView.as_view(), name="reissueToken"),
    # 구글 소셜로그인
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
]
