from django.contrib import admin
from cafes.models import (
    Region,
    Cafe,
    Review,
    CafeLike,
    ReviewLike,
)

admin.site.register(Region)
admin.site.register(Cafe)
admin.site.register(Review)
admin.site.register(CafeLike)
admin.site.register(ReviewLike)
