from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from apps.cagong.models import Area, Cafe, Review, CafeLike, ReviewLike
from apps.cagong.serializers import (
    AreaSerializer,
    CafeSerializer,
    ReviewSerializer,
    CafeLikeSerializer,
    ReviewLikeSerializer,
)
