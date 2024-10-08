# Generated by Django 4.2.11 on 2024-06-06 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cagong', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='cafe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='cagong.cafe'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cafelike',
            name='cafe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='cagong.cafe'),
        ),
        migrations.AddField(
            model_name='cafelike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cafe_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cafe',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cafes', to='cagong.area'),
        ),
    ]
