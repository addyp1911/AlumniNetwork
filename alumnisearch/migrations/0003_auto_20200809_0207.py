# Generated by Django 3.0.2 on 2020-08-08 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumnisearch', '0002_auto_20200809_0201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumnusprofile',
            name='profile_name',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
