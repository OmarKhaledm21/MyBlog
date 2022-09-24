from django.urls import path
from .views import IndexView, PostView, AllPostsView, StoredPostsView
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('posts',AllPostsView.as_view(),name='all-posts'),
    path('stored-posts',StoredPostsView.as_view(),name='stored-posts'),
    path('post/<slug:slug>', PostView.as_view(), name='post-detail-page')
]
