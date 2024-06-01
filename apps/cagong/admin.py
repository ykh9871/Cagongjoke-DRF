from django.contrib import admin
from apps.cagong.models import (
    Area,
    Cafe,
    Review,
    CafeLike,
    ReviewLike,
)

admin.site.register(Area)
admin.site.register(Cafe)
admin.site.register(Review)
admin.site.register(CafeLike)
admin.site.register(ReviewLike)
