# Generated by Django 3.1.5 on 2021-02-18 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0002_auto_20210209_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationslot',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]