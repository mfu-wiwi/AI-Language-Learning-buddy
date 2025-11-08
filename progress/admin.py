from django.contrib import admin
from .models import UserProgress


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'chat_type', 'level', 'total_sessions', 'quiz_score_avg', 'last_activity']
    list_filter = ['chat_type', 'level']
    search_fields = ['user__username']
