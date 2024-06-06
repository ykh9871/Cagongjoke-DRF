from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_yasg.utils import swagger_auto_schema
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
        areas = Area.objects.values("city_name", "city_code").distinct()
        return Response(areas)


class CountyListAPIView(APIView):
    def get(self, request, city_code):
        counties = (
            Area.objects.filter(city_code=city_code)
            .values("county_code", "county_name")
            .distinct()
        )
        return Response(counties)


class TownListAPIView(APIView):
    def get(self, request, county_code):
        towns = (
            Area.objects.filter(county_code=county_code)
            .values("town_code", "town_name")
            .distinct()
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
