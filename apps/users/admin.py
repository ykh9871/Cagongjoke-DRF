from django.contrib import admin
from django.utils.html import format_html
from apps.users.models import User


def soft_delete(modeladmin, request, queryset):
    queryset.update(is_active=False)


soft_delete.short_description = "선택된 user를 Soft Delete 합니다."


def hard_delete(modeladmin, request, queryset):
    queryset.hard_delete()


hard_delete.short_description = "선택된 user를 Hard Delete 합니다."


def restore(modeladmin, request, queryset):
    queryset.restore()


restore.short_description = "선택된 user를 Restore 합니다."


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "is_active",
        "is_staff",
        "created_at",
        "deleted_at",
    )
    list_filter = ("is_active",)  # is_active 필터 추가
    actions = [soft_delete, hard_delete, restore]  # restore 액션 추가

    def is_active(self, obj):
        if not obj.is_active:
            return format_html('<span style="color: red;">{}</span>', obj.is_active)
        return obj.is_active

    is_active.boolean = True  # True/False 아이콘 표시

    def get_queryset(self, request):
        # 모든 유저를 반환하도록 queryset을 수정합니다.
        return User.objects.all_with_deleted()


admin.site.register(User, UserAdmin)
