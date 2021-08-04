from django.contrib import admin
from .models import *


models_to_register = [YoutubeVideo, PickPair, PickPlaylist,
                        PickSession, PickSessionRound]
for model in models_to_register:
    admin.site.register(model)