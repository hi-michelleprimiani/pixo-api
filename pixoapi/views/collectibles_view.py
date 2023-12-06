from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pixoapi.models import Collectible, Image, Category


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['img_url']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']


class CollectibleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CollectiblePixoUserSerializer(serializers.ModelSerializer):
    user = CollectibleUserSerializer(many=False)

    class Meta:
        model = User
        fields = ['user']


class CollectibleSerializer(serializers.ModelSerializer):
    seller = CollectiblePixoUserSerializer(many=False)
    images = ImageSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Collectible
        fields = ['id', 'seller', 'name', 'description',
                  'price', 'material', 'color', 'size', 'created_date', 'images', 'categories']


class CollectibleView(ViewSet):

    def retrieve(self, request, pk):
        try:
            collectible = Collectible.objects.get(pk=pk)
            serializer = CollectibleSerializer(
                collectible, context={'request': request})
            return Response(serializer.data)
        except Collectible.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        # Get the query parameter 'user' from the request
        user_param = request.query_params.get('user')

        if user_param == 'current':
            # If user_param is 'current', filter posts by the current user ID
            try:
                user_id = request.seller.id
                collectible = Collectible.objects.filter(
                    user__user__id=user_id)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # If no 'user' parameter or 'user' is not 'current', return all posts
            collectible = Collectible.objects.all()

        serializer = CollectibleSerializer(collectible, many=True)
        return Response(serializer.data)
