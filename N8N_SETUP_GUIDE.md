# N8n Webhook Setup Guide

This guide explains how to set up N8n workflows to handle the three chat types.

## Prerequisites

1. **N8n Installation**
   - Cloud: https://app.n8n.cloud/
   - Self-hosted: https://docs.n8n.io/hosting/installation/

2. **AI Model Access**
   - OpenAI API Key (GPT-4)
   - Anthropic API Key (Claude)
   - Or any other AI model API

---

## Workflow 1: Language Learning Assistance

### Workflow Overview
```
Webhook Trigger → Extract Data → AI Model (GPT-4) → Format Response → Return JSON
```

### Step-by-Step Setup

1. **Create New Workflow** in N8n

2. **Add Webhook Node**
   - Name: `Language Assistance Webhook`
   - HTTP Method: `POST`
   - Path: `language-assistance`
   - Response Mode: `Last Node`

3. **Add Set Node** (Extract Data)
   - Name: `Extract Message Data`
   - Set Fields:
     ```json
     {
       "userId": "{{ $json.userId }}",
       "sessionId": "{{ $json.sessionId }}",
       "userMessage": "{{ $json.message }}",
       "username": "{{ $json.context.username }}",
       "chatHistory": "{{ $json.context.previousMessages }}"
     }
     ```

4. **Add OpenAI Node** (or Claude)
   - Name: `AI Language Assistant`
   - Operation: `Message a Model`
   - Model: `gpt-4` or `gpt-3.5-turbo`
   - System Message:
     ```
     You are a helpful language learning assistant. Help users with:
     - Vocabulary explanations
     - Grammar rules
     - Pronunciation tips
     - Conversation practice
     - Sentence structure
     
     Be encouraging, clear, and provide examples.
     ```
   - User Message: `{{ $json.userMessage }}`

5. **Add Set Node** (Format Response)
   - Name: `Format AI Response`
   - Set Fields:
     ```json
     {
       "response": "{{ $json.choices[0].message.content }}"
     }
     ```

6. **Activate Workflow**
   - Copy the webhook URL (e.g., `https://your-n8n.com/webhook/language-assistance`)

---

## Workflow 2: Quiz Chat

### Workflow Overview
```
Webhook → Extract → AI Quiz Generator → Parse JSON → Format → Return
```

### Step-by-Step Setup

1. **Create New Workflow**

2. **Add Webhook Node**
   - Path: `quiz-chat`
   - HTTP Method: `POST`

3. **Add Set Node**
   - Extract userId, sessionId, message

4. **Add OpenAI Node**
   - Model: `gpt-4`
   - System Message:
     ```
     You are a quiz generator for language learning. 
     - Generate quiz questions based on user's request
     - Provide multiple choice or fill-in-the-blank questions
     - Give immediate feedback on answers
     - Explain correct answers
     - Track difficulty level
     - Be encouraging
     
     Format your response as:
     Question: [question text]
     Options: A) ... B) ... C) ... D) ...
     Correct Answer: [letter]
     Explanation: [why this is correct]
     ```
   - User Message: `{{ $json.userMessage }}`

5. **Add Function Node** (Calculate Score)
   - JavaScript code to track quiz scores:
     ```javascript
     const userAnswer = $json.userAnswer;
     const correctAnswer = $json.correctAnswer;
     const isCorrect = userAnswer === correctAnswer;
     const score = isCorrect ? 100 : 0;
     
     return {
       json: {
         response: $json.aiResponse,
         score: score,
         isCorrect: isCorrect,
         metadata: {
           score: score,
           correctAnswer: correctAnswer
         }
       }
     };
     ```

6. **Format Response**
   ```json
   {
     "response": "{{ $json.response }}",
     "metadata": {
       "score": "{{ $json.score }}",
       "isCorrect": "{{ $json.isCorrect }}"
     }
   }
   ```

---

## Workflow 3: Matching Chat

### Workflow Overview
```
Webhook → Extract → AI Matcher → Generate Pairs → Format → Return
```

### Step-by-Step Setup

1. **Create New Workflow**

2. **Add Webhook Node**                                    
   - Path: `matching-chat`
   - HTTP Method: `POST`

3. **Add OpenAI Node**
   - System Message:
     ```
     You are a language learning matching game assistant.
     - Generate word/phrase pairs for matching exercises
     - Create translation pairs
     - Provide synonym/antonym matches
     - Give hints when asked
     - Celebrate correct matches
     
     When user starts, provide 5-10 pairs to match.
     When user submits an answer, validate and provide feedback.
     ```

4. **Add Function Node** (Generate Matching Pairs)
   ```javascript
   // Example: Generate matching pairs
   const pairs = [
     { id: 1, word: "Hello", match: "Bonjour" },
     { id: 2, word: "Goodbye", match: "Au revoir" },
     { id: 3, word: "Thank you", match: "Merci" }
   ];
   
   return {
     json: {
       response: "Match the English words with their French translations:",
       pairs: pairs,
       type: "matching-game"
     }
   };
   ```

5. **Format Response**

---

## Example N8n Payload (from Django)

```json
{
  "userId": "1",
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "chatType": "assistance",
  "message": "How do I say 'Good morning' in Spanish?",
  "context": {
    "username": "demo",
    "previousMessages": [
      {
        "sender": "user",
        "content": "Hello!",
        "timestamp": "2025-11-06T10:00:00"
      },
      {
        "sender": "assistant",
        "content": "Hello! How can I help you learn today?",
        "timestamp": "2025-11-06T10:00:05"
      }
    ]
  }
}
```

## Example N8n Response (to Django)

```json
{
  "response": "In Spanish, 'Good morning' is said as 'Buenos días' (pronounced: BWEH-nos DEE-ahs). Here's a breakdown:\n- 'Buenos' means 'good'\n- 'Días' means 'days'\n\nExample: '¡Buenos días! ¿Cómo estás?' means 'Good morning! How are you?'"
}
```

---

## Advanced N8n Features

### 1. Add Context Memory
Use N8n's Redis or Database nodes to store conversation context:

```
Webhook → Load Previous Context → AI Model → Save New Context → Return
```

### 2. Multi-Language Support
Add a Switch node based on user's learning language:

```
Extract Language → Switch Node
    ├─ Spanish → Spanish Tutor AI
    ├─ French → French Tutor AI
    └─ German → German Tutor AI
```

### 3. Progress Tracking
Send progress updates back to Django:

```
AI Response → HTTP Request Node (POST to Django Progress API) → Return
```

### 4. Error Handling
Add Error Trigger node:

```
On Error → Format Error Message → Return Friendly Error
```

Example error response:
```json
{
  "response": "I'm having trouble processing your request right now. Please try again in a moment.",
  "error": true
}
```

---

## Testing N8n Webhooks

### Using cURL:

```bash
curl -X POST https://your-n8n.com/webhook/language-assistance \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "1",
    "sessionId": "test-session",
    "chatType": "assistance",
    "message": "How do I conjugate the verb to be in Spanish?",
    "context": {
      "username": "testuser",
      "previousMessages": []
    }
  }'
```

### Using Postman:

1. Create new POST request
2. URL: `https://your-n8n.com/webhook/language-assistance`
3. Headers: `Content-Type: application/json`
4. Body (raw JSON): Copy the JSON payload above
5. Send

---

## Configuring Django to Use N8n

After setting up your N8n workflows, update `language_learning_platform/settings.py`:

```python
# Replace these with your actual N8n webhook URLs
N8N_WEBHOOK_ASSISTANCE = 'https://your-n8n-instance.com/webhook/language-assistance'
N8N_WEBHOOK_QUIZ = 'https://your-n8n-instance.com/webhook/quiz-chat'
N8N_WEBHOOK_MATCHING = 'https://your-n8n-instance.com/webhook/matching-chat'
```

Or use environment variables (recommended):

1. Create `.env` file:
```bash
N8N_WEBHOOK_ASSISTANCE=https://your-n8n.com/webhook/language-assistance
N8N_WEBHOOK_QUIZ=https://your-n8n.com/webhook/quiz-chat
N8N_WEBHOOK_MATCHING=https://your-n8n.com/webhook/matching-chat
```

2. Update `settings.py`:
```python
from decouple import config

N8N_WEBHOOK_ASSISTANCE = config('N8N_WEBHOOK_ASSISTANCE', default='')
N8N_WEBHOOK_QUIZ = config('N8N_WEBHOOK_QUIZ', default='')
N8N_WEBHOOK_MATCHING = config('N8N_WEBHOOK_MATCHING', default='')
```

---

## Troubleshooting

### Problem: Webhook timeout
**Solution**: Increase timeout in Django:
```python
response = requests.post(webhook_url, json=payload, timeout=60)  # 60 seconds
```

### Problem: N8n returns error
**Solution**: Check N8n execution logs and add error handling:
```python
try:
    response = requests.post(webhook_url, json=payload, timeout=30)
    if response.status_code == 200:
        data = response.json()
        return data.get('response', 'Error processing response')
except Exception as e:
    print(f"N8n error: {e}")
    return "Sorry, I'm having trouble connecting right now."
```

### Problem: Missing AI response
**Solution**: Ensure N8n workflow returns JSON with "response" key

---

## Best Practices

1. **Always validate webhook responses**
2. **Add rate limiting** to prevent abuse
3. **Log all webhook calls** for debugging
4. **Use environment variables** for webhook URLs
5. **Implement retry logic** for failed requests
6. **Add timeout handling**
7. **Monitor N8n execution logs**

---

## Example N8n Workflow JSON Export

You can import this workflow into N8n:

```json
{
  "name": "Language Learning Assistance",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "webhookId": "language-assistance",
      "parameters": {
        "httpMethod": "POST",
        "path": "language-assistance",
        "responseMode": "lastNode"
      }
    },
    {
      "name": "OpenAI",
      "type": "n8n-nodes-base.openAi",
      "position": [450, 300],
      "parameters": {
        "operation": "message",
        "model": "gpt-4",
        "messages": {
          "values": [
            {
              "role": "system",
              "content": "You are a helpful language learning assistant."
            },
            {
              "role": "user",
              "content": "={{ $json.message }}"
            }
          ]
        }
      }
    },
    {
      "name": "Format Response",
      "type": "n8n-nodes-base.set",
      "position": [650, 300],
      "parameters": {
        "values": {
          "string": [
            {
              "name": "response",
              "value": "={{ $json.choices[0].message.content }}"
            }
          ]
        }
      }
    }
  ]
}
```

---

## Next Steps

1. ✅ Set up N8n account
2. ✅ Create three workflows
3. ✅ Configure AI model credentials
4. ✅ Test each webhook
5. ✅ Update Django settings
6. ✅ Test full integration
7. ✅ Monitor and optimize

**Happy N8n Setup! 🚀**
