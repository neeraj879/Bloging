from django.urls import path
from .views import (
	home,
	about,
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	UserPostListView,
	PostDetail,
	CommentCreateView
	)

urlpatterns=[
path('',PostListView.as_view(),name="home"),
path('user/<str:username>',UserPostListView.as_view(),name="user_post_list"),
path('post/<int:pk>',PostDetail,name="post_detail"),
path('post/<int:pk>/update',PostUpdateView.as_view(),name="post_update"),
path('post/<int:pk>/delete',PostDeleteView.as_view(),name="post_delete"),
path('post/create',PostCreateView.as_view(),name="post_create"),
path('post/create',CommentCreateView.as_view(),name="post_create_"),
path('about/',about,name="about")
]