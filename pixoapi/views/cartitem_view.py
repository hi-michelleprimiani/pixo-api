from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pixoapi.models import Cart, CartItem, Collectible, PixoUser


class CollectibleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collectible
        fields = ['id', 'name',
                  'price']


class CartItemSerializer(serializers.ModelSerializer):
    collectible = CollectibleSerializer(many=False)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'collectible', 'quantity']


class CartItemView(ViewSet):

    def retrieve(self, request, pk):
        try:
            cartitem = CartItem.objects.get(pk=pk)
            serializer = CartItemSerializer(
                cartitem, context={'request': request})
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):

        cartitem = CartItem.objects.all()
        serializer = CartItemSerializer(cartitem, many=True)
        return Response(serializer.data)

    def create(self, request):

        user = PixoUser.objects.get(user=request.auth.user)
        try:
            cart = Cart.objects.get(user=user, paid=False)
        except Cart.DoesNotExist:
            cart = Cart()
            cart.user = user
            cart.save()

        collectible = Collectible.objects.get(pk=request.data['collectible'])
        user = PixoUser.objects.get(user=request.auth.user)
        cartitem = CartItem()
        cartitem.user = user
        cartitem.cart = cart
        cartitem.collectible = collectible
        cartitem.quantity = request.data.get('quantity')
        cartitem.save()

        try:
            serializer = CartItemSerializer(cartitem, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            cartitem = CartItem.objects.get(pk=pk)
            cartitem.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
