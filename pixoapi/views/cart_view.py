from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pixoapi.models import Cart, CartItem, PixoUser, Collectible
from pixoapi.views.image_view import ImageSerializer
from django.http import HttpResponseServerError


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
        fields = ['cart', 'collectible', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source='users_cart')
    user = PixoUserCartSerializer(many=False)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'purchase_date', 'paid', 'items']


class CartView(ViewSet):

    def retrieve(self, request, pk):
        try:
            cart = Cart.objects.get(pk=pk)
            serializer = CartSerializer(cart, context={'request': request})
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):

        try:
            # user = PixoUser.objects.get(user=request.auth.user)
            carts = Cart.objects.get(user__user=request.auth.user, paid=False)
            serializer = CartSerializer(
                carts, many=False, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk)
            items = CartItem.objects.filter(cart__id=cart.id)
            cart.delete()
            items.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
