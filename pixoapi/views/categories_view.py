
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from pixoapi.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label']


class CategoryView(ViewSet):
    def retrieve(self, request, pk):
        try:
            cat = Category.objects.get(pk=pk)
            serializer = CategorySerializer(
                cat, context={'request': request})
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        cat = Category.objects.all()
        serializer = CategorySerializer(
            cat, many=True, context={'request': request})
        return Response(serializer.data)
