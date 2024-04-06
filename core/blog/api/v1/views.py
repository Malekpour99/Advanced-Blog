from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog.models import Post
from .serializers import PostSerializer


@api_view()
def api_rest_view(request):
    return Response("ok")


@api_view()
def post_detail(request, id):
    try:
        post = Post.objects.get(pk=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({"detail": "Post does not exist"}, status=404)
