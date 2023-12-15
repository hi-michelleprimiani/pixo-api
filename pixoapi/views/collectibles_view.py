from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pixoapi.models import Collectible, Image, PixoUser, ImageGallery, Category
from pixoapi.views.image_view import ImageSerializer
# from pixoapi.views.categories_view import CategorySerializer


class CollectibleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class CollectiblePixoUserSerializer(serializers.ModelSerializer):
    user = CollectibleUserSerializer(many=False)

    class Meta:
        model = PixoUser
        fields = ['id', 'user', 'img_url', 'bio', 'location']


class CollectibleSerializer(serializers.ModelSerializer):
    seller = CollectiblePixoUserSerializer(many=False)
    images = ImageSerializer(many=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )

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

        collectible = Collectible.objects.all()
        serializer = CollectibleSerializer(collectible, many=True)
        return Response(serializer.data)

    def create(self, request):

        seller = PixoUser.objects.get(user=request.auth.user)
        c = Collectible()
        c.seller = seller
        c.name = request.data.get('name')
        c.description = request.data.get('description')
        c.price = request.data.get('price')
        c.material = request.data.get('material')
        c.color = request.data.get('color')
        c.size = request.data.get('size')
        c.save()

        image_data = request.data.get('images', [])
        image_ids = []
        for image in image_data:
            i = Image()
            i.img_url = image.get('img_url')
            i.save()
            image_ids.append(i.id)
        c.images.set(image_ids)

        category_data = request.data.get('categories', [])
        c.categories.set(category_data)

        try:
            serializer = CollectibleSerializer(c, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            collectible = Collectible.objects.get(pk=pk)

            serializer = CollectibleSerializer(
                collectible, data=request.data, partial=True)
            if serializer.is_valid():
                collectible.name = serializer.validated_data.get(
                    'name', collectible.name)
                collectible.description = serializer.validated_data.get(
                    'description', collectible.description)
                collectible.price = serializer.validated_data.get(
                    'price', collectible.price)
                collectible.material = serializer.validated_data.get(
                    'material', collectible.material)
                collectible.color = serializer.validated_data.get(
                    'color', collectible.color)
                collectible.size = serializer.validated_data.get(
                    'size', collectible.size)

                collectible.save()

                # Handling images update
                # Delete old ImageGallery entries
                ImageGallery.objects.filter(collectible=collectible).delete()

                # Create new images and ImageGallery entries
                images_data = request.data.get('images', [])
                for image_data in images_data:
                    new_image = Image.objects.create(
                        img_url=image_data.get('img_url'))
                    ImageGallery.objects.create(
                        collectible=collectible, image=new_image)

                # Handling categories update
                category_data = request.data.get('categories', [])
                collectible.categories.set(category_data)

                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Collectible.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            collectible = Collectible.objects.get(pk=pk)
            images = ImageGallery.objects.filter(
                collectible__id=collectible.id)
            collectible.delete()
            images.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Collectible.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
