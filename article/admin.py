from django.contrib import admin
from .models import Category, Article, Like, Subscriber

# Register your models here.

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Like)
admin.site.register(Subscriber)
