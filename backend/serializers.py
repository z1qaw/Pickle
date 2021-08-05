from rest_framework.serializers import ModelSerializer

from .models import PickPair, PickSession, PickSessionRound, YoutubeVideo


class YoutubeVideoSerializer(ModelSerializer):
    class Meta:
        model = YoutubeVideo
        fields = '__all__'


class PickPairSerializer(ModelSerializer):
    class Meta:
        model = PickPair
        fields = '__all__'


class PickSessionDetailsSerializer(ModelSerializer):
    class Meta:
        model = PickSession
        fields = '__all__'
        depth = 1

class PickSessionRoundDetailsSerializer(ModelSerializer):
    class Meta:
        model = PickSessionRound
        fields = '__all__'
        depth = 2
