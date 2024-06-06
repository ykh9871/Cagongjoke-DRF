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
    path("areas/", AreaUpdateAPIView.as_view(), name="area-update"),
]
