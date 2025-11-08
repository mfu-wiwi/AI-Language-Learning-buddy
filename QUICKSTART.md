# 🚀 Quick Start Guide

Get your AI Language Learning Platform running in **5 minutes**!

---

## ✅ Current Status

The application is **READY** and the server is **RUNNING**!

🌐 **Access your app**: http://127.0.0.1:8000/

---

## 📋 Quick Access

### Try the Application Right Now:

1. **Open your browser**: http://127.0.0.1:8000/

2. **Register a new account**:
   - Click "Register here"
   - Choose a username and password
   - Click "Register"

3. **Start chatting**:
   - You'll see 3 chat categories
   - Click any category to start
   - Send messages and get AI responses (demo mode)

---

## 🔑 Demo Accounts

Run this command to create demo accounts:

```powershell
.\venv\Scripts\python.exe setup_demo.py
```

**Demo User:**
- Username: `demo`
- Password: `demo1234`

**Admin User:**
- Username: `admin`
- Password: `admin1234`
- Admin Panel: http://127.0.0.1:8000/admin/

---

## 🎯 Main Features to Test

### 1. Language Learning Assistance Chat 📚
- Click the purple card with 📚 icon
- Ask: "How do I say hello in Spanish?"
- Get AI response (demo mode)

### 2. Quiz Chat 🎯
- Click the quiz card with 🎯 icon
- Ask: "Give me a grammar quiz"
- Take interactive quizzes

### 3. Matching Chat 🔄
- Click the matching card with 🔄 icon
- Ask: "Create a vocabulary matching game"
- Match words and phrases

### 4. Chat History 📜
- Click "Chat History" in navigation
- View all your past conversations
- Filter by chat type
- Delete old sessions

### 5. Progress Tracking 📊
- Click "My Progress" in navigation
- See statistics for each category
- View your level and session count
- Check quiz scores

---

## 🛠️ Common Commands

### Start the server:
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### Stop the server:
Press `CTRL+C` in the terminal

### Create admin account:
```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```

### Apply database changes:
```powershell
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management script |
| `db.sqlite3` | Database file |
| `language_learning_platform/settings.py` | Configuration |
| `templates/` | HTML templates |
| `accounts/`, `chat/`, `progress/` | Django apps |

---

## 🔌 Connect to Real AI (N8n)

Currently running in **demo mode**. To connect real AI:

1. Set up N8n workflows (see `N8N_SETUP_GUIDE.md`)
2. Get webhook URLs from N8n
3. Update `settings.py`:
   ```python
   N8N_WEBHOOK_ASSISTANCE = 'https://your-n8n.com/webhook/language-assistance'
   N8N_WEBHOOK_QUIZ = 'https://your-n8n.com/webhook/quiz-chat'
   N8N_WEBHOOK_MATCHING = 'https://your-n8n.com/webhook/matching-chat'
   ```
4. Restart server

---

## 📖 Full Documentation

- `README.md` - Complete project documentation
- `IMPLEMENTATION_GUIDE.md` - Detailed implementation details
- `ARCHITECTURE.md` - System architecture diagrams
- `N8N_SETUP_GUIDE.md` - N8n webhook setup

---

## 🐛 Troubleshooting

### Server not starting?
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start server
python manage.py runserver
```

### Port already in use?
```powershell
# Use different port
python manage.py runserver 8080
```

### Database errors?
```powershell
# Reset database
python manage.py migrate
```

### Can't login?
```powershell
# Create new user
python manage.py createsuperuser
```

---

## 🎓 User Flow Example

1. **Register**: Create account with username/password
2. **Dashboard**: See 3 chat categories with stats
3. **Choose**: Click "Language Learning Assistance"
4. **Chat**: New session opens, start typing
5. **Message**: "Help me with French vocabulary"
6. **Response**: AI assistant replies (demo mode)
7. **Continue**: Keep chatting in same session
8. **History**: View saved conversation later
9. **Progress**: Check your stats and level

---

## 📊 Database Schema Overview

```
User
  ├─ UserProfile (1:1)
  ├─ ChatSession (1:N)
  │    └─ ChatMessage (1:N)
  └─ UserProgress (1:N)
```

---

## 🎨 UI Screenshots Locations

When you open the app, you'll see:

1. **Login Page**: Clean gradient background, centered form
2. **Dashboard**: 3 colorful category cards with stats
3. **Chat Room**: WhatsApp-style chat interface
4. **History**: List of all chat sessions with filters
5. **Progress**: Visual cards showing stats per category

---

## 🔒 Security Notes

- Passwords are hashed (Django's built-in system)
- CSRF protection enabled
- Login required for all features
- Session management active
- SQL injection protected (Django ORM)

---

## 🚀 Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure PostgreSQL database
3. Set up static file serving
4. Use Gunicorn/uWSGI
5. Configure HTTPS
6. Set up environment variables

See `README.md` for detailed deployment instructions.

---

## 📞 Need Help?

If you encounter any issues:

1. Check the error message in terminal
2. Look at browser console (F12)
3. Review the documentation files
4. Check Django logs

---

## ✨ What's Next?

Extend the platform with:

- [ ] Real-time chat (WebSockets)
- [ ] Voice input/output
- [ ] Image uploads
- [ ] Multi-language UI
- [ ] Mobile responsive design (already partially done)
- [ ] Social features
- [ ] Gamification
- [ ] Analytics dashboard

---

## 🎉 You're All Set!

Your AI Language Learning Platform is ready to use!

**Happy Learning! 📚🚀**

---

**Quick Links:**
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Documentation: `README.md`
