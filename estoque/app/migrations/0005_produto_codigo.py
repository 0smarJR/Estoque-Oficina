# Generated by Django 3.1.1 on 2020-09-17 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200914_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='codigo',
            field=models.IntegerField(default=None),
        ),
    ]