# Generated by Django 3.0.2 on 2020-08-08 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumnisearch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumnusprofile',
            name='profile_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]