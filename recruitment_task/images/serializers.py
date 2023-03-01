from django.conf import settings
from rest_framework import serializers

from .models import ExpiringLinks, Image, Thumbnail


class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = ("path", "size")

    def to_representation(self, instance):
        thumbnail_path = instance.path[1:]
        host = self.context["request"].get_host()
        return {"path": f"{host}{thumbnail_path}", "size": instance.size}


class ImageSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ("id", "original_image", "thumbnails")


class ImageBasicSerializer(ImageSerializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "thumbnails": ThumbnailSerializer(
                many=True, read_only=True, context={"request": self.context.get("request")}
            ).to_representation(instance.thumbnails),
        }


class ImagePremiumSerializer(ImageSerializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "image": f"{self.context.get('request').get_host()}{settings.MEDIA_URL}{instance.original_image.name}",
            "thumbnails": ThumbnailSerializer(
                many=True, read_only=True, context={"request": self.context.get("request")}
            ).to_representation(instance.thumbnails),
        }


class ImageEnterpriseSerializer(ImageSerializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "image": f"{self.context.get('request').get_host()}{settings.MEDIA_URL}{instance.original_image.name}",
            "thumbnails": ThumbnailSerializer(
                many=True, read_only=True, context={"request": self.context.get("request")}
            ).to_representation(instance.thumbnails),
        }


class ImageCustomSerializer(ImageSerializer):
    def to_representation(self, instance):
        link_present = self.context["request"].user.account_tier.link_present
        if link_present:
            return {
                "id": instance.id,
                "thumbnails": ThumbnailSerializer(
                    many=True, read_only=True, context={"request": self.context.get("request")}
                ).to_representation(instance.thumbnails),
                "image": f"{self.context.get('request').get_host()}{settings.MEDIA_URL}{instance.original_image.name}",
            }
        return {
            "id": instance.id,
            "thumbnails": ThumbnailSerializer(many=True, read_only=True).to_representation(
                instance.thumbnails
            ),
        }


class ExpiringLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLinks
        fields = ("id", "image", "seconds")

    def validate_image(self, image):
        user = self.context["request"].user
        if image.user != user:
            raise serializers.ValidationError("Selected image does not belong to you.")
        return image

    def create(self):
        return ExpiringLinks(**self.validated_data)
