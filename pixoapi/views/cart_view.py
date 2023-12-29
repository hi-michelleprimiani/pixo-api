from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.http import HttpResponseServerError
from pixoapi.models import Cart, CartItem, PixoUser, Collectible
from pixoapi.views.image_view import ImageSerializer


class UserCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PixoUserCartSerializer(serializers.ModelSerializer):
    user = UserCartSerializer(many=False)

    class Meta:
        model = PixoUser
        fields = ['id', 'user']


class CartCollectibleSerializer(serializers.ModelSerializer):
    seller = PixoUserCartSerializer(many=False)
    images = ImageSerializer(many=True)

    class Meta:
        model = Collectible
        fields = ['id', 'name', 'price', 'images', 'seller']


class CartItemSerializer(serializers.ModelSerializer):
    collectible = CartCollectibleSerializer(many=False)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'collectible', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source='users_cart')
    user = PixoUserCartSerializer(many=False)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'purchase_date', 'paid', 'items']


class CartView(ViewSet):

    def retrieve(self, request, pk):
        """
        Retrieve a specific Cart object based on its primary key (pk).

        This method handles the retrieval of a Cart object from the database
        based on the provided primary key.

        Parameters:
        request (HttpRequest): The HTTP request object that carries data like
                            headers, method type, and user information.
        pk (int): The primary key of the Cart object to be retrieved.

        Returns:
        Response: An HttpResponse object. If the Cart object is found, the response
                contains the serialized Cart data. If not found, it returns a
                404 Not Found status.
        """
        try:
            cart = Cart.objects.get(pk=pk)
            serializer = CartSerializer(cart, context={'request': request})
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """
        Retrieve the current unpaid cart for the authenticated user.

        This method fetches the cart associated with the authenticated user that has not yet been paid for.
        It serializes the cart data and returns it. In case of any exception, an HTTP server error is returned.

        Parameters:
        request (HttpRequest): The HTTP request object with user authentication details.

        Returns:
        Response: Serialized cart data with HTTP 200 OK, or HTTP server error in case of exceptions.
        """

        try:
            # Fetches the Cart object associated with the authenticated user that has not been paid for yet.
            # 'user__user' is used to navigate through the related user model to the actual User model.
            carts = Cart.objects.get(user__user=request.auth.user, paid=False)
            serializer = CartSerializer(
                carts, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """
        Delete a specific cart and its items based on the cart's primary key.

        This method deletes the cart identified by the primary key and all associated cart items.
        If the cart is not found, it returns a 404 Not Found response.

        Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int, optional): The primary key of the cart to be deleted.

        Returns:
        Response: HTTP 204 No Content on successful deletion, or HTTP 404 Not Found if the cart does not exist.
        """
        try:
            cart = Cart.objects.get(pk=pk)
            items = CartItem.objects.filter(cart__id=cart.id)
            cart.delete()
            items.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
