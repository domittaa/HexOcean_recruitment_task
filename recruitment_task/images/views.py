import datetime
import uuid
from pathlib import Path

from django.http import FileResponse, Http404
from django.utils import timezone
from PIL import Image as PILImage
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import ExpiringLinks, Image, Thumbnail
from .serializers import (
    ExpiringLinksSerializer,
    ImageBasicSerializer,
    ImageCustomSerializer,
    ImageEnterpriseSerializer,
    ImagePremiumSerializer,
)


class ImageCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        user = self.request.user
        if user.account_tier.name == "Basic":
            return ImageBasicSerializer
        if user.account_tier.name == "Premium":
            return ImagePremiumSerializer
        if user.account_tier.name == "Enterprise":
            return ImageEnterpriseSerializer
        return ImageCustomSerializer

    def perform_create(self, serializer):
        user = self.request.user
        account_tier = user.account_tier
        thumbnail_sizes = account_tier.thumbnail_sizes.split(",")
        thumbnail_sizes = [int(size.strip()) for size in thumbnail_sizes]

        image = serializer.save(user=user)

        for size in thumbnail_sizes:
            self.create_thumbnail(image, size)

        if account_tier.link_present:
            image.original_image = image.original_image

        image.save()

    @staticmethod
    def create_thumbnail(image, size):
        thumbnail_image = PILImage.open(image.original_image)
        thumbnail_image.thumbnail((size, size))
        fmt = Path(image.original_image.name).suffix
        path = f"./media/thumbnails/{image.id}/{size}{fmt}"
        Path(f"./media/thumbnails/{image.id}").mkdir(exist_ok=True, parents=True)
        thumbnail_image.save(path)
        thumbnail_obj = Thumbnail(path=path, size=size, image=image)

        thumbnail_obj.save()
        return thumbnail_obj


class ImageListApiView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        user = self.request.user
        if user.account_tier.name == "Basic":
            return ImageBasicSerializer
        if user.account_tier.name == "Premium":
            return ImagePremiumSerializer
        if user.account_tier.name == "Enterprise":
            return ImageEnterpriseSerializer
        return ImageCustomSerializer

    def get_queryset(self):
        images = Image.objects.filter(user=self.request.user).all()
        return images


class ExpiringLinkCreateApiView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ExpiringLinksSerializer

    def create(self, request, *args, **kwargs):
        if not self.request.user.account_tier.allow_expiring_link:
            raise PermissionDenied
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        link = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            "link": request.build_absolute_uri(f"/links/get_by_code/{link.code}"),
            "expiration_date": link.time,
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        link = serializer.create()
        link.code = uuid.uuid4().hex
        link.time = datetime.datetime.now() + datetime.timedelta(seconds=serializer.data["seconds"])
        link.save()
        return link


class ExpiringLinkRetrieveApiView(generics.RetrieveAPIView):
    queryset = ExpiringLinks.objects.all()
    lookup_field = "code"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.time < timezone.now():
            raise Http404
        image_file = instance.image.original_image
        fmt = Path(image_file.name).suffix[1:]
        response = FileResponse(image_file, content_type=f"image/{fmt}")
        response["Content-Disposition"] = f'attachment; filename="{instance.code}.{fmt}"'
        return response
