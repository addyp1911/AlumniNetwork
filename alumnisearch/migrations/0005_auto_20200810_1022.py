# Generated by Django 3.0.2 on 2020-08-10 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alumnisearch', '0004_auto_20200809_1945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alumnusprofile',
            old_name='state',
            new_name='address',
        ),
    ]
