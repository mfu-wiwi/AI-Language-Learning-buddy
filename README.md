# AI Language Learning Platform

A Django-based language learning platform powered by AI, featuring three interactive chat modes: Language Learning Assistance, Quiz Chat, and Matching Chat. The platform integrates with N8n webhooks for AI-powered responses.

## Features

### 🔐 User Authentication
- User registration and login
- Secure password authentication
- User profile management

### 💬 Three Chat Categories

1. **Language Learning Assistance** 📚
   - Get personalized help with vocabulary, grammar, and pronunciation
   - Interactive conversation practice
   - Real-time AI-powered assistance

2. **Quiz Chat** 🎯
   - Interactive quizzes to test your knowledge
   - Instant feedback on answers
   - Progress tracking with average scores

3. **Matching Chat** 🔄
   - Match words, phrases, and concepts
   - Improve vocabulary and understanding
   - Interactive learning exercises

### 📊 Progress Tracking
- Track progress across all chat categories
- View statistics (level, sessions, scores)
- Monitor learning achievements
- Visual progress dashboard

### 💾 Chat History
- Save and review all chat sessions
- Filter by chat type
- Delete old sessions
- Access recent conversations

## Technical Stack

- **Backend**: Django 5.2.8
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **AI Integration**: N8n Webhooks
- **Authentication**: Django Auth System

## Database Schema

### Users & Profiles
- User authentication via Django's built-in User model
- UserProfile for extended user information

### Chat Management
- ChatSession: Stores chat sessions with type and metadata
- ChatMessage: Stores individual messages with sender info

### Progress Tracking
- UserProgress: Tracks user progress per chat category

## Installation & Setup

### 1. Clone the repository
```bash
cd AI_language_learning
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate  # Linux/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure N8n Webhooks
Edit `language_learning_platform/settings.py` and update:
```python
N8N_WEBHOOK_ASSISTANCE = 'https://your-n8n-instance.com/webhook/language-assistance'
N8N_WEBHOOK_QUIZ = 'https://your-n8n-instance.com/webhook/quiz-chat'
N8N_WEBHOOK_MATCHING = 'https://your-n8n-instance.com/webhook/matching-chat'
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser (admin)
```bash
python manage.py createsuperuser
```

### 7. Run the development server
```bash
python manage.py runserver
```

### 8. Access the application
- Application: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## Project Structure

```
AI_language_learning/
├── accounts/               # User authentication & profiles
│   ├── models.py          # UserProfile model
│   ├── views.py           # Auth views (login, register, logout)
│   └── urls.py            # Auth URLs
├── chat/                  # Chat functionality
│   ├── models.py          # ChatSession, ChatMessage models
│   ├── views.py           # Chat views & N8n integration
│   └── urls.py            # Chat URLs
├── progress/              # Progress tracking
│   ├── models.py          # UserProgress model
│   ├── views.py           # Progress views
│   └── urls.py            # Progress URLs
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── accounts/         # Auth templates
│   ├── chat/             # Chat templates
│   └── progress/         # Progress templates
├── language_learning_platform/  # Main project settings
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI config
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## API Endpoints

### Authentication
- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/profile/` - User profile

### Chat
- `/chat/` - Dashboard (chat categories)
- `/chat/create/<chat_type>/` - Create new chat session
- `/chat/room/<session_id>/` - Chat room
- `/chat/send/<session_id>/` - Send message (triggers N8n)
- `/chat/history/` - View chat history
- `/chat/delete/<session_id>/` - Delete session

### Progress
- `/progress/` - View user progress

## N8n Integration

The platform sends requests to N8n webhooks with the following payload structure:

```json
{
  "userId": "user_id",
  "sessionId": "session_id",
  "chatType": "assistance|quiz|matching",
  "message": "user message",
  "context": {
    "username": "username",
    "previousMessages": [...]
  }
}
```

Expected response from N8n:
```json
{
  "response": "AI-generated response text"
}
```

## Usage

1. **Register/Login**: Create an account or login
2. **Choose Chat Type**: Select from three chat categories
3. **Start Chatting**: Send messages and receive AI responses
4. **Track Progress**: View your learning progress and statistics
5. **Review History**: Access past conversations anytime

## Demo Mode

When N8n webhooks are not configured, the app runs in demo mode with placeholder responses.

## Future Enhancements

- [ ] Real-time chat with WebSockets (Django Channels)
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Gamification (badges, achievements)
- [ ] Social features (share progress)
- [ ] Mobile app (React Native)
- [ ] Integration with more AI models

## Contributing

Feel free to submit issues, fork the repository, and create pull requests!

## License

MIT License - feel free to use this project for learning and development.

## Support

For questions or issues, please open an issue on the repository.

---

**Happy Learning! 🚀📚**
