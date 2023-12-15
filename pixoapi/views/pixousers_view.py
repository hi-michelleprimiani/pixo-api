from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pixoapi.models import PixoUser, Collectible, Category
from pixoapi.views.collectibles_view import CollectibleSerializer, CollectiblePixoUserSerializer
from pixoapi.views.cart_view import CartSerializer
from pixoapi.views.image_view import ImageSerializer


class UserPixoUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ['full_name', 'username']


class PixoCollectibleSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Collectible
        fields = ['id', 'name', 'description',
                  'price', 'material', 'color', 'size', 'created_date', 'images', 'categories']


class PixoUserSerializer(serializers.ModelSerializer):
    user = UserPixoUserSerializer(many=False)
    collectible = PixoCollectibleSerializer(
        many=True, source="seller_collectibles")
    carts = CartSerializer(many=True, read_only=True)

    class Meta:
        model = PixoUser
        fields = ['id', 'user', 'bio', 'location',
                  'img_url', 'collectible', 'carts']


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
