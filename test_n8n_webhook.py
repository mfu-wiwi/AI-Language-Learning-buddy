"""
Test N8n Webhook Connection
Run this to verify your N8n webhook is working correctly
"""
import requests
import json

# Your N8n webhook URL
WEBHOOK_URL = 'https://n8n.mettagarden.live/webhook-test/language-learning-chat'

# Test payload
payload = {
    'userId': '1',
    'sessionId': 'test-session-123',
    'chatType': 'assistance',
    'message': 'Hello, can you help me with Spanish?',
    'context': {
        'username': 'testuser',
        'previousMessages': []
    }
}

print("🧪 Testing N8n Webhook Connection...")
print(f"📤 URL: {WEBHOOK_URL}")
print(f"📦 Payload: {json.dumps(payload, indent=2)}")
print("\n" + "="*60 + "\n")

try:
    response = requests.post(
        WEBHOOK_URL,
        json=payload,
        timeout=30,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"📥 Status Code: {response.status_code}")
    print(f"📥 Headers: {dict(response.headers)}")
    print(f"📥 Raw Response: {response.text}")
    print("\n" + "="*60 + "\n")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"✅ JSON Response: {json.dumps(data, indent=2)}")
            
            if 'response' in data:
                print(f"\n✅ SUCCESS! AI Response: {data['response']}")
            elif 'output' in data:
                print(f"\n✅ SUCCESS! AI Output: {data['output']}")
            else:
                print(f"\n⚠️  WARNING: No 'response' or 'output' key found!")
                print(f"Available keys: {list(data.keys())}")
        except ValueError as e:
            print(f"❌ JSON Parsing Error: {e}")
    else:
        print(f"❌ Error: HTTP {response.status_code}")
        
except requests.exceptions.Timeout:
    print("❌ Timeout: N8n took too long to respond")
    
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection Error: {e}")
    
except Exception as e:
    print(f"❌ Unexpected Error: {type(e).__name__}: {e}")

print("\n" + "="*60)
print("Test complete!")
