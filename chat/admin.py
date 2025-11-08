from django.contrib import admin
from .models import ChatSession, ChatMessage


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'chat_type', 'title', 'created_at', 'is_active']
    list_filter = ['chat_type', 'is_active', 'created_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'sender', 'timestamp']
    list_filter = ['sender', 'timestamp']
    search_fields = ['session__title', 'message_content']
    readonly_fields = ['id', 'timestamp']
