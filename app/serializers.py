from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import services
from app import services as likes_services
from .models import Tweet

User = get_user_model()


class FanSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'full_name',
        )

    def get_full_name(self, obj):
        return obj.get_full_name()


class TweetSerializer(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = (
            'id',
            'body',
            'is_fan',
            'total_likes',
        )

    def get_is_fan(self, obj) -> bool:
        """Check if a `request.user` has liked this tweet (`obj`).
        """
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


