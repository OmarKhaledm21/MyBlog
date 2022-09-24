from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import View

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from .forms import CommentForm
from .models import Post
# Create your views here.


class IndexView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog_app/index.html"
    ordering = ["-date"]

    def get_queryset(self):
        qs = super().get_queryset()
        data = qs[:3]
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "home"
        return context


class PostView(View):
    def is_stored_post(self,request,post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        tags = post.tags.all() if post else None
        comments = post.comments.all().order_by("-id")
        if len(comments) == 0:
            comments = None

        context = {
            "post": post,
            "tags": tags,
            "comment_form": CommentForm,
            "comments": comments,
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog_app/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        comments = post.comments.all().order_by("-id")
        if len(comments) == 0:
            comments = None
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": comments,
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog_app/post-detail.html", context)


class AllPostsView(ListView):
    model = Post
    template_name = "blog_app/all-posts.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = "all_posts"
        return context


class StoredPostsView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {
            "current_page":"stored_posts"
        }


        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog_app/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        
        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")