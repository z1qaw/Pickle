from backend.models import PickSession, PickPair
from django.db.models import Q


def make_pairs_from_videos_list(pick_playlist_videos: list, pick_session: PickSession):
    current_pair = []
    pairs = []
    for i, video in enumerate(pick_playlist_videos):
        current_pair.append(video)
        pair = None

        if i+1 == len(pick_playlist_videos) and len(current_pair) == 1:
            pair = PickPair.objects.create(
                pick_session=pick_session,
                single=True
            )
            pair.videos_pair.set(current_pair)

        if len(current_pair) == 2:
            pair = PickPair.objects.create(
                pick_session=pick_session,
            )
            pair.videos_pair.set(current_pair)
            current_pair = []

        if pair:
            pairs.append(pair)
    
    return pairs


def make_completed_pairs_from_pick_session(pick_session: PickSession):
    query = Q(completed=True)
    query.add(Q(single=True), Q.OR)
    query.add(Q(pick_session=pick_session), Q.AND)

    completed_pairs = PickPair.objects.filter(query)
    next_videos = []
    for pair in completed_pairs:
        next_videos.append(pair.pick)
    
    return make_pairs_from_videos_list(next_videos, pick_session)
