from django.urls import path
from apps.cagong.views import (
    AreaListCreateAPIView,
    AreaDetailAPIView,
    CafeListCreateAPIView,
    CafeDetailAPIView,
    ReviewListCreateAPIView,
    ReviewDetailAPIView,
    CafeLikeListCreateAPIView,
    CafeLikeDetailAPIView,
    ReviewLikeListCreateAPIView,
    ReviewLikeDetailAPIView,
)

urlpatterns = [
    path("areas/", AreaListCreateAPIView.as_view(), name="area-list-create"),
    path("areas/<int:pk>/", AreaDetailAPIView.as_view(), name="area-detail"),
    path("cafes/", CafeListCreateAPIView.as_view(), name="cafe-list-create"),
    path("cafes/<int:pk>/", CafeDetailAPIView.as_view(), name="cafe-detail"),
    path("reviews/", ReviewListCreateAPIView.as_view(), name="review-list-create"),
    path("reviews/<int:pk>/", ReviewDetailAPIView.as_view(), name="review-detail"),
    path(
        "cafe-likes/", CafeLikeListCreateAPIView.as_view(), name="cafe-like-list-create"
    ),
    path(
        "cafe-likes/<int:pk>/", CafeLikeDetailAPIView.as_view(), name="cafe-like-detail"
    ),
    path(
        "review-likes/",
        ReviewLikeListCreateAPIView.as_view(),
        name="review-like-list-create",
    ),
    path(
        "review-likes/<int:pk>/",
        ReviewLikeDetailAPIView.as_view(),
        name="review-like-detail",
    ),
]
