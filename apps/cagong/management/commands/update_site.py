from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = "id가 1인 django_site 테이블의 데이터를 업데이트"

    def handle(self, *args, **kwargs):
        try:
            site = Site.objects.get(id=1)
            site.domain = "localhost:8000"
            site.name = "localhost:8000"
            site.save()
            self.stdout.write(self.style.SUCCESS("Site id=1 업데이트 완료"))
        except Site.DoesNotExist:
            self.stdout.write(self.style.ERROR("Site id=1이 존재하지 않습니다"))
