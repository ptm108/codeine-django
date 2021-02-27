# Generated by Django 3.1.5 on 2021-02-26 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0005_auto_20210216_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecomment',
            name='time_edited',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='codereviewcomment',
            name='time_edited',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='articlecomment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]