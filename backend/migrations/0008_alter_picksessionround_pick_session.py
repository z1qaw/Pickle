# Generated by Django 3.2.5 on 2021-08-03 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20210803_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picksessionround',
            name='pick_session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.picksession'),
        ),
    ]
