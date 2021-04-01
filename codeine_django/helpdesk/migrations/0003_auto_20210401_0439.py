# Generated by Django 3.1.7 on 2021-04-01 04:39

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0020_auto_20210323_1702'),
        ('helpdesk', '0002_auto_20210331_0401'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='code_review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to='community.codereview'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_type',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('ACCOUNT', 'Account'), ('GENERAL', 'General'), ('TECHNICAL', 'Technical'), ('PAYMENT', 'Payments'), ('COURSE', 'Courses'), ('ARTICLE', 'Articles'), ('CODE_REVIEWS', 'Code Reviews'), ('INDUSTRY_PROJECT', 'Industry Projects'), ('CONSULTATION', 'Consultations')], max_length=91),
        ),
    ]
