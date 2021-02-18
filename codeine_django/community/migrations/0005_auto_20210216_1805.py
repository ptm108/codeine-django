# Generated by Django 3.1.5 on 2021-02-16 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0004_auto_20210216_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlecomment',
            name='member',
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='article_comments', to='common.baseuser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='codereviewcomment',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='code_review_comments', to='common.baseuser'),
            preserve_default=False,
        ),
    ]