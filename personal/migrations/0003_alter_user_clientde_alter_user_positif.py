# Generated by Django 4.2.7 on 2023-11-13 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0002_lieu_user_datetest_user_positif_alter_user_gerant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='clientde',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='personal.lieu'),
        ),
        migrations.AlterField(
            model_name='user',
            name='positif',
            field=models.BooleanField(null=True),
        ),
    ]
