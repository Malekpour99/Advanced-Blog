from rest_framework import serializers
from blog.models import Post


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # don't use __all__ for fields (best practice)
        fields = [
            "id",
            "title",
            "content",
            "published",
            "published_date",
            "created_date",
        ]
