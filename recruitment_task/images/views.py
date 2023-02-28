from rest_framework import generics, permissions
from .models import Image
from .serializers import ImageSerializer


class ImageCreateAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImageListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)
