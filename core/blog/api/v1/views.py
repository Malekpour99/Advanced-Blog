from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import mixins
from rest_framework import viewsets
from blog.models import Post
from .serializers import PostSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


# Function Based Views --------------------------------
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.filter(published=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # you must specify 'data' since is_valid() will look for it
        serializer = PostSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


"""@api_view()
def post_detail(request, id):
    try:
        post = Post.objects.get(pk=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        # return Response({"detail": "Post does not exist"}, status=404)
        return Response(
            {"detail": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND
        )"""


# You can summarize above code like below:
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminUser])
def post_detail(request, id):
    post = get_object_or_404(Post, pk=id, published=True)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        post.delete()
        return Response(
            {"detail": "Item removed successfully."}, status=status.HTTP_204_NO_CONTENT
        )


# Class Based Views --------------------------------
'''class PostList(APIView):
    """Retrieving and creating posts"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request):
        """Get a list of posts"""
        posts = Post.objects.filter(published=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new post from provided data"""
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)'''


'''class PostList(GenericAPIView):
    """Retrieving and creating posts"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published=True)

    def get(self, request):
        """Get a list of posts"""
        # You must call get_queryset() when overriding a method since queryset is cached
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new post from provided data"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)'''


'''class PostList(GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Retrieving and creating posts"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published=True)

    def get(self, request, *args, **kwargs):
        """Get a list of posts"""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create a new post from provided data"""
        return self.create(request, *args, **kwargs)'''


class PostList(ListCreateAPIView):
    """Retrieving and creating posts"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published=True)


'''class PostSingle(APIView):
    """Retrieving, Updating and Deleting a single post"""

    permission_classes = [IsAdminUser]
    serializer_class = PostSerializer

    def get(self, request, id):
        """Retrieve a single post"""
        post = get_object_or_404(Post, pk=id, published=True)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def put(self, request, id):
        """Edit/Update a single post"""
        post = get_object_or_404(Post, pk=id, published=True)
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        """Delete a single post"""
        post = get_object_or_404(Post, pk=id, published=True)
        post.delete()
        return Response(
            {"detail": "Item removed successfully."}, status=status.HTTP_204_NO_CONTENT
        )'''


'''class PostSingle(
    GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """Retrieving, Updating and Deleting a single post"""

    permission_classes = [IsAdminUser]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published=True)
    # we changed 'id' to 'pk' for retrieving post object but if
    # you want to use a different field override the 'lookup_field' attribute

    def get(self, request, *args, **kwargs):
        """Retrieve a single post"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Edit/Update a single post"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete a single post"""
        return self.destroy(request, *args, **kwargs)'''


class PostSingle(RetrieveUpdateDestroyAPIView):
    """Retrieving, Updating and Deleting a single post"""

    permission_classes = [IsAdminUser]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published=True)


class PostViewSet(viewsets.ViewSet):
    """
    Retrieving posts and creating a post \n
    Retrieving, Updating and Deleting a single post
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published=True)

    def list(self, request):
        """Returning a list of posts"""
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Creating a new post"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Retrieving a single post"""
        post_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post_object)
        return Response(serializer.data)

    def update(self, request, pk):
        """Updating a single post completely"""
        post_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post_object, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk):
        """Updating a single post Partially"""
        post_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post_object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Deleting a single post"""
        post_object = get_object_or_404(self.queryset, pk=pk)
        post_object.delete()
        return Response(
            {"detail": "Item removed successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class PostModelViewSet(viewsets.ModelViewSet):
    """
    Retrieving posts and creating a post \n
    Retrieving, Updating and Deleting a single post
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(published=True)
