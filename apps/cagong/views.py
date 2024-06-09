from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from apps.users.models import User
from apps.cagong.models import Area, Cafe, Review, CafeLike, ReviewLike
from apps.cagong.serializers import (
    AreaSerializer,
    CafeSerializer,
    ReviewSerializer,
    CafeLikeSerializer,
    ReviewLikeSerializer,
)


# Area 관련 API
class CityListAPIView(APIView):
    def get(self, request):
        areas = (
            Area.objects.values("city_name", "city_code")
            .distinct()
            .order_by("city_code")
        )
        return Response(areas)


class CountyListAPIView(APIView):
    def get(self, request, city_code):
        counties = (
            Area.objects.filter(city_code=city_code)
            .values("county_code", "county_name")
            .distinct()
            .order_by("county_code")
        )
        return Response(counties)


class TownListAPIView(APIView):
    def get(self, request, county_code):
        towns = (
            Area.objects.filter(county_code=county_code)
            .values("town_code", "town_name")
            .distinct()
            .order_by("town_code")
        )
        return Response(towns)


class AreaCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AreaUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        area = Area.objects.get(pk=pk)
        serializer = AreaSerializer(area, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AreaDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        area = Area.objects.get(pk=pk)
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Cafe 관련 API
class CafeListAPIView(APIView):
    def get(self, request):
        area_id = request.query_params.get("area_id", None)

        if area_id:
            cafes = Cafe.objects.filter(area__id__startswith=area_id).order_by(
                "-cagong"
            )
        else:
            cafes = Cafe.objects.all().order_by("-cagong")

        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 항목 수를 10으로 설정
        result_page = paginator.paginate_queryset(cafes, request)

        serializer = CafeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CafeDetailAPIView(APIView):
    def get(self, request, pk):
        cafe = Cafe.objects.get(pk=pk)
        serializer = CafeSerializer(cafe)
        return Response(serializer.data)


class CafeCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CafeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CafeUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        cafe = Cafe.objects.get(pk=pk)
        serializer = CafeSerializer(cafe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CafeDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        cafe = Cafe.objects.get(pk=pk)
        cafe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CafeLikeCountAPIView(APIView):
    def get(self, request, pk):
        try:
            cafe = Cafe.objects.get(pk=pk)
            count = cafe.likes.count()
            return Response({"count": count})
        except Cafe.DoesNotExist:
            return Response({"error": "Cafe not found"}, status=404)


class CafeReviewCountAPIView(APIView):
    def get(self, request, pk):
        try:
            cafe = Cafe.objects.get(pk=pk)
            count = cafe.reviews.count()
            return Response({"count": count})
        except Cafe.DoesNotExist:
            return Response({"error": "Cafe not found"}, status=404)


class CafeReviewListAPIView(APIView):
    def get(self, request, pk):
        try:
            cafe = Cafe.objects.get(pk=pk)
        except Cafe.DoesNotExist:
            return Response({"error": "Cafe not found"}, status=404)

        reviews = cafe.reviews.all().order_by("-created_at")

        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 항목 수를 설정합니다.
        result_page = paginator.paginate_queryset(reviews, request)

        serializer = ReviewSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class UserLikedCafesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cafes = user.cafe_likes.all().order_by("-updated_at")

        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 항목 수를 설정합니다.
        result_page = paginator.paginate_queryset(cafes, request)
        serializer = CafeLikeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# Review 관련 API
class UserReviewsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = request.user
        reviews = user.reviews.all().order_by("-updated_at")
        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 항목 수를 설정합니다.
        result_page = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class UserLikedReviewsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        likes = user.review_likes.all().order_by("-updated_at")
        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 항목 수를 설정합니다.
        result_page = paginator.paginate_queryset(likes, request)
        serializer = ReviewLikeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ReviewCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
