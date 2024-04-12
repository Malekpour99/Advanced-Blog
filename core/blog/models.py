from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# To get User model object: use USER_AUTH_MODEL from settings
# or import User model directly from accounts app
# but below way is more efficient since it's more dynamic
User = get_user_model()


# Create your models here.
class Post(models.Model):
    """
    This is a class for defining posts in the blog app
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog/", null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    published = models.BooleanField()
    published_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ["-created_date"]

    def __str__(self):
        return f"{self.title} - {self.id}"

    def get_snippet(self):
        return self.content[0:10]


class Category(models.Model):
    """
    This is a class for defining categories for blog posts
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
