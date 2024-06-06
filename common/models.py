from django.db import models
from django.utils import timezone


# SoftDeleteQuerySet 클래스 정의: 소프트 삭제 관련 쿼리셋 메소드 제공
class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        # 소프트 삭제: is_active를 False로, deleted_at을 현재 시간으로 설정
        return self.update(is_active=False, deleted_at=timezone.now())

    def hard_delete(self):
        # 실제 삭제
        return super().delete()

    def active(self):
        # 활성 상태의 객체 필터링
        return self.filter(is_active=True)

    def inactive(self):
        # 비활성 상태의 객체 필터링
        return self.filter(is_active=False)

    def restore(self):
        # 복구: is_active를 True로, deleted_at을 None으로 설정
        return self.update(is_active=True, deleted_at=None)


# SoftDeleteManager 클래스 정의: 커스텀 매니저로 쿼리셋 메소드 활용
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # 기본 쿼리셋: 활성 상태의 객체만 반환
        return SoftDeleteQuerySet(self.model, using=self._db).active()

    def all_with_deleted(self):
        # 모든 객체 반환 (삭제된 객체 포함)
        return SoftDeleteQuerySet(self.model, using=self._db)

    def hard_delete(self):
        return self.all_with_deleted().hard_delete()

    def active(self):
        return self.all_with_deleted().active()

    def inactive(self):
        return self.all_with_deleted().inactive()

    def restore(self):
        return self.all_with_deleted().restore()


# SoftDeleteModel 추상 클래스 정의: 소프트 삭제를 지원하는 모델
class SoftDeleteModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = SoftDeleteManager()  # 기본 매니저 교체
    all_objects = models.Manager()  # 기본 매니저 유지

    class Meta:
        abstract = True  # 추상 클래스 선언

    def delete(self, using=None, keep_parents=False):
        # 삭제 메소드: 소프트 삭제 및 연관된 객체도 소프트 삭제
        self._soft_delete()

    def restore(self):
        # 복구 메소드: 복구 및 연관된 객체도 복구
        self._restore()

    def hard_delete(self, using=None, keep_parents=False):
        # 실제 삭제 메소드
        super().delete(using=using, keep_parents=keep_parents)

    def _soft_delete(self):
        # 소프트 삭제 동작
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_active", "deleted_at"])  # 변경된 필드만 업데이트
        self._cascade_update(is_active=False, deleted_at=self.deleted_at)

    def _restore(self):
        # 복구 동작
        self.is_active = True
        self.deleted_at = None
        self.updated_at = timezone.now()
        self.save(
            update_fields=["is_active", "deleted_at", "updated_at"]
        )  # 변경된 필드만 업데이트
        self._cascade_update(
            is_active=True, deleted_at=None, updated_at=self.updated_at
        )

    def _cascade_update(self, **kwargs):
        # 연관된 모든 객체 업데이트
        for related_object in self._meta.related_objects:
            related_manager = getattr(self, related_object.get_accessor_name(), None)
            if related_manager:
                related_manager.all().update(**kwargs)
