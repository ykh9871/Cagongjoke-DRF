from rest_framework import serializers
from apps.cagong.models import Area, Cafe, Review, CafeLike, ReviewLike
from apps.users.serializers import UserSerializer


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
            "id",
            "city_code",
            "city_name",
            "county_code",
            "county_name",
            "town_code",
            "town_name",
        ]


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
            "city_code",
            "city_name",
        ]


class CountyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
            "city_code",
            "county_code",
            "county_name",
        ]


class TownListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
            "id",
            "town_code",
            "town_name",
        ]


class CafeSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Cafe
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cafe = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = "__all__"


class CafeLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cafe = serializers.StringRelatedField()

    class Meta:
        model = CafeLike
        fields = "__all__"


class ReviewLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    review = serializers.StringRelatedField()

    class Meta:
        model = ReviewLike
        fields = "__all__"
