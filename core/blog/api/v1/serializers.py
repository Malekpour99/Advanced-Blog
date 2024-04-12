from rest_framework import serializers
from blog.models import Post, Category


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_relative_api_url")

    class Meta:
        model = Post
        # don't use __all__ for fields (best practice)
        fields = [
            "id",
            "author",
            "title",
            "content",
            "snippet",
            "relative_url",
            "published",
            "published_date",
            "created_date",
        ]

    # If your methods and fields depend on the user request define them here in the serializer
    # otherwise you can define them directly in your model class


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # don't use __all__ for fields (best practice)
        fields = ["id", "name"]
