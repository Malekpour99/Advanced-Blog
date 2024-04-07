from rest_framework.decorators import api_view
from rest_framework.response import Response
from blog.models import Post
from .serializers import PostSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view(["GET", "POST"])
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.filter(published=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        # you must specify 'data' since is_valid() will look for it
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


# @api_view()
# def post_detail(request, id):
#     try:
#         post = Post.objects.get(pk=id)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#     except Post.DoesNotExist:
#         # return Response({"detail": "Post does not exist"}, status=404)
#         return Response(
#             {"detail": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND
#         )


# You can summarize above code like below:
@api_view()
def post_detail(request, id):
    post = get_object_or_404(Post, pk=id, published=True)
    serializer = PostSerializer(post)
    return Response(serializer.data)
