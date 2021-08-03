from rest_framework.response import Response
from rest_framework.decorators import \
    api_view, permission_classes, authentication_classes
from rest_framework.authentication import \
    SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .services.youtube import YoutubeApi
from .models import PickPlaylist, YoutubeVideo, PickSession, PickPair
from rest_framework.status import HTTP_201_CREATED


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_pick_playlist(request):
    '''
        Create pick playlist view

        Youtube playlist id must be provided in
            youtube_playlist_id (str) field in json data.
    '''

    playlist_info = YoutubeApi.get_playlist_info(request.data['youtube_playlist_id'])
    playlist = PickPlaylist.objects.create(
        author=request.user,
        name=playlist_info['items'][0]['snippet']['title'],
        youtube_id=request.data['youtube_playlist_id'],
    )
    playlist_items = YoutubeApi.get_full_playlist_items(request.data['youtube_playlist_id'])
    for item in playlist_items:
        YoutubeVideo.objects.create(
            name=item['snippet']['title'],
            youtube_id=item['id'],
            pick_playlist=playlist)
    return Response(status=HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_pick_session(request):
    '''
        Create pick session.

        Pick playlist id must be provided in
            pick_playlist_id (int) field in json data.
    '''

    pick_session = PickSession.objects.create(
        user=request.user,
        pick_playlist=PickPlaylist.objects.get(
            id=request.data['pick_playlist_id']
        )
    )
    pick_playlist_videos = list(YoutubeVideo.objects.filter(
        pick_playlist=request.data['pick_playlist_id']
    ))

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

    return Response(
        {
            'id': pick_session.id,
            'author_id': pick_session.user.id,
            'pairs': [
                    {
                        'id': pair.id,
                        'is_single': pair.single,
                    } for pair in pairs
                ]
        }
    )
