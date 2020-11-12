from . import views
from django.urls import path

app_name = 'userpost'

urlpatterns = [
    path('', views.Postslist.as_view(), name='all_posts'),
    path('addcomment/', views.add_comment),
    path('add/', views.Addpost.as_view(), name='add_post'),
    path('<slug:username>/', views.UserPosts.as_view(), name='user_posts'),
    path('<slug:username>/<int:id>/<slug:post>/', views.Showpost.as_view(), name='post'),
    path('tags/<slug:tag>/', views.TaggedPost.as_view(), name='tag'),
]
