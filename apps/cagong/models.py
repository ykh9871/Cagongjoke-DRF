from django.db import models
from apps.users.models import User
from common.models import SoftDeleteModel


class Area(SoftDeleteModel):
    id = models.IntegerField(primary_key=True)  # 지역 코드를 기본 키로 사용
    city_code = models.IntegerField()
    city_name = models.CharField(max_length=100)
    county_code = models.IntegerField()
    county_name = models.CharField(max_length=100)
    town_code = models.IntegerField()
    town_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city_name} {self.county_name} {self.town_name}"


class Cafe(SoftDeleteModel):
    crawl_id = models.CharField(unique=True, null=True, max_length=20)
    is_crawled = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    wordcloud = models.TextField(null=True, blank=True)
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, related_name="cafes"
    )  # 지역과 1:N 관계
    addr = models.CharField(max_length=200)
    kagong = models.BooleanField(default=False)  # 가공 여부
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(SoftDeleteModel):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="reviews"
    )  # 사용자와 1:N 관계
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, related_name="reviews"
    )  # 카페와 1:N 관계
    review = models.TextField()
    crawling = models.BooleanField(default=False)  # 크롤링 여부
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cafe.name}카페의 리뷰"


class CafeLike(SoftDeleteModel):
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, related_name="likes"
    )  # 카페와 N:N 관계
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cafe_likes"
    )  # 사용자와 N:N 관계

    def __str__(self):
        return f"{self.user.email} likes {self.cafe.name}"


class ReviewLike(SoftDeleteModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="likes"
    )  # 리뷰와 N:N 관계
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review_likes"
    )  # 사용자와 N:N 관계

    def __str__(self):
        return f"{self.user.email} likes a review of {self.review.cafe.name}"
