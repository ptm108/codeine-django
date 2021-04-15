# Generated by Django 3.1.7 on 2021-04-12 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('achievements', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberachievement',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to='common.member'),
        ),
        migrations.AddField(
            model_name='achievementrequirement',
            name='achievement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievement_requirements', to='achievements.achievement'),
        ),
    ]