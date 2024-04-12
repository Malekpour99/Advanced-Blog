from rest_framework import serializers
from blog.models import Post, Category


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")

    class Meta:
        model = Post
        # don't use __all__ for fields (best practice)
        fields = [
            "id",
            "author",
            "title",
            "content",
            "snippet",
            "published",
            "published_date",
            "created_date",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # don't use __all__ for fields (best practice)
        fields = ["id", "name"]
