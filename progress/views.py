from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProgress
from chat.models import ChatSession


@login_required
def progress_view(request):
    """View user progress across all chat types"""
    progress_list = UserProgress.objects.filter(user=request.user)
    
    # Get statistics
    total_sessions = ChatSession.objects.filter(user=request.user).count()
    
    context = {
        'progress_list': progress_list,
        'total_sessions': total_sessions,
    }
    return render(request, 'progress/progress.html', context)
