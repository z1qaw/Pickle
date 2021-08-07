from django.urls import path

from .views import (create_pick_playlist, create_pick_session,
                    get_next_session_round, pick_pair_video,
                    submit_pick_session_completion)

urlpatterns = [
    path('create_pick_playlist/', create_pick_playlist),
    path('create_pick_session/', create_pick_session),
    path('get_next_session_round/', get_next_session_round),
    path('pick_pair_video/', pick_pair_video),
    path('submit_pick_session_completion/', submit_pick_session_completion),
]
