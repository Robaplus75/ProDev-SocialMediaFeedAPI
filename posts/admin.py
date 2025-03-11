from django.contrib import admin
from .models import Post, Comment, Share

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Share)
