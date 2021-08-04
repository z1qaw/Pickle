from backend.models import PickSession, PickPair, PickSessionRound
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


def make_pairs_round(pick_session, pairs):
    round = PickSessionRound.objects.create(pick_session=pick_session)
    round.pickpair_set.set(pairs)
    return round


def make_pick_round_from_videos_list(pick_session, videos):
    pairs = make_pairs_from_videos_list(videos, pick_session)
    return make_pairs_round(pick_session, pairs)


def get_round_completed_choices(pick_round_id):
    query = Q(completed=True)
    query.add(Q(single=True), Q.OR)
    completed_round_pairs = PickSessionRound.objects.get(id=pick_round_id) \
        .pickpair_set.filter(query)

    chosen_videos = []
    for pair in completed_round_pairs:
        if pair.single:
            chosen_videos.append(pair.videos_pair.all()[0])
        else:
            chosen_videos.append(pair.pick)
    return chosen_videos


def is_round_completed(pick_round_id):
    query = Q(completed=True)
    query.add(Q(single=True), Q.OR)
    completed_round_pairs = PickSessionRound.objects.get(id=pick_round_id) \
        .pickpair_set.filter(query)

    if not completed_round_pairs:
        return True
    else:
        return False
