from rest_framework import serializers
from blog.models import Post, Category
from accounts.models import Profile


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
    relative_url = serializers.URLField(source="get_relative_api_url", read_only=True)
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
        read_only_fields = ["author"]

    # If your methods and fields depend on the user request define them here in the serializer
    # otherwise you can define them directly in your model class
    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("content", None)
        rep["category"] = CategorySerializer(instance.category).data
        return rep

    def create(self, validated_data):
        validated_data["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)
