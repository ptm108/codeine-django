# Generated by Django 3.1.7 on 2021-03-18 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_auto_20210316_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='search_string',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]