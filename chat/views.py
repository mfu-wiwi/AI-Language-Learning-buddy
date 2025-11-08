from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import ChatSession, ChatMessage
from progress.models import UserProgress
import requests
import json


@login_required
def dashboard_view(request):
    """Main dashboard showing chat categories"""
    # Get recent chat sessions
    recent_sessions = ChatSession.objects.filter(user=request.user)[:5]
    
    # Get user progress for each category
    progress_data = {}
    for chat_type, _ in ChatSession.CHAT_TYPE_CHOICES:
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            chat_type=chat_type
        )
        progress_data[chat_type] = progress
    
    context = {
        'recent_sessions': recent_sessions,
        'progress_data': progress_data,
    }
    return render(request, 'chat/dashboard.html', context)


@login_required
def create_chat_session(request, chat_type):
    """Create a new chat session"""
    if chat_type not in dict(ChatSession.CHAT_TYPE_CHOICES):
        messages.error(request, 'Invalid chat type.')
        return redirect('chat:dashboard')
    
    # Create new session
    session = ChatSession.objects.create(
        user=request.user,
        chat_type=chat_type,
        title=f"{dict(ChatSession.CHAT_TYPE_CHOICES)[chat_type]} - {ChatSession.objects.filter(user=request.user, chat_type=chat_type).count() + 1}"
    )
    
    # Update progress
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        chat_type=chat_type
    )
    progress.total_sessions += 1
    progress.save()
    
    return redirect('chat:chat_room', session_id=session.id)


@login_required
def chat_room(request, session_id):
    """Chat room view"""
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    messages_list = session.messages.all()
    
    context = {
        'session': session,
        'messages': messages_list,
    }
    return render(request, 'chat/chat_room.html', context)


@login_required
def send_message(request, session_id):
    """Send message and get AI response from N8n webhook"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    
    message_content = request.POST.get('message', '').strip()
    if not message_content:
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)
    
    # Save user message
    user_message = ChatMessage.objects.create(
        session=session,
        sender='user',
        message_content=message_content
    )
    
    # Determine webhook URL based on chat type
    webhook_urls = {
        'assistance': settings.N8N_WEBHOOK_ASSISTANCE,
        'quiz': settings.N8N_WEBHOOK_QUIZ,
        'matching': settings.N8N_WEBHOOK_MATCHING,
    }
    webhook_url = webhook_urls.get(session.chat_type)
    
    # Prepare payload for N8n
    payload = {
        'userId': str(request.user.id),
        'sessionId': str(session.id),
        'chatType': session.chat_type,
        'message': message_content,
        'context': {
            'username': request.user.username,
            'previousMessages': [
                {
                    'sender': msg.sender,
                    'content': msg.message_content,
                    'timestamp': msg.timestamp.isoformat()
                }
                for msg in session.messages.all()[:10]  # Last 10 messages for context
            ]
        }
    }
    
    # Send to N8n webhook (with improved error handling)
    assistant_response = "I'm currently unable to connect. Please try again later."
    
    # Check if webhook URL is configured
    if not webhook_url or webhook_url == '':
        print(f"⚠️  N8n webhook not configured for {session.chat_type}")
        assistant_response = f"Demo mode: I received your message '{message_content}'. N8n webhook is not configured yet."
    else:
        try:
            print(f"📤 Sending to N8n: {webhook_url}")
            print(f"📦 Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                webhook_url, 
                json=payload, 
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"📥 N8n Status Code: {response.status_code}")
            print(f"📥 N8n Response: {response.text[:500]}")
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    print(f"✅ Parsed JSON: {response_data}")
                    
                    # Try multiple possible response keys
                    assistant_response = (
                        response_data.get('response') or 
                        response_data.get('output') or 
                        response_data.get('message') or
                        response_data.get('text') or
                        response_data.get('result')
                    )
                    
                    if assistant_response:
                        print(f"✅ AI Response received: {assistant_response[:100]}...")
                    else:
                        print(f"⚠️  No valid response key found in: {response_data}")
                        assistant_response = "Sorry, I received an empty response from the AI."
                        
                except ValueError as e:
                    print(f"❌ JSON parsing error: {e}")
                    print(f"Raw response: {response.text}")
                    assistant_response = f"Error: Unable to parse AI response."
            else:
                print(f"❌ Error status code: {response.status_code}")
                assistant_response = f"Error: AI service returned status {response.status_code}."
                
        except requests.exceptions.Timeout:
            print("❌ Request timeout")
            assistant_response = "The AI is taking too long to respond. Please try again."
            
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection error: {e}")
            assistant_response = f"Demo mode: I received your message '{message_content}'. Cannot connect to N8n webhook."
            
        except Exception as e:
            print(f"❌ Unexpected error: {type(e).__name__}: {e}")
            assistant_response = f"Demo mode: I received your message '{message_content}'. Error: {str(e)[:100]}"
    
    # Save assistant response
    assistant_message = ChatMessage.objects.create(
        session=session,
        sender='assistant',
        message_content=assistant_response
    )
    
    return JsonResponse({
        'success': True,
        'user_message': {
            'id': str(user_message.id),
            'content': user_message.message_content,
            'timestamp': user_message.timestamp.isoformat()
        },
        'assistant_message': {
            'id': str(assistant_message.id),
            'content': assistant_message.message_content,
            'timestamp': assistant_message.timestamp.isoformat()
        }
    })


@login_required
def chat_history(request):
    """View all chat history"""
    sessions = ChatSession.objects.filter(user=request.user)
    
    # Filter by chat type if provided
    chat_type = request.GET.get('type')
    if chat_type and chat_type in dict(ChatSession.CHAT_TYPE_CHOICES):
        sessions = sessions.filter(chat_type=chat_type)
    
    context = {
        'sessions': sessions,
        'chat_types': ChatSession.CHAT_TYPE_CHOICES,
        'selected_type': chat_type,
    }
    return render(request, 'chat/history.html', context)


@login_required
def delete_session(request, session_id):
    """Delete a chat session"""
    session = get_object_or_404(ChatSession, id=session_id, user=request.user)
    session.delete()
    messages.success(request, 'Chat session deleted successfully.')
    return redirect('chat:history')
