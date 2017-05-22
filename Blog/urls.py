"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from blogs import end_point_views
from blogs.blog_views import BlogListView, BlogPostListView
from blogs.views import UserRegisterView, UserLoginView, AddPostView, PostListView, PostDetails, UpdateDeletePost, \
    LogOutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^register_user/$', UserRegisterView.as_view(), name='register-user'),
                  url(r'^login/$', UserLoginView.as_view(), name='login'),
                  url(r'^add_post/$', AddPostView.as_view(), name='add_post'),
                  url(r'^$', PostListView.as_view(), name='post_list'),
                  url(r'^update/(?P<slug>[^/]+)/post/$', UpdateDeletePost.as_view(), name='update-post'),

                  url(r'^post/(?P<slug>[^/]+)/details$', PostDetails.as_view(), name='post-details'),
                  url(r'^logout/$', LogOutView.as_view(), name='logout'),
                  url(r'^blog/$', BlogListView.as_view(), name='blog-list'),
                  url(r'^blog/(?P<username>[^/]+)/posts$', BlogPostListView.as_view(), name='blog-post-details'),
                  # url(r'^login/$', UserLoginView.as_view(), name='login'),

                  url(r'^end_point/post/(?P<slug>[^/]+)/details$', end_point_views.PostDetails.as_view(),
                      name='end-post-details'),
                  url(r'^end_point/post_list/$', end_point_views.PostListView.as_view(), name='end-post-list'),
                  url(r'^end_point/add_post/$', end_point_views.AddPostView.as_view(), name='end-add_post'),
                  url(r'^end_point/blogs/$', end_point_views.BlogListView.as_view(), name='end-blog-list'),
                  url(r'^end_point/update/(?P<slug>[^/]+)/post/$', end_point_views.UpdateDeletePost.as_view(),
                      name='end-update-post'),
                  url(r'^end_point/blog/(?P<username>[^/]+)/posts$', end_point_views.BlogPostListView.as_view(),
                      name='end-blog-post-details'),
                  url(r'^end_point/register_user/$', end_point_views.UserRegisterView.as_view(),
                      name='end-register-user'),
                  url(r'^end_point/update_delete/$', end_point_views.UserProfileView.as_view(),
                      name='end-update-delete-user'),
                  url(r'^end_point/login/$', end_point_views.UserLoginView.as_view(), name='end-login'),
                  url(r'^end_point/categories/$', end_point_views.CategoriesView.as_view(), name='end-login'),
                  url(r'^end_point/check_user/(?P<username>[^/]+)$', end_point_views.CheckUserView.as_view(),
                      name='end-login'),

                  url(r'^end_point/delete_user/(?P<username>[^/]+)$', end_point_views.DeleteUserView.as_view(),
                      name='delete-user'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
