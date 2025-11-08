from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('create/<str:chat_type>/', views.create_chat_session, name='create_session'),
    path('room/<uuid:session_id>/', views.chat_room, name='chat_room'),
    path('send/<uuid:session_id>/', views.send_message, name='send_message'),
    path('history/', views.chat_history, name='history'),
    path('delete/<uuid:session_id>/', views.delete_session, name='delete_session'),
]
