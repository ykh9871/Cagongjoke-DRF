from rest_framework import serializers
from apps.cagong.models import Area, Cafe, Review, CafeLike, ReviewLike
from apps.users.serializers import UserSerializer


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"


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
