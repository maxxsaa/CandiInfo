# Generated by Django 4.2.7 on 2023-11-14 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0004_lieu_proprietaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='personne',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lieu',
            name='proprietaire',
            field=models.CharField(max_length=30),
        ),
    ]
