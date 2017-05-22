from django import forms
from django.contrib.auth.models import User, Group
from rest_framework import serializers

# from users.models import Task
from blogs.models import Post, Category, Blog
from datetime import datetime


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    def create_blog_if_not_exist(self, user):
        blog_title = user.username + "_" + "Blog"
        return Blog.objects.create(title=blog_title, author=user)

    def get_user_blog(self, user):

        blog = Blog.objects.filter(author=user)
        if not blog:
            return self.create_blog_if_not_exist(user)

    def validate(self, data):
        username = data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist as ex:
            return data
        raise serializers.ValidationError("finish must occur after start")

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        self.get_user_blog(user)
        return user

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Blog
        exclude = ['title', 'author']


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['category', 'blog']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['category', 'blog', 'slug']

    def create_blog_if_not_exist(self, user):
        blog_title = user.first_name + "_" + "Blog"
        return Blog.objects.create(title=blog_title, author=user)

    def get_user_blog(self, user):
        try:
            blog = Blog.objects.get(author=user)
        except Blog.DoesNotExist:
            return self.create_blog_if_not_exist(user)
        return blog

    def create(self, validated_data):
        user_id = self.context.get("user_id")
        category_ids = self.context.get("category")
        categories = []
        if category_ids != ['']:
            categories = Category.objects.filter(id__in=category_ids)
        user = User.objects.get(id=user_id)
        post = Post(**validated_data)
        post.blog = self.get_user_blog(user)
        post.save()
        for cat in categories:
            post.category.add(cat)
        post.save()
        return post

    def remove_all_categories(self, instance):
        instance.category.clear()

    def update(self, instance, validated_data):

        # user_id = self.context.get("user_id")
        category_ids = self.context.get("category")
        categories = Category.objects.filter(id__in=category_ids)
        # user = User.objects.get(id=user_id)
        # post = Post(**validated_data)
        # post.blog = user.blog

        # post.save()
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.posted_at = datetime.now()
        for cat in categories:
            instance.category.add(cat)
        instance.save()
        return instance

        # return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100,
        style={'placeholder': 'Username', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    remember_me = serializers.BooleanField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['hidden']

        #  # class GroupSerializer(serializers.HyperlinkedModelSerializer):

# class Meta:
#         model = Group
#         fields = ('url', 'name')
#
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')
#
#
# class TaskSerializer(serializers.ModelSerializer):
#     my_task = serializers.SerializerMethodField('self_task')
#     user = UserProfileSerializer(many=False, read_only=True)
#
#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'description', 'my_task', 'done', 'user']
#
#     def self_task(self, obj):
#         user_id = self.context.get("user_id")
#         if isinstance(obj, Task) and obj.user.id == user_id:
#             return True
#         return False
#
#     def create(self, validated_data):
#         task_data = validated_data
#         user_id = self.context.get("user_id")
#         task = Task.objects.create(user_id=user_id, **task_data)
#         return task
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.done = validated_data.get('done', instance.done)
#         instance.save()
#         return instance
