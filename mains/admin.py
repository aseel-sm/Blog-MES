#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Members
from .models import Profile
from .models import Blog
from .models import Comment


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'dept', 'insta_id', 'about')


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'content',
        'author',
        'author_name',
        'date',
        'edit',
        'comment_no',
        'user_pic',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog_id', 'comment', 'date', 'commenter',
                    'commenter_name')


class MembersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'image')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)

# admin.site.register(Members,UserAdmin)

admin.site.register(Members, MembersAdmin)
