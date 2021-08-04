# Generated by Django 3.2.5 on 2021-08-03 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_pickpair_single'),
    ]

    operations = [
        migrations.CreateModel(
            name='PickSessionRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed')),
            ],
        ),
        migrations.AddField(
            model_name='pickpair',
            name='pick_round',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.picksessionround'),
        ),
    ]
