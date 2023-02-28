from rest_framework import serializers

from .models import ExpiringLinks, Image, Thumbnail


class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        fields = ("path", "size")


class ImageBasicSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ("id", "original_image", "thumbnails")

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "thumbnails": ThumbnailSerializer(many=True, read_only=True).to_representation(
                instance.thumbnails
            ),
        }


class ImagePremiumSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ("id", "original_image", "thumbnails")

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "image": instance.original_image.name,
            "thumbnails": ThumbnailSerializer(many=True, read_only=True).to_representation(
                instance.thumbnails
            ),
        }

    def get_original_image(self, obj):
        if obj.original_image and hasattr(obj.original_image, "url"):
            return obj.original_image.url


class ImageEnterpriseSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ("id", "original_image", "thumbnails")

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "image": instance.original_image.name,
            "thumbnails": ThumbnailSerializer(many=True, read_only=True).to_representation(
                instance.thumbnails
            ),
        }

    def get_original_image(self, obj):
        if obj.original_image and hasattr(obj.original_image, "url"):
            return obj.original_image.url


class ImageCustomSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, read_only=True)

    class Meta:
        model = Image
        fields = ("id", "original_image", "thumbnails")

    def to_representation(self, instance):
        link_present = self.context['request'].user.account_tier.link_present
        if link_present:
            return {"id": instance.id, "thumbnails": ThumbnailSerializer(many=True, read_only=True).to_representation(
                instance.thumbnails), "link": instance.original_image.name}
        return {"id": instance.id, "thumbnails": ThumbnailSerializer(many=True, read_only=True).to_representation(
                instance.thumbnails)}

class ExpiringLinksSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExpiringLinks
        fields = ("id", "image", "seconds")

    def validate_image(self, image):
        user = self.context['request'].user
        if image.user != user:
            raise serializers.ValidationError('Selected image does not belong to you.')
        return image

    def create(self):
        return ExpiringLinks(**self.validated_data)
