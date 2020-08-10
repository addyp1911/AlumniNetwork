# Generated by Django 3.0.2 on 2020-08-10 22:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alumnisearch', '0006_user_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_post',
            name='alumnus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL),
        ),
    ]