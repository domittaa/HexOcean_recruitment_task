from rest_framework import serializers
from .models import Image, Tier


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'user', 'image', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

    def get_original_image(self, obj):
        return obj.image.url


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = ('name', 'thumbnail_size', 'link_present', 'allow_expiring_link', 'expiring_link_expiration')
