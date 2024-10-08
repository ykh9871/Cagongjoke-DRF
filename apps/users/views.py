import datetime
import jwt
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from config.settings import (
    SECRET_KEY,
    SOCIAL_AUTH_GOOGLE_CLIENT_ID,
    SOCIAL_AUTH_GOOGLE_SECRET,
)
from django.shortcuts import redirect

from apps.users.serializers import *
from apps.users.models import *

from json import JSONDecodeError
from django.http import JsonResponse
import requests
import os
from rest_framework import status
from django.contrib.auth.hashers import make_password
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp


state = os.environ.get("STATE")
BASE_URL = "http://localhost:8000/"
GOOGLE_CALLBACK_URI = BASE_URL + "api/user/google/callback/"


def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
    client_id = SOCIAL_AUTH_GOOGLE_CLIENT_ID
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )


def google_callback(request):
    client_id = SOCIAL_AUTH_GOOGLE_CLIENT_ID
    client_secret = SOCIAL_AUTH_GOOGLE_SECRET
    code = request.GET.get("code")
    state = request.GET.get("state")  # state가 없으면 None을 반환

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_CALLBACK_URI,
            "state": state,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)

    google_access_token = token_req_json.get("access_token")
    google_refresh_token = token_req_json.get("refresh_token")
    expires_in = token_req_json.get("expires_in")
    expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)

    # 사용자 정보 요청
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={"access_token": google_access_token},
    )
    user_info = user_info_response.json()

    email = user_info.get("email")

    def create_response(user, message):
        serializer = UserSerializer(user)
        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)
        refresh_token = str(token)

        user.last_login = timezone.now()
        user.save()

        response = JsonResponse(
            {
                "user": serializer.data,
                "message": message,
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )

        # Access 토큰 쿠키 설정
        response.set_cookie("access_token", access_token, httponly=True)
        # Refresh 토큰 쿠키 설정
        response.set_cookie("refresh_token", refresh_token, httponly=True)

        return response

    try:
        user = User.objects.get(email=email)
        if user.is_active:
            # 소셜 계정 연결 여부 확인
            if not SocialAccount.objects.filter(user=user, provider="google").exists():
                # 소셜 계정이 연결되어 있지 않으면 연결 절차 진행
                # 여기서 추가 인증을 요구할 수도 있음 (예: 비밀번호 확인)
                return JsonResponse(
                    {"message": "계정에 소셜 로그인을 연결하시겠습니까?"}
                )
            # 이미 소셜 계정이 연결되어 있으면 바로 로그인 처리
            return create_response(user, "login success")
        else:
            raise Exception("Signup Required")
    except User.DoesNotExist:
        # 신규 사용자 등록 및 소셜 계정, 토큰 저장
        username = user_info.get("name")
        user = User.objects.create(email=email, username=username)
        user.set_unusable_password()  # 비밀번호 없이 로그인할 것이므로 설정 불가로 처리
        user.is_social = True
        user.save()

        social_account = SocialAccount.objects.create(
            user=user,
            provider="google",
            uid=user_info.get("id"),
            extra_data=user_info,  # 추가된 사용자 정보 저장
        )

        social_app = SocialApp.objects.get(provider="google")

        SocialToken.objects.create(
            account=social_account,
            token=google_access_token,
            token_secret=google_refresh_token if google_refresh_token else "",
            expires_at=expires_at,
            app=social_app,
        )

        # 회원가입 후 로그인 처리
        return create_response(user, "login success")
    except Exception as e:
        return JsonResponse(
            {"status": 400, "message": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SignupAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="회원가입",
        operation_description="새 사용자를 등록합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="사용자 이름"
                ),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호"
                ),
                "password_confirm": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호 확인"
                ),
            },
            required=["username", "email", "password", "password_confirm"],
        ),
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {"message": "User registered successfully"}
                },
            ),
            400: openapi.Response(
                description="Invalid input",
                examples={
                    "application/json": {
                        "errors": {
                            "email": ["A user with this email already exists."],
                            "password": ["Passwords do not match."],
                        }
                    }
                },
            ),
        },
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        # 에러 메시지를 포맷하여 반환
        error_messages = serializer.errors
        return Response({"errors": error_messages}, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):
    # 유저 정보 확인
    @swagger_auto_schema(
        operation_summary="사용자 정보 가져오기",
        operation_description="쿠키에서 액세스 토큰을 사용하여 사용자 정보를 가져옵니다.",
        responses={
            200: openapi.Response(
                description="User information retrieved successfully",
                schema=UserSerializer,
            ),
            400: openapi.Response(description="Invalid token"),
            401: openapi.Response(description="Unauthorized"),
        },
    )
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES["access"]
            payload = jwt.decode(access, SECRET_KEY, algorithms=["HS256"])
            pk = payload.get("user_id")
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError:
            # 토큰 만료 시 토큰 갱신
            data = {"refresh": request.COOKIES.get("refresh", None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get("access", None)
                refresh = serializer.data.get("refresh", None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=["HS256"])
                pk = payload.get("user_id")
                user = get_object_or_404(User, pk=pk)
                serializer = UserSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie("access", access)
                res.set_cookie("refresh", refresh)
                return res
            raise jwt.exceptions.InvalidTokenError

        except jwt.exceptions.InvalidTokenError:
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    @swagger_auto_schema(
        operation_summary="로그인",
        operation_description="사용자를 인증하고 JWT 토큰을 반환합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호"
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            # ...
                        },
                        "message": "login success",
                        "token": {
                            "access": "access_token_example",
                            "refresh": "refresh_token_example",
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="Incorrect email or password",
                examples={
                    "application/json": {
                        "detail": "Incorrect email or password",
                    }
                },
            ),
            403: openapi.Response(
                description="Inactive account",
                examples={
                    "application/json": {
                        "detail": "This account is inactive. Would you like to restore it?",
                        "restore": True,
                    }
                },
            ),
        },
    )
    def post(self, request):
        # 유저 인증
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            if not user.is_active:
                return Response(
                    {
                        "detail": "This account is inactive. Would you like to restore it?",
                        "restore": True,
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            user.last_login = timezone.now()
            user.save()
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(
                {"detail": "Incorrect email or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    # 로그아웃
    @swagger_auto_schema(
        operation_summary="로그아웃",
        operation_description="쿠키에서 JWT 토큰을 삭제하여 사용자를 로그아웃합니다.",
        responses={
            202: openapi.Response(description="Logout successful"),
        },
    )
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response(
            {"message": "Logout success"}, status=status.HTTP_202_ACCEPTED
        )
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


class WithdrawalViewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="회원 탈퇴",
        operation_description="사용자의 비밀번호를 확인한 후 회원 탈퇴를 수행합니다.",
        request_body=WithdrawalSerializer,
        responses={
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized - Incorrect password",
        },
    )
    def delete(self, request):
        user = request.user
        serializer = WithdrawalSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("password")):
                return Response(
                    {"password": ["Incorrect password."]},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="비밀번호 변경",
        operation_description="사용자의 비밀번호를 변경합니다.",
        request_body=ChangePasswordSerializer,
        responses={
            200: "Password updated successfully",
            400: "Bad Request",
        },
    )
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("current_password")):
                return Response(
                    {"current_password": ["Current password is incorrect."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.password = make_password(serializer.data.get("new_password"))
            user.save()

            return Response(
                {"message": "Password updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="회원 정보 변경",
        operation_description="사용자의 정보를 변경합니다.",
        request_body=UpdateUserSerializer,
        responses={
            200: "User information updated successfully",
            400: "Bad Request",
        },
    )
    def patch(self, request):
        user = request.user
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RestoreAccountAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="계정 복구",
        operation_description="비활성화된 계정을 복구합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
            },
            required=["email"],
        ),
        responses={
            200: openapi.Response(
                description="Account restored successfully",
                examples={
                    "application/json": {
                        "detail": "Account restored successfully.",
                    }
                },
            ),
            400: openapi.Response(
                description="Account is already active",
                examples={
                    "application/json": {
                        "detail": "Account is already active.",
                    }
                },
            ),
            404: openapi.Response(
                description="Account not found",
                examples={
                    "application/json": {
                        "detail": "Account not found.",
                    }
                },
            ),
        },
    )
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response(
                    {"detail": "Account is already active."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.restore()
            return Response(
                {"detail": "Account restored successfully."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "Account not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
