# Generated by Django 3.2.5 on 2021-08-03 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_pickpair_pick'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickpair',
            name='single',
            field=models.BooleanField(default=False, verbose_name='Is single'),
        ),
    ]