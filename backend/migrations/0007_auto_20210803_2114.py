# Generated by Django 3.2.5 on 2021-08-03 21:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20210803_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pickpair',
            name='pick_session',
        ),
        migrations.AddField(
            model_name='picksession',
            name='current_round',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.picksessionround'),
        ),
        migrations.AddField(
            model_name='picksessionround',
            name='pick_session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.picksession'),
        ),
    ]
