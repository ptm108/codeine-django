# Generated by Django 3.1.5 on 2021-02-21 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0009_auto_20210220_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationslot',
            name='is_all_day',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='consultationslot',
            name='r_rule',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
    ]