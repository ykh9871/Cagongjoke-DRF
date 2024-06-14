from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.cagong.models import Area, Cafe, Review, CafeLike, ReviewLike
from apps.cagong.serializers import *


# Area 관련 API
class CityListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="시/도 목록 조회",
        operation_description="모든 시/도 목록을 조회합니다.",
        responses={200: openapi.Response("시/도 목록", CityListSerializer(many=True))},
    )
    def get(self, request):
        areas = (
            Area.objects.values("city_name", "city_code")
            .distinct()
            .order_by("city_code")
        )
        serializer = CityListSerializer(areas, many=True)
        return Response(serializer.data)


class CountyListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="시군구 목록 조회",
        operation_description="특정 시/도의 모든 시군구 목록을 조회합니다.",
        responses={
            200: openapi.Response("시군구 목록", CountyListSerializer(many=True))
        },
    )
    def get(self, request, city_code):
        counties = (
            Area.objects.filter(city_code=city_code)
            .values("city_code", "county_code", "county_name")
            .distinct()
            .order_by("county_code")
        )
        serializer = CountyListSerializer(counties, many=True)
        return Response(serializer.data)


class TownListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="읍면동 목록 조회",
        operation_description="특정 시군구의 모든 읍면동 목록을 조회합니다.",
        responses={200: openapi.Response("읍면동 목록", TownListSerializer(many=True))},
    )
    def get(self, request, city_code, county_code):
        towns = (
            Area.objects.filter(city_code=city_code, county_code=county_code)
            .values("id", "town_code", "town_name")
            .order_by("town_code")
        )
        serializer = TownListSerializer(towns, many=True)
        return Response(serializer.data)


class AreaCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="지역 생성",
        operation_description="새로운 지역을 생성합니다.",
        request_body=AreaSerializer,
        responses={201: AreaSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = AreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AreaUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="지역 업데이트",
        operation_description="특정 지역 정보를 업데이트합니다.",
        request_body=AreaSerializer,
        responses={200: AreaSerializer, 400: "Bad Request"},
    )
    def put(self, request, pk):
        area = Area.objects.get(pk=pk)
        serializer = AreaSerializer(area, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AreaDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="지역 삭제",
        operation_description="특정 지역 정보를 삭제합니다.",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, pk):
        area = Area.objects.get(pk=pk)
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Cafe 관련 API
class CafeListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="카페 목록 조회",
        operation_description="모든 카페 목록을 조회합니다.",
        responses={200: openapi.Response("카페 목록", CafeSerializer(many=True))},
    )
    def get(self, request):
        area_id = request.query_params.get("area_id", None)

        if area_id:
            cafes = Cafe.objects.filter(area__id=area_id).order_by("-cagong", "id")
        else:
            cafes = Cafe.objects.all().order_by("-cagong", "id")

        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 항목 수를 10으로 설정
        result_page = paginator.paginate_queryset(cafes, request)

        serializer = CafeSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CafeDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="카페 상세 조회",
        operation_description="특정 카페의 상세 정보를 조회합니다.",
        responses={200: CafeSerializer, 404: "Not Found"},
    )
    def get(self, request, pk):
        cafe = Cafe.objects.get(pk=pk)
        serializer = CafeSerializer(cafe)
        return Response(serializer.data)


class CafeCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="카페 생성",
        operation_description="새로운 카페를 생성합니다.",
        request_body=CafeSerializer,
        responses={201: CafeSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = CafeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CafeUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="카페 업데이트",
        operation_description="특정 카페 정보를 업데이트합니다.",
        request_body=CafeSerializer,
        responses={200: CafeSerializer, 400: "Bad Request"},
    )
    def patch(self, request, pk):
        cafe = Cafe.objects.get(pk=pk)
        serializer = CafeSerializer(cafe, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CafeDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="카페 삭제",
        operation_description="특정 카페 정보를 삭제합니다.",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, pk):
        cafe = Cafe.objects.get(pk=pk)
        cafe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CafeLikeCountAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="카페 좋아요 수 조회",
        operation_description="특정 카페의 좋아요 수를 조회합니다.",
        responses={
            200: openapi.Response(
                "좋아요 수",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"count": openapi.Schema(type=openapi.TYPE_INTEGER)},
                ),
            ),
            404: "Not Found",
        },
    )
    def get(self, request, pk):
        try:
            cafe = Cafe.objects.get(pk=pk)
            count = cafe.likes.count()
            return Response({"count": count})
        except Cafe.DoesNotExist:
            return Response({"error": "Cafe not found"}, status=404)


class CafeReviewCountAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="카페 리뷰 수 조회",
        operation_description="특정 카페의 리뷰 수를 조회합니다.",
        responses={
            200: openapi.Response(
                "리뷰 수",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"count": openapi.Schema(type=openapi.TYPE_INTEGER)},
                ),
            ),
            404: "Not Found",
        },
    )
    def get(self, request, pk):
        try:
            cafe = Cafe.objects.get(pk=pk)
            count = cafe.reviews.count()
            return Response({"count": count})
        except Cafe.DoesNotExist:
            return Response({"error": "Cafe not found"}, status=404)


class CafeReviewListAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="카페 리뷰 목록 조회",
        operation_description="특정 카페의 모든 리뷰 목록을 조회합니다.",
        responses={
            200: openapi.Response("리뷰 목록", ReviewSerializer(many=True)),
            404: "Not Found",
        },
    )
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

    @swagger_auto_schema(
        operation_summary="사용자가 찜한 카페 목록 조회",
        operation_description="사용자가 찜한 카페 목록을 조회합니다.",
        responses={
            200: openapi.Response("찜한 카페 목록", CafeLikeSerializer(many=True))
        },
    )
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

    @swagger_auto_schema(
        operation_summary="사용자 리뷰 목록 조회",
        operation_description="사용자가 작성한 리뷰 목록을 조회합니다.",
        responses={
            200: openapi.Response("사용자 리뷰 목록", ReviewSerializer(many=True))
        },
    )
    def get(self, request):
        user = request.user
        reviews = user.reviews.all().order_by("-updated_at")
        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 항목 수를 설정합니다.
        result_page = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class UserLikedReviewsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="사용자가 좋아요한 리뷰 목록 조회",
        operation_description="사용자가 좋아요한 리뷰 목록을 조회합니다.",
        responses={
            200: openapi.Response("좋아요한 리뷰 목록", ReviewLikeSerializer(many=True))
        },
    )
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

    @swagger_auto_schema(
        operation_summary="리뷰 생성",
        operation_description="새로운 리뷰를 생성합니다.",
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="리뷰 업데이트",
        operation_description="특정 리뷰를 업데이트합니다.",
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer, 400: "Bad Request", 404: "Not Found"},
    )
    def patch(self, request, pk):
        user = request.user
        review = Review.objects.get(pk=pk)
        if review.user_id == user.id:
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"detail": "You do not have permission."},
            status=status.HTTP_404_BAD_REQUEST,
        )


class ReviewDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="리뷰 삭제",
        operation_description="특정 리뷰를 삭제합니다.",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, pk):
        user = request.user
        review = Review.objects.get(pk=pk)
        if review.user_id == user.id:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"detail": "You do not have permission."},
            status=status.HTTP_404_BAD_REQUEST,
        )


# CafeLike 관련 API
class CafeLikeCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="카페 찜 생성",
        operation_description="특정 카페를 찜합니다.",
        request_body=CafeLikeSerializer,
        responses={201: CafeLikeSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = CafeLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CafeLikeDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="카페 찜 삭제",
        operation_description="특정 카페의 찜을 삭제합니다.",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, pk):
        like = CafeLike.objects.get(pk=pk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ReviewLike 관련 API
class ReviewLikeCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="리뷰 좋아요 생성",
        operation_description="특정 리뷰를 좋아요합니다.",
        request_body=ReviewLikeSerializer,
        responses={201: ReviewLikeSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = ReviewLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewLikeDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="리뷰 좋아요 삭제",
        operation_description="특정 리뷰의 좋아요를 삭제합니다.",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, pk):
        like = ReviewLike.objects.get(pk=pk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
