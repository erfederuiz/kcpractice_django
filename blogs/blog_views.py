from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from blogs import utils
from blogs.models import Blog, Post
from blogs.serializers import BlogSerializer, PostSerializer
from rest_framework.response import Response


class BlogListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blogs.html'
    serializer_class = BlogSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        categories = utils.get_all_visible_categories()
        auth = request.user.is_authenticated()
        return Response(
            {'blogs': Blog.objects.all(), 'user': auth, 'categories': categories, 'logged_in_user': request.user})


class BlogPostListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'post_list.html'
    serializer_class = PostSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, username, format=None):
        categories = utils.get_all_visible_categories()
        cat_slug = request.GET.get('cat', None)
        sort = request.GET.get('sort', None)
        auth = request.user.is_authenticated()

        posts = Post.objects.filter(blog__author__username=username)
        if request.user.username != username:
            posts = Post.objects.filter(is_published=True, blog__author__username=username)
        if cat_slug:
            posts = posts.filter(category__slug=cat_slug)
        if sort:
            posts = posts.order_by(sort)

        if not auth:
            posts = posts.filter(is_published=True)
        return Response({'posts': posts, 'user': auth, 'categories': categories, 'selected_cat': cat_slug,
                         'logged_in_user': request.user, 'blog': True})
