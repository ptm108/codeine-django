# Generated by Django 3.1.7 on 2021-03-20 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0017_auto_20210320_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomment',
            name='time_edited',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
