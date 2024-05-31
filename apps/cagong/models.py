from django.db import models
from apps.users.models import User


class Region(models.Model):
    id = models.IntegerField(primary_key=True)  # 지역 코드를 기본 키로 사용
    city_code = models.IntegerField()
    city_name = models.CharField(max_length=100)
    county_code = models.IntegerField()
    county_name = models.CharField(max_length=100)
    town_code = models.IntegerField()
    town_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)


class Cafe(models.Model):
    id = models.IntegerField(primary_key=True)
    crawl_id = models.CharField(null=True, max_length=20)
    is_crawled = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    wordcloud = models.TextField(null=True, blank=True)
    area = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="cafes"
    )  # 지역과 1:N 관계
    address = models.CharField(max_length=200)
    kagong = models.BooleanField(default=False)  # 가공 여부
    phonenum = models.CharField(max_length=20)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = True


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="reviews"
    )  # 사용자와 1:N 관계
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, related_name="reviews"
    )  # 카페와 1:N 관계
    review = models.TextField()
    crawling = models.BooleanField(default=False)  # 크롤링 여부
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class CafeLike(models.Model):
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, related_name="likes"
    )  # 카페와 N:N 관계
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cafe_likes"
    )  # 사용자와 N:N 관계
    liked_at = models.DateTimeField(auto_now_add=True)  # 좋아요 시간 기록


class ReviewLike(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="likes"
    )  # 리뷰와 N:N 관계
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review_likes"
    )  # 사용자와 N:N 관계
    liked_at = models.DateTimeField(auto_now_add=True)  # 좋아요 시간 기록
