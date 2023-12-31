# Generated by Django 4.2.7 on 2023-11-13 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lieu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('capacity', models.IntegerField()),
                ('provirus', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='DateTest',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='positif',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='gerant',
            field=models.BooleanField(),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.IntegerField()),
                ('date', models.DateField(null=True)),
                ('lieu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal.lieu')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='clientde',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='personal.lieu'),
            preserve_default=False,
        ),
    ]
