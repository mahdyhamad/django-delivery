# Generated by Django 3.1.1 on 2020-09-16 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200913_2031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_shop',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_shop',
            field=models.BooleanField(default=False),
        ),
    ]