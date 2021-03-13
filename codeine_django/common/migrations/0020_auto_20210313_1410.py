# Generated by Django 3.1.7 on 2021-03-13 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0019_auto_20210313_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='receivers',
        ),
        migrations.AddField(
            model_name='notification',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
