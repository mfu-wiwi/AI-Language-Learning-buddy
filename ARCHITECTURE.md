# System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          USER BROWSER                                       │
│                    (HTML/CSS/JavaScript)                                    │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 │ HTTP Requests
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DJANGO APPLICATION                                   │
│                                                                              │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐               │
│  │   ACCOUNTS     │  │     CHAT       │  │   PROGRESS     │               │
│  │   (Auth)       │  │   (Chatbot)    │  │   (Tracking)   │               │
│  ├────────────────┤  ├────────────────┤  ├────────────────┤               │
│  │ • Register     │  │ • Dashboard    │  │ • View Stats   │               │
│  │ • Login        │  │ • Chat Room    │  │ • Level Info   │               │
│  │ • Logout       │  │ • History      │  │ • Achievements │               │
│  │ • Profile      │  │ • Send Msg     │  │                │               │
│  └────────────────┘  └────────────────┘  └────────────────┘               │
│                                │                                            │
│                                │ N8n Webhook Trigger                       │
│                                ▼                                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                 │
                  ┌──────────────┼──────────────┐
                  │              │              │
                  ▼              ▼              ▼
    ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐
    │  N8n Webhook 1   │  │ N8n Webhook 2│  │ N8n Webhook 3│
    │   (Assistance)   │  │    (Quiz)    │  │  (Matching)  │
    └────────┬─────────┘  └──────┬───────┘  └──────┬───────┘
             │                   │                  │
             └───────────────────┼──────────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │   AI MODELS (Backend)   │
                    │  • GPT-4 / Claude       │
                    │  • Custom AI Logic      │
                    │  • Response Generation  │
                    └─────────────────────────┘
                                 │
                                 │ AI Response
                                 ▼
                         (Returns to Django)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DATABASE (SQLite/PostgreSQL)                          │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │    Users     │  │ ChatSession  │  │ ChatMessage  │  │ UserProgress │   │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤   │
│  │ • id         │  │ • id (UUID)  │  │ • id (UUID)  │  │ • user_id    │   │
│  │ • username   │  │ • user_id    │  │ • session_id │  │ • chat_type  │   │
│  │ • password   │  │ • chat_type  │  │ • sender     │  │ • level      │   │
│  │ • email      │  │ • title      │  │ • content    │  │ • sessions   │   │
│  └──────────────┘  │ • created_at │  │ • timestamp  │  │ • avg_score  │   │
│                    └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Registration/Login
```
User → Register Form → Django Auth → Create User → Create Profile → Redirect to Dashboard
```

### 2. Start Chat Session
```
User → Click Category → Create Session → Update Progress → Open Chat Room
```

### 3. Send Message & Get AI Response
```
User Types Message
    ↓
JavaScript (AJAX) → Django View (send_message)
    ↓
Save User Message to DB
    ↓
Prepare Payload (userId, sessionId, message, context)
    ↓
HTTP POST to N8n Webhook
    ↓
N8n Processes with AI Model
    ↓
AI Response Returns to Django
    ↓
Save Assistant Message to DB
    ↓
Return JSON Response to Frontend
    ↓
JavaScript Displays Messages
```

### 4. View Progress
```
User → Progress Page → Query UserProgress → Display Stats → Show Charts
```

### 5. View Chat History
```
User → History Page → Query ChatSessions → Filter by Type → Display List
```

## Chat Type Webhooks

| Chat Type | Webhook URL | Purpose |
|-----------|-------------|---------|
| **Assistance** | `/webhook/language-assistance` | Language learning help, grammar, vocabulary |
| **Quiz** | `/webhook/quiz-chat` | Interactive quizzes, score tracking |
| **Matching** | `/webhook/matching-chat` | Word/phrase matching exercises |

## N8n Workflow Structure

```
┌─────────────────────────────────────────────────────┐
│              N8n Workflow (Example)                 │
│                                                     │
│  1. Webhook Trigger (Receive from Django)          │
│           ↓                                         │
│  2. Extract Data (userId, message, context)        │
│           ↓                                         │
│  3. AI Model Node (GPT-4/Claude API)               │
│           ↓                                         │
│  4. Process Response                                │
│           ↓                                         │
│  5. Format JSON                                     │
│           ↓                                         │
│  6. Respond to Webhook                             │
└─────────────────────────────────────────────────────┘
```

## Technologies Used

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Backend** | Python 3.13, Django 5.2.8 |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Integration** | N8n Webhooks |
| **AI Models** | GPT-4, Claude (via N8n) |
| **Authentication** | Django Auth System |
| **Session Management** | Django Sessions |

## Security Layers

```
┌──────────────────────────────────────────────┐
│  1. HTTPS (SSL/TLS) - Transport Layer       │
├──────────────────────────────────────────────┤
│  2. Django CSRF Protection                   │
├──────────────────────────────────────────────┤
│  3. Password Hashing (PBKDF2/bcrypt)        │
├──────────────────────────────────────────────┤
│  4. Session Authentication                   │
├──────────────────────────────────────────────┤
│  5. Login Required Decorators               │
├──────────────────────────────────────────────┤
│  6. SQL Injection Prevention (ORM)          │
├──────────────────────────────────────────────┤
│  7. XSS Protection (Template Escaping)      │
└──────────────────────────────────────────────┘
```
