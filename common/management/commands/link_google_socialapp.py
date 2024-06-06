from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = "Google 소셜앱을 사이트와 연결합니다."

    def handle(self, *args, **kwargs):
        try:
            site = Site.objects.get(id=1)
            app = SocialApp.objects.get(provider="google", name="google")
            if site not in app.sites.all():
                app.sites.add(site)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Google 소셜앱과 사이트 연결됨, Site ID: {site.id}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Google 소셜앱과 사이트 이미 연결됨, Site ID: {site.id}"
                    )
                )
        except Site.DoesNotExist:
            self.stdout.write(self.style.ERROR("Site id=1이 존재하지 않습니다"))
        except SocialApp.DoesNotExist:
            self.stdout.write(self.style.ERROR("Google 소셜앱이 존재하지 않습니다"))
