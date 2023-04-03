from rest_framework import serializers


class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return {'name': obj.name,
                'slug': obj.slug}
