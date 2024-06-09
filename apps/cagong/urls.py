from django.urls import path
from .views import *

urlpatterns = [
    # Area 관련 API
    path("areas/cities/", CityListAPIView.as_view(), name="city-name-list"),
    path(
        "areas/cities/<int:city_code>/counties/",
        CountyListAPIView.as_view(),
        name="county-name-list",
    ),
    path(
        "areas/counties/<int:county_code>/towns/",
        TownListAPIView.as_view(),
        name="town-name-list",
    ),
    path("areas/", AreaCreateAPIView.as_view(), name="area-create"),
    path("areas/<int:pk>/", AreaUpdateAPIView.as_view(), name="area-update"),
    path("areas/<int:pk>/", AreaDeleteAPIView.as_view(), name="area-delete"),
    # Cafe 관련 API
    # /cafes/areas/?area_id=11&page=1 형태로 호출할 수 있습니다.
    path("cafes/areas/", CafeListAPIView.as_view(), name="cafe-list"),
    path("cafes/<int:pk>/", CafeDetailAPIView.as_view(), name="cafe-detail"),
    path("cafes/", CafeCreateAPIView.as_view(), name="cafe-create"),
    path("cafes/<int:pk>/", CafeUpdateAPIView.as_view(), name="cafe-update"),
    path("cafes/<int:pk>/", CafeDeleteAPIView.as_view(), name="cafe-delete"),
    path(
        "cafes/<int:pk>/like-count/",
        CafeLikeCountAPIView.as_view(),
        name="cafe-like-count",
    ),
    path(
        "cafes/<int:pk>/review-count/",
        CafeReviewCountAPIView.as_view(),
        name="cafe-review-count",
    ),
    path(
        "cafes/<int:pk>/reviews/",
        CafeReviewListAPIView.as_view(),
        name="cafe-review-list",
    ),
    path(
        "users/liked_cafes/",
        UserLikedCafesAPIView.as_view(),
        name="user-liked-cafes",
    ),
    # Review 관련 API
    path("users/reviews/", UserReviewsAPIView.as_view(), name="user-reviews"),
    path(
        "users/liked_reviews/",
        UserLikedReviewsAPIView.as_view(),
        name="user-liked-reviews",
    ),
    path("reviews/", ReviewCreateAPIView.as_view(), name="review-create"),
]
