from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
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
        # Combine the querysets of sent and received messages.
        # This will include all messages where the user is either the sender or the receiver.
        messages = sent_messages | received_messages
        # Sort the messages if needed (e.g., by date)
        messages = messages.order_by('date_time')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request):

        sender = PixoUser.objects.get(user=request.auth.user)
        receiver = PixoUser.objects.get(pk=request.data["receiver"])
        m = Message()
        m.sender = sender
        m.receiver = receiver
        m.text = request.data.get('text')
        m.date_time = request.data.get('date_time')
        m.save()

        try:
            serializer = MessageSerializer(m, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            message = Message.objects.get(pk=pk)
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
