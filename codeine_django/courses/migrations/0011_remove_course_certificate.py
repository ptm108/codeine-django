# Generated by Django 3.1.5 on 2021-02-17 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_remove_course_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='certificate',
        ),
    ]
