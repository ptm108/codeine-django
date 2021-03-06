# Generated by Django 3.1.5 on 2021-02-23 06:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20210222_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('bank_account', models.CharField(max_length=50)),
                ('bank_name', models.CharField(max_length=255)),
                ('swift_code', models.CharField(max_length=20)),
                ('bank_country', models.CharField(max_length=255)),
                ('bank_address', models.CharField(max_length=255)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_details', to='common.partner')),
            ],
        ),
    ]
