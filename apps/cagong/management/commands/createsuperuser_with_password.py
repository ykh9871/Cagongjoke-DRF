from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = "지정된 비밀번호로 슈퍼유저 생성"

    def add_arguments(self, parser):
        parser.add_argument("--username", required=True, help="슈퍼유저의 사용자 이름")
        parser.add_argument("--email", required=True, help="슈퍼유저의 이메일 주소")
        parser.add_argument("--password", required=True, help="슈퍼유저의 비밀번호")

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    '사용자 이름 "{}"을(를) 가진 유저가 이미 존재합니다.'.format(
                        username
                    )
                )
            )
        else:
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    '슈퍼유저 "{}"가 성공적으로 생성되었습니다.'.format(username)
                )
            )
