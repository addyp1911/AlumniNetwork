# Generated by Django 3.0.2 on 2020-08-10 21:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alumnisearch', '0005_auto_20200810_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(blank=True, max_length=100, null=True)),
                ('alumnus', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
