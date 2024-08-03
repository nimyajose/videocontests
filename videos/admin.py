from django.contrib import admin
from .models import UserProfile, Video, Vote  # Import your models

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified')
    search_fields = ('user__username',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'views_count', 'likes_count')
    search_fields = ('title',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'voted_at')
    list_filter = ('voted_at', 'video')
    search_fields = ('user__username', 'video__title')
# admin.py



