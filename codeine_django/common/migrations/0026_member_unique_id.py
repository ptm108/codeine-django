# Generated by Django 3.1.7 on 2021-04-06 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0025_auto_20210403_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='unique_id',
            field=models.CharField(default=None, max_length=10, null=True, unique=True),
        ),
    ]
