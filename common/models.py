from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_active=False, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # 기본적으로 활성화된 객체만 반환
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_active=True)

    def all_with_deleted(self):
        # 활성화 여부에 관계없이 모든 객체 반환
        return SoftDeleteQuerySet(self.model, using=self._db)

    def hard_delete(self):
        return self.all_with_deleted().hard_delete()

    def active(self):
        return self.all_with_deleted().active()

    def inactive(self):
        return self.all_with_deleted().inactive()


class SoftDeleteModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = SoftDeleteManager()  # 기본 매니저 교체
    all_objects = models.Manager()  # 기본 매니저 유지

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

        # CASCADE 처리를 위해 연결된 객체도 삭제 처리
        for related_object in self._meta.related_objects:
            related_manager = getattr(self, related_object.get_accessor_name(), None)
            if related_manager:
                related_manager.all().update(is_active=False, deleted_at=timezone.now())

    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.updated_at = timezone.now()
        self.save()

        # CASCADE 처리를 위해 연결된 객체도 복원 처리
        for related_object in self._meta.related_objects:
            related_manager = getattr(self, related_object.get_accessor_name(), None)
            if related_manager:
                related_manager.all().update(
                    is_active=True, deleted_at=None, updated_at=timezone.now()
                )

    def hard_delete(self, using=None, keep_parents=False):
        super(SoftDeleteModel, self).delete(using=using, keep_parents=keep_parents)
