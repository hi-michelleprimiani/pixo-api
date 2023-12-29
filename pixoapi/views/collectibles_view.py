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
        """
        Retrieve a specific Collectible by its primary key.

        Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the Collectible to retrieve.

        Returns:
        Response: Serialized Collectible data or 404 Not Found if it doesn't exist.
        """
        try:
            collectible = Collectible.objects.get(pk=pk)
            serializer = CollectibleSerializer(
                collectible, context={'request': request})
            return Response(serializer.data)
        except Collectible.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        List all Collectibles.

        Parameters:
        request (HttpRequest): The HTTP request object.

        Returns:
        Response: List of serialized Collectible data.
        """

        collectible = Collectible.objects.all()
        serializer = CollectibleSerializer(collectible, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new Collectible using the request data, including its associated images and categories.

        This method extracts data from the request, including the authenticated user's details, and uses 
        it to create a new Collectible object. It handles the setting of various attributes like name, 
        description, price, material, color, and size. It also processes and associates images and categories 
        with the newly created Collectible. If any exception occurs during creation, a detailed error 
        response is returned.

        Parameters:
        request (HttpRequest): The HTTP request object containing Collectible data.

        Returns:
        Response: Serialized data of the created Collectible or 404 Not Found on error.
        """

        # Retrieve the seller's information based on the authenticated user.
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
        # initialize a list to store image Id's
        image_ids = []
        for image in image_data:
            i = Image()
            i.img_url = image.get('img_url')
            i.save()
            image_ids.append(i.id)
        # Associate the images with the Collectible.
        c.images.set(image_ids)

        category_data = request.data.get('categories', [])
        c.categories.set(category_data)

        try:
            serializer = CollectibleSerializer(c, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Handle exceptions and return a 404 response with error details.
            # Convert the exception to a string and put it in a dictionary.
            error_message = {'error': str(e)}
            return Response(error_message, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """
        Update an existing Collectible identified by the primary key based on the provided request data.

        This method retrieves a Collectible based on the provided primary key and updates its attributes 
        with the data sent in the request. It allows partial updates to fields like name, description, price, 
        material, color, and size. The method also handles the updating of associated images and categories, 
        including the deletion of old images and addition of new ones. It checks for data validity before 
        saving changes. If the specified Collectible is not found or if the data is invalid, appropriate 
        error responses are returned.

        Parameters:
        request (HttpRequest): The HTTP request object with updated data for the Collectible.
        pk (int, optional): Primary key of the Collectible to update.

        Returns:
        Response: Serialized updated Collectible data with HTTP 204 status on successful update, 
                HTTP 400 Bad Request if data is invalid, or HTTP 404 Not Found if the Collectible doesn't exist.
        """
        try:
            collectible = Collectible.objects.get(pk=pk)

            # Initialize the serializer with the retrieved object and incoming data.
            # 'partial=True' allows partial update of the object fields.
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

                # Delete existing ImageGallery entries related to this collectible.
                ImageGallery.objects.filter(collectible=collectible).delete()

                # Create new images and ImageGallery entries
                images_data = request.data.get('images', [])
                for image_data in images_data:
                    new_image = Image.objects.create(
                        img_url=image_data.get('img_url'))
                    ImageGallery.objects.create(
                        collectible=collectible, image=new_image)

                # Handling categories update associated with collectible
                category_data = request.data.get('categories', [])
                collectible.categories.set(category_data)

                # Return the updated collectible
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

            # If the data is not valid, return 404
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If the collectible does not exist, return 404
        except Collectible.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """
        Delete a Collectible and its related images identified by the primary key.

        Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int, optional): Primary key of the Collectible to delete.

        Returns:
        Response: 204 No Content on successful deletion or 404 Not Found if not found.
        """
        try:
            collectible = Collectible.objects.get(pk=pk)
            images = ImageGallery.objects.filter(
                collectible__id=collectible.id)
            collectible.delete()
            images.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Collectible.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
