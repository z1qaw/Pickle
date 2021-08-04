from django.urls import path

from .views import (create_pick_playlist, create_pick_session,
                    get_next_session_round, make_pair_choice,
                    pick_pair_video)

urlpatterns = [
    path('create_pick_playlist/', create_pick_playlist),
    path('create_pick_session/', create_pick_session),
    path('make_pair_choice/', make_pair_choice),
    path('get_next_session_round/', get_next_session_round),
    path('pick_pair_video/', pick_pair_video),
]
