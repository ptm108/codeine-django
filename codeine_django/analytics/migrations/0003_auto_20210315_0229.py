# Generated by Django 3.1.7 on 2021-03-15 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20210312_0930'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventlog',
            options={'ordering': ['-timestamp']},
        ),
    ]
