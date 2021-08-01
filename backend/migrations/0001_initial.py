# Generated by Django 3.2.5 on 2021-08-01 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PickPlaylist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Pick playlist name')),
                ('youtube_link', models.CharField(max_length=256, unique=True, verbose_name='Youtube link')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
        ),
        migrations.CreateModel(
            name='YoutubeVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, null=True, verbose_name='Video name')),
                ('link', models.CharField(max_length=256, verbose_name='Video link')),
            ],
        ),
        migrations.CreateModel(
            name='PickSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('pick_playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.pickplaylist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PickPair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False, verbose_name='Completed')),
                ('pick', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.youtubevideo', verbose_name='User pick')),
                ('pick_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.picksession')),
                ('videos_pair', models.ManyToManyField(related_name='pairs', to='backend.YoutubeVideo', verbose_name='Videos pair')),
            ],
        ),
    ]
