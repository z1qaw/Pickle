from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class YoutubeVideo(models.Model):
    '''
        Simple model of Youtube video. Includes only name and link.
    '''
    
    name = models.CharField('Video name', unique=False, null=True, blank=False, max_length=256)
    youtube_id = models.CharField('Video link', unique=False, null=False, blank=False, max_length=256)
    pick_playlist = models.ForeignKey(to='PickPlaylist', on_delete=models.CASCADE, null=True)


class PickPair(models.Model):
    '''
        Pick pair model.
        
        videos_pair must contain only 2 instances of YoutubeVideo model.

        This model instances creates on every pick session creation.
    '''
    pick_session = models.ForeignKey(to='PickSession', null=True, on_delete=models.CASCADE)
    pick_round = models.ForeignKey(to='PickSessionRound', null=True, on_delete=models.CASCADE)
    videos_pair = models.ManyToManyField(verbose_name='Videos pair', to=YoutubeVideo, related_name='pairs')
    completed = models.BooleanField('Completed', default=False)
    pick = models.ForeignKey(verbose_name='User pick', to=YoutubeVideo,
                             null=True, on_delete=models.CASCADE,
                             default=None)
    single = models.BooleanField('Is single', default=False)
    pick_round = models.ForeignKey(to='PickSessionRound', null=True, on_delete=models.CASCADE)


class PickPlaylist(models.Model):
    '''
        PickPlaylist model. Creates by user and is public, so every user can see it and
        play with it in pick game.
    '''

    author = models.ForeignKey(verbose_name='Author', to=User, on_delete=models.CASCADE)
    name = models.CharField('Pick playlist name', blank=False, null=False, max_length=120)
    youtube_id = models.CharField('Youtube link', unique=True, null=False, blank=False, max_length=256)


class PickSession(models.Model):
    '''
        PickSession model. Creates when user wants to play in pick game and generates
        new pairs based on youtube playlist videos.
    '''
    current_round = models.ForeignKey(to='PickSessionRound', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pick_playlist = models.ForeignKey(to=PickPlaylist, on_delete=models.CASCADE)
    pick = models.ForeignKey(to=YoutubeVideo, null=True, on_delete=models.SET_NULL)
    completed = models.BooleanField('Completed', blank=False, default=False)


class PickSessionRound(models.Model):
    '''
        PickSessionRound model.

        Must be created on every pick round, when user complete all
            available pick pairs.
    '''
    completed = models.BooleanField('Completed', default=False)
    pick_session = models.ForeignKey(to=PickSession, on_delete=models.CASCADE)
