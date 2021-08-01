from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class YoutubeVideo(models.Model):
    '''
    Simple model of Youtube video. Includes only name and link.
    '''
    
    name = models.CharField('Video name', unique=False, null=True, blank=False, max_length=256)
    link = models.CharField('Video link', unique=False, null=False, blank=False, max_length=256)


class PickPair(models.Model):
    '''
    Pick pair model.
    
    videos_pair must contain only 2 instances of YoutubeVideo model.

    This model instances creates on every pick session creation.
    '''

    pick_session = models.ForeignKey(to='PickSession', on_delete=models.CASCADE)
    videos_pair = models.ManyToManyField(verbose_name='Videos pair', to=YoutubeVideo, related_name='pairs')
    completed = models.BooleanField('Completed', default=False)
    pick = models.ForeignKey(verbose_name='User pick', to=YoutubeVideo, null=True, on_delete=models.CASCADE)


class PickPlaylist(models.Model):
    '''
    PickPlaylist model. Creates by user and is public, so every user can see it and
    play with it in pick game.
    '''

    author = models.ForeignKey(verbose_name='Author', to=User, on_delete=models.CASCADE)
    name = models.CharField('Pick playlist name', blank=False, null=False, max_length=120)
    youtube_link = models.CharField('Youtube link', unique=True, null=False, blank=False, max_length=256)


class PickSession(models.Model):
    '''
    PicSession model. Creates when user wants to play in pick game and generates
    new pairs based on youtube playlist videos.
    '''

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    pick_playlist = models.ForeignKey(to=PickPlaylist, on_delete=models.CASCADE)
    completed = models.BooleanField('Completed', blank=False, default=False)
