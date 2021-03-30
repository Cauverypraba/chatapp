# from django.contrib.auth.models import User
from rest_framework import serializers
from real_chat.models import user, FriendList, Message


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=200, required=True)
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = user
        fields = ['name', 'password', 'email', 'mobile_number', 'created_date']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='name', queryset=user.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='name', queryset=user.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
