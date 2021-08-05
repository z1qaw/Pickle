from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)

from backend.serializers import YoutubeVideoSerializer, PickPairSerializer
from backend.services.pickle import (get_round_completed_choices,
                                     is_round_completed,
                                     make_pick_round_from_videos_list,
                                     pick_video_from_pair)

from .models import PickPair, PickPlaylist, PickSession, YoutubeVideo
from .permissions import IsPickPairOwnerOrSuperuser, IsPickSessionOwnerOrSuperuser
from .services.youtube import YoutubeApi


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_pick_playlist(request):
    '''
        Create pick playlist view

        Youtube playlist id must be provided in
            youtube_playlist_id (str) field in json data.

        Example data: {"youtube_playlist_id": "PLSUE3Jrs90TDCt2rDjxWWb5EdZFlF8RLJ"}
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

        Example data: {"pick_playlist_id": 10}
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

    round = make_pick_round_from_videos_list(pick_session, pick_playlist_videos)
    pick_session.current_round = round

    return Response(
        {
            'id': pick_session.id,
            'pick_playlist_id': request.data['pick_playlist_id'],
            'author_id': pick_session.user.id,
            'current_round': {
                'id': round.id,
                'completed': round.completed,
                'pairs': [
                    {
                        'id': pair.id,
                        'completed': pair.completed,
                        'pick': pair.pick,
                        'is_single': pair.single,
                        'pick_videos': [
                            YoutubeVideoSerializer(video).data 
                            for video in pair.videos_pair.all()]
                    } for pair in round.pickpair_set.all()
                ]
            }
        },
        status=HTTP_201_CREATED
    )


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsPickSessionOwnerOrSuperuser])
def get_next_session_round(request):
    pick_session_id = request.query_params['pick_session_id']
    pick_session = PickSession.objects.get(id=pick_session_id)
    current_round_id = pick_session.current_round.id
    if is_round_completed(current_round_id):
        round_choises = get_round_completed_choices(current_round_id)
        next_round = make_pick_round_from_videos_list(
            pick_session,
            round_choises
        )
        pick_session.current_round.completed = True
        pick_session.current_round = next_round
        pick_session.save()
        return Response(
            {
                'id': next_round.id,
                'completed': next_round.completed,
                'pairs': [
                    {
                        'id': pair.id,
                        'completed': pair.completed,
                        'pick': pair.pick,
                        'is_single': pair.single
                    } for pair in next_round.pickpair_set.all()
                ]
            },
            status=HTTP_201_CREATED
        )
    else:
        return Response(
            {'message': 'Current round isn\'t completed.'},
            status=HTTP_400_BAD_REQUEST,
        )


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsPickPairOwnerOrSuperuser])
def pick_pair_video(request):
    updated_pair = pick_video_from_pair(
        request.data['pick_pair_id'],
        request.data['choiced_video_id']
    )
    return Response(PickPairSerializer(updated_pair).data, status=HTTP_200_OK)
