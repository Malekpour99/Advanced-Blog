from rest_framework import serializers
from blog.models import Post, Category


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # don't use __all__ for fields (best practice)
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_relative_api_url")
    absolute_url = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(
    #     many=False, slug_field="name", queryset=Category.objects.all()
    # )
    # category = CategorySerializer()

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
            "absolute_url",
            "category",
            "published",
            "published_date",
            "created_date",
        ]

    # If your methods and fields depend on the user request define them here in the serializer
    # otherwise you can define them directly in your model class
    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["category"] = CategorySerializer(instance.category).data
        return rep
