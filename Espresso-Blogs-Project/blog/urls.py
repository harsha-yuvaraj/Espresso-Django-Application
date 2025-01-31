from django.urls import path
from . import views
from .feeds import LatestPostsFeed

# define application namespace
app_name = 'blog'

urlpatterns = [
    # post views
    path('',views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # SEO friendly - for post detail view
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
         views.post_detail, 
         name='post_detail'
        ),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    path('api/generate_summary', views.generate_post_summary, name='generate_post_summary'),
]
