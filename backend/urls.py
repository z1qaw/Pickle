from django.urls import path
from .views import create_pick_playlist, create_pick_session

urlpatterns = [
    path('create_pick_playlist/', create_pick_playlist),
    path('create_pick_session/', create_pick_session)
]