from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from config import settings


class Command(BaseCommand):
    help = "Google 소셜앱을 생성합니다."

    def handle(self, *args, **kwargs):
        client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
        secret = settings.SOCIAL_AUTH_GOOGLE_SECRET
        app, created = SocialApp.objects.get_or_create(
            provider="google",
            name="google",
            defaults={"client_id": client_id, "secret": secret},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Google 소셜앱 생성됨, ID: {app.id}"))
        else:
            self.stdout.write(
                self.style.WARNING(f"Google 소셜앱 이미 존재함, ID: {app.id}")
            )
