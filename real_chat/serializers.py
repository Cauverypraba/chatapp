# from django.contrib.auth.models import User
from rest_framework import serializers
from real_chat.models import user, FriendList, Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = user
        fields = ['name', 'password', 'email', 'mobile_number', 'profile_pic', 'created_date']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='name', queryset=user.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='name', queryset=user.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
