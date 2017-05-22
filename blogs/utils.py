from blogs.models import Category
from datetime import datetime


def get_all_visible_categories():
    return Category.objects.filter(hidden=False)


def update_post(instance, validated_data, category_ids):
    categories = Category.objects.filter(id__in=category_ids)
    instance.title = validated_data.get('title', instance.title)
    instance.body = validated_data.get('body', instance.body)
    instance.summary = validated_data.get('summary', instance.summary)
    instance.is_published = validated_data.get('is_published', instance.is_published)
    instance.posted_at = datetime.now()
    for cat in categories:
        instance.category.add(cat)
    instance.save()

    return instance


def update_user(instance, validated_data):
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    instance.email = validated_data.get('email', instance.email)
    instance.set_password(validated_data.get('password', instance.password))
    instance.save()
    return instance
