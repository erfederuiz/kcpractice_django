from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.contrib import messages

from blogs import utils
from blogs.serializers import UserSerializer, LoginSerializer, PostSerializer, CategorySerializer, BlogPostSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from blogs.models import Blog, Post, Category
from blogs.serializers import BlogSerializer, PostSerializer
from rest_framework.response import Response


class UserRegisterView(APIView):
    serializer_class = UserSerializer

    def get(self, request, format=None):
        users = UserSerializer()
        return Response(users.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

        # return Response(content)


class UserLoginView(APIView):
    serializer_class = LoginSerializer

    def auth_user(self, request, username, password):
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return True

        else:
            return False

    def get(self, request, format=None):
        users = LoginSerializer()
        return Response(users.data)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.POST)
        if serializer.is_valid():
            status = self.auth_user(request, serializer.validated_data['username'],
                                    serializer.validated_data['password'])
            if status:
                return Response(serializer.data)
        return Response(serializer.errors)


class UserProfileView(APIView):
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        users = UserSerializer(request.user)
        return Response({'serializer': users.data})

    def put(self, request, format=None):
        user = utils.update_user(request.user, request.data)
        return Response(UserSerializer(user).data)

    def delete(self, request, format=None):
        user = request.user
        User.objects.filter(id=user.id).delete()
        return Response("successfully removed")


class PostListView(APIView):
    serializer_class = PostSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, format=None):
        # categories = utils.get_all_visible_categories()
        cat_slug = request.GET.get('cat', None)
        sort = request.GET.get('sort', None)
        # auth = request.user.is_authenticated()
        posts = Post.objects.filter(is_published=True).order_by('-posted_at')
        if cat_slug:
            posts = posts.filter(category__slug=cat_slug)
        if sort:
            if sort == 'posted_at':
                sort = "-" + sort
            posts = posts.order_by(sort)

        posts = PostSerializer(posts, many=True).data
        return Response(posts)


class AddPostView(APIView):
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser,)

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        post = PostSerializer(Post.objects.all(), many=True).data
        return Response(post)

    def post(self, request, format=None):
        post = PostSerializer(data=request.data,
                              context={'user_id': request.user.id, 'request': request,
                                       'category': request.POST.getlist('category')})
        if post.is_valid():
            post.save()
            return Response(post.data)
        return Response(post.errors)


class PostDetails(APIView):
    serializer_class = PostSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_object(self, slug, request):
        try:
            post = Post.objects.get(slug=slug)
            if not post.is_published and post.blog.author != request.user:
                raise Http404
        except Post.DoesNotExist:
            raise Http404
        return post

    def get(self, request, slug):
        post = PostSerializer(self.get_object(slug, request), many=False,
                              context={'request': request, 'user_id': request.user.id}).data
        return Response(post)


class UpdateDeletePost(APIView):
    serializer_class = PostSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_object(self, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        post_data = self.get_object(slug)
        if post_data.blog.author != request.user:
            return Http404
        post = PostSerializer(post_data, many=False, context={'request': request})
        return Response(post.data)

    def post(self, request, slug, format=None):
        post_data = self.get_object(slug)
        if post_data.blog.author != request.user:
            return Http404
        category_ids = request.POST.getlist('category')
        if not request.POST.getlist('category'):
            category_ids = [0]
        post = utils.update_post(post_data, request.data, category_ids)

        return Response(PostSerializer(post).data)

    def delete(self, request, slug):
        post = self.get_object(slug)
        if post.blog.author != request.user and not request.user.is_superuser:
            return Http404
        post.delete()
        return Response("Post Deleted")


class LogOutView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = PostSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return redirect('post_list')


class BlogListView(APIView):
    serializer_class = BlogSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, format=None):
        blogs = BlogSerializer(Blog.objects.all(), many=True).data
        return Response(blogs)


class BlogPostListView(APIView):
    serializer_class = BlogPostSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, username, format=None):
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
        posts = BlogPostSerializer(posts, many=True).data
        return Response(posts)


class CategoriesView(APIView):
    serializer_class = CategorySerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, format=None):
        categories = Category.objects.filter(hidden=False)
        cats = CategorySerializer(categories, many=True).data
        return Response(cats)


class CheckUserView(APIView):
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self, request, username, format=None):
        if not request.user.is_superuser:
            return Response("only admin can perform this stuff")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response("User Does not exist")
        user_serializer = UserSerializer(user).data
        return Response(user_serializer)


class DeleteUserView(APIView):
    serializer_class = UserSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request, username, format=None):
        if not request.user.is_superuser:
            return Response("only admin can perform this stuff")
        try:
            user = User.objects.filter(username=username)
            user.delete()
        except User.DoesNotExist:
            return Response("User Does not exist")

        return Response("User deleted Successfully")
