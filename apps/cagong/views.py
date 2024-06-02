from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
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


class AreaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    @swagger_auto_schema(
        operation_summary="지역 목록 조회",
        operation_description="모든 지역의 목록을 가져옵니다.",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="새 지역 생성",
        operation_description="새로운 지역을 생성합니다.",
        request_body=AreaSerializer,
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AreaDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    @swagger_auto_schema(
        operation_summary="지역 조회", operation_description="ID로 지역을 조회합니다."
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="지역 업데이트",
        operation_description="ID로 지역을 업데이트합니다.",
        request_body=AreaSerializer,
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="지역 부분 업데이트",
        operation_description="ID로 지역을 부분 업데이트합니다.",
        request_body=AreaSerializer,
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="지역 삭제", operation_description="ID로 지역을 삭제합니다."
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CafeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer

    @swagger_auto_schema(
        operation_summary="카페 목록 조회",
        operation_description="모든 카페의 목록을 가져옵니다.",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="새 카페 생성",
        operation_description="새로운 카페를 생성합니다.",
        request_body=CafeSerializer,
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CafeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer

    @swagger_auto_schema(
        operation_summary="카페 조회", operation_description="ID로 카페를 조회합니다."
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="카페 업데이트",
        operation_description="ID로 카페를 업데이트합니다.",
        request_body=CafeSerializer,
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="카페 부분 업데이트",
        operation_description="ID로 카페를 부분 업데이트합니다.",
        request_body=CafeSerializer,
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="카페 삭제", operation_description="ID로 카페를 삭제합니다."
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @swagger_auto_schema(
        operation_summary="리뷰 목록 조회",
        operation_description="모든 리뷰의 목록을 가져옵니다.",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="새 리뷰 생성",
        operation_description="새로운 리뷰를 생성합니다.",
        request_body=ReviewSerializer,
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReviewListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="리뷰 목록 조회",
        operation_description="모든 리뷰의 목록을 가져옵니다.",
        responses={200: ReviewSerializer(many=True)},
    )
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="새 리뷰 생성",
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


class ReviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="리뷰 조회",
        operation_description="ID로 리뷰를 조회합니다.",
        responses={200: ReviewSerializer, 404: "Not Found"},
    )
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="리뷰 업데이트",
        operation_description="ID로 리뷰를 업데이트합니다.",
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer, 400: "Bad Request", 404: "Not Found"},
    )
    def put(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="리뷰 부분 업데이트",
        operation_description="ID로 리뷰를 부분 업데이트합니다.",
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer, 400: "Bad Request", 404: "Not Found"},
    )
    def patch(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="리뷰 삭제",
        operation_description="ID로 리뷰를 삭제합니다.",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CafeLikeListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="카페 좋아요 목록 조회",
        operation_description="모든 카페 좋아요의 목록을 가져옵니다.",
        responses={200: CafeLikeSerializer(many=True)},
    )
    def get(self, request):
        likes = CafeLike.objects.all()
        serializer = CafeLikeSerializer(likes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="새 카페 좋아요 생성",
        operation_description="새로운 카페 좋아요를 생성합니다.",
        request_body=CafeLikeSerializer,
        responses={201: CafeLikeSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = CafeLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CafeLikeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="카페 좋아요 조회",
        operation_description="ID로 카페 좋아요를 조회합니다.",
        responses={200: CafeLikeSerializer, 404: "Not Found"},
    )
    def get(self, request, pk):
        try:
            like = CafeLike.objects.get(pk=pk)
            serializer = CafeLikeSerializer(like)
            return Response(serializer.data)
        except CafeLike.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="카페 좋아요 삭제",
        operation_description="ID로 카페 좋아요를 삭제합니다.",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, pk):
        try:
            like = CafeLike.objects.get(pk=pk)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CafeLike.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ReviewLikeListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="리뷰 좋아요 목록 조회",
        operation_description="모든 리뷰 좋아요의 목록을 가져옵니다.",
        responses={200: ReviewLikeSerializer(many=True)},
    )
    def get(self, request):
        likes = ReviewLike.objects.all()
        serializer = ReviewLikeSerializer(likes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="새 리뷰 좋아요 생성",
        operation_description="새로운 리뷰 좋아요를 생성합니다.",
        request_body=ReviewLikeSerializer,
        responses={201: ReviewLikeSerializer, 400: "Bad Request"},
    )
    def post(self, request):
        serializer = ReviewLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewLikeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="리뷰 좋아요 조회",
        operation_description="ID로 리뷰 좋아요를 조회합니다.",
        responses={200: ReviewLikeSerializer, 404: "Not Found"},
    )
    def get(self, request, pk):
        try:
            like = ReviewLike.objects.get(pk=pk)
            serializer = ReviewLikeSerializer(like)
            return Response(serializer.data)
        except ReviewLike.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_summary="리뷰 좋아요 삭제",
        operation_description="ID로 리뷰 좋아요를 삭제합니다.",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, pk):
        try:
            like = ReviewLike.objects.get(pk=pk)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReviewLike.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
