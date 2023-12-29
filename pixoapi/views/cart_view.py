from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.http import HttpResponseServerError
from pixoapi.models import Cart, CartItem, PixoUser, Collectible
from pixoapi.views.image_view import ImageSerializer
from datetime import datetime
from django.utils.timezone import localtime


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

    def validate_paid(self, value):
        """
        Check that the paid field is not being set to False if it's already True.
        """
        if self.instance and self.instance.paid and not value:
            raise serializers.ValidationError("Cannot unset a cart as unpaid.")
        return value

    def validate_purchase_date(self, value):
        """
        Ensure the purchase date is not set in the future.
        """
        if value > datetime.datetime.now():
            raise serializers.ValidationError(
                "Purchase date cannot be in the future.")
        return value


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
        is_paid = request.query_params.get('paid', 'False').lower() in [
            'true', '1', 'yes']

        try:
            if is_paid:
                carts = Cart.objects.filter(
                    user__user=request.auth.user, paid=True)
                serializer = CartSerializer(
                    carts, many=True, context={"request": request})
            else:
                cart = Cart.objects.get(
                    user__user=request.auth.user, paid=False)
                serializer = CartSerializer(
                    cart, many=False, context={"request": request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        try:
            # Retrieve the cart object
            cart = Cart.objects.get(pk=pk)

            # Create a serializer instance with the retrieved cart and new data
            serializer = CartSerializer(cart, data=request.data, partial=True)

            # Validate the data
            if serializer.is_valid():
                if serializer.validated_data.get('paid', False):
                    cart.purchase_date = datetime.now()  # Set the purchase date
                serializer.save()

                # Return a successful response with the updated data
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # If the data is not valid, return an error response
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Cart.DoesNotExist:
            # If the cart does not exist, return a not found response
            return Response(status=status.HTTP_404_NOT_FOUND)

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
