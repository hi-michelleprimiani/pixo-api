from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from pixoapi.models import Message, PixoUser


class UserMessagesSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ['full_name', 'username']


class PixoUserMessagesSerializer(serializers.ModelSerializer):
    user = UserMessagesSerializer(many=False)

    class Meta:
        model = PixoUser
        fields = ['id', 'user', 'img_url']


class MessageSerializer(serializers.ModelSerializer):
    sender = PixoUserMessagesSerializer(many=False)
    receiver = PixoUserMessagesSerializer(many=False)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'text', 'date_time']


class MessagesView(ViewSet):

    def list(self, request):
        sent_messages = Message.objects.filter(sender__user=request.user)
        received_messages = Message.objects.filter(receiver__user=request.user)
        messages = sent_messages | received_messages
        # Sort the messages if needed (e.g., by date)
        messages = messages.order_by('-date_time')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
