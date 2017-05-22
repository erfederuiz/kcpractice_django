from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Blog(models.Model):
    title = models.CharField(max_length=100)
    author = models.OneToOneField(User, related_name='blog')
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Blog, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.title

    def __str__(self):
        return '%s' % self.title


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    hidden = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.title

    def __str__(self):
        return '%s' % self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    picture = models.ImageField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    summary = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False)
    blog = models.ForeignKey(Blog, related_name='post')
    category = models.ManyToManyField(Category)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.title

    def __str__(self):
        return '%s' % self.title
