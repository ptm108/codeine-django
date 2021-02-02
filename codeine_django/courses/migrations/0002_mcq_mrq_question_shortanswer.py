# Generated by Django 3.1.5 on 2021-02-02 15:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.TextField()),
                ('subtitle', models.TextField(blank=True, default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShortAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField(default=1)),
                ('keywords', models.JSONField()),
                ('question', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.question')),
            ],
        ),
        migrations.CreateModel(
            name='MRQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField(default=1)),
                ('options', models.JSONField()),
                ('correct_answer', models.JSONField()),
                ('question', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.question')),
            ],
        ),
        migrations.CreateModel(
            name='MCQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField(default=1)),
                ('options', models.JSONField()),
                ('correct_answer', models.CharField(max_length=255)),
                ('question', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.question')),
            ],
        ),
    ]
