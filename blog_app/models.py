from django.db import models
from django.core.validators import MinLengthValidator

from django.urls import reverse
# Create your models here.


class Tags(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.caption}"


class Author(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"Author: {self.full_name()} Email: {self.email}"


class Post(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True, null=False)
    excerpt = models.TextField(blank=True, default="")
    content = models.TextField(validators=[MinLengthValidator(10)])

    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name='posts')

    tags = models.ManyToManyField(Tags, related_name="tags")

    def __str__(self) -> str:
        return f"Title: {self.title}, Date: {self.date}, Slug: {self.slug}"

    def get_absolute_url(self):
        return reverse("post-detail-page", args=[self.slug])


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
