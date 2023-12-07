from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pixoapi.models import PixoUser


class UserPixoUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ['full_name', 'username']


class PixoUserSerializer(serializers.ModelSerializer):
    user = UserPixoUserSerializer(many=False)

    class Meta:
        model = PixoUser
        fields = ['id', 'user', 'bio', 'location', 'img_url']


class PixoUserView(ViewSet):

    def retrieve(self, request, pk):
        try:
            pixouser = PixoUser.objects.get(pk=pk)
            serializer = PixoUserSerializer(
                pixouser, context={'request': request})
            return Response(serializer.data)
        except PixoUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        pixouser = PixoUser.objects.all()
        serializer = PixoUserSerializer(
            pixouser, many=True, context={'request': request})
        return Response(serializer.data)
