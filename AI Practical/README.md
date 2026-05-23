# Azure AI Content Safety - Content Moderation System

## 📋 Project Overview

This is a complete Python project that implements a **Content Moderation System** using **Azure AI Content Safety REST API**. The application analyzes user-generated content to detect and classify inappropriate or harmful text including:

- 🔴 **Hate Speech** - Hateful, discriminatory content
- 🔪 **Violence** - Aggressive, violent language
- 🔞 **Sexual Content** - Inappropriate sexual material
- ⚠️ **Self-Harm** - Content promoting self-injury or suicide

### 🎯 Key Features

✅ Terminal-based interactive interface
✅ Real-time content analysis via Azure API
✅ Severity scoring for each content category (0-6 scale)
✅ Automatic content approval/blocking decision
✅ Comprehensive error handling
✅ Beginner-friendly code with detailed comments
✅ Optional Flask API for web integration
✅ Professional logging and formatted output

---

## 🏗️ Project Structure

```
azure-content-moderator/
├── app.py                 # Main application (Terminal mode)
├── config.py              # Configuration file (API credentials)
├── flask_api.py           # Optional Flask web API
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .env                   # Environment variables (optional, for production)
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- An Azure account with Content Safety resource

### Step 1: Clone/Download the Project

```bash
cd path/to/project
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Azure API Credentials

#### 4a. Get Your Azure Credentials

1. Go to [Azure Portal](https://portal.azure.com)
2. Create a new resource: **Content Safety**
3. Navigate to **Keys and Endpoint**
4. Copy your:
   - **Subscription Key** (Key1 or Key2)
   - **Endpoint URL**

#### 4b. Add Credentials to config.py

Edit `config.py` and replace:

```python
AZURE_API_KEY = "YOUR_API_KEY_HERE"
AZURE_ENDPOINT = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com"
```

Example:
```python
AZURE_API_KEY = "abc123def456ghi789jkl012mno345pqr"
AZURE_ENDPOINT = "https://mycontentsafety.cognitiveservices.azure.com"
```

#### 4c. (Production) Use Environment Variables

For security in production, use `.env` file:

1. Create `.env` file in project root:
```
AZURE_API_KEY=your_api_key_here
AZURE_ENDPOINT=https://your_resource.cognitiveservices.azure.com
```

2. Update `config.py` to read from environment:
```python
import os
from dotenv import load_dotenv

load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
```

---

## 💻 Usage

### Terminal Mode (Interactive)

```bash
python app.py
```

**Example Interaction:**

```
============================================================
🛡️  AZURE AI CONTENT SAFETY MODERATOR
============================================================
Severity Threshold for Blocking:  2
Type 'quit' or 'exit' to end the program
------------------------------------------------------------

📝 Enter text to analyze (or 'quit' to exit): I will hurt you

⏳ Analyzing content... Please wait.

============================================================
📋 CONTENT MODERATION ANALYSIS RESULTS
============================================================

📝 User Input:
   "I will hurt you"

📊 Severity Scores (0-6 scale, where 0=safe, 6=highly unsafe):
------------------------------------------------------------
   Hate         | Severity: 1 | █░░░░░
   Violence     | Severity: 5 | █████░
   Sexual       | Severity: 0 | ░░░░░░
   SelfHarm     | Severity: 0 | ░░░░░░

🔍 Decision: Content Blocked ❌
   Reason: Blocked due to: Violence (Severity: 5)
============================================================
```

### Severity Scale

| Score | Meaning | Action |
|-------|---------|--------|
| 0 | Safe content | ✅ Approved |
| 1-2 | Minor issues | ✅ Approved (default threshold=2) |
| 3-4 | Moderate concern | ❌ Blocked |
| 5-6 | Severe content | ❌ Blocked |

### Adjust Blocking Threshold

Edit `app.py` main function:

```python
moderator = ContentModerator(
    api_key=AZURE_API_KEY,
    endpoint=AZURE_ENDPOINT,
    severity_threshold=3  # Change from 2 to 3
)
```

---

## 🌐 Flask Web API (Optional)

### Running the Flask Server

```bash
python flask_api.py
```

Server runs at: `http://localhost:5000`

### API Endpoints

#### 1. Analyze Content (POST)

**Endpoint:** `POST /api/moderate`

**Request:**
```json
{
  "text": "I will hurt you"
}
```

**Response:**
```json
{
  "status": "success",
  "input_text": "I will hurt you",
  "severity_scores": {
    "Hate": 1,
    "Violence": 5,
    "Sexual": 0,
    "SelfHarm": 0
  },
  "decision": "Content Blocked ❌",
  "reason": "Blocked due to: Violence (Severity: 5)"
}
```

#### 2. Health Check (GET)

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "message": "Content Moderator API is running"
}
```

### Using cURL to Test

```bash
# Analyze content
curl -X POST http://localhost:5000/api/moderate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you?"}'

# Health check
curl http://localhost:5000/api/health
```

### Using Python requests to Test

```python
import requests

response = requests.post(
    'http://localhost:5000/api/moderate',
    json={'text': 'Sample text to analyze'}
)

print(response.json())
```

---

## 🔧 Error Handling

The application handles the following errors gracefully:

### 1. Invalid API Key
```
❌ Authentication Error: Invalid API key. 
Please check your credentials in config.py
```
**Solution:** Verify API key in Azure Portal

### 2. Network Errors
```
❌ Error: Cannot connect to Azure API. 
Please check your endpoint URL and internet connection.
```
**Solution:** Check internet connection and endpoint URL

### 3. Empty Input
```
❌ Error: Text input cannot be empty!
```
**Solution:** Enter some text to analyze

### 4. Request Timeout
```
❌ Error: Request timed out. 
Please check your internet connection.
```
**Solution:** Check internet speed and retry

### 5. Invalid Endpoint
```
❌ API Error: HTTP 404 - Not Found
```
**Solution:** Verify endpoint format in config.py

---

## 📊 Code Architecture

### Classes

#### `ContentModerator`
Main class for content analysis

**Methods:**
- `__init__()` - Initialize with API credentials
- `analyze_content()` - Send text to Azure API
- `extract_severity_scores()` - Parse API response
- `decide_content_status()` - Determine approval/blocking
- `display_results()` - Format and print results
- `run_interactive_mode()` - Interactive interface

### Flow Diagram

```
┌─────────────────────┐
│   User Input        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Validate Input      │ ← Check if empty
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Call Azure API      │ ← Send to cloud
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Parse Response      │ ← Extract scores
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Decide Status       │ ← Compare threshold
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Display Results     │ ← Show to user
└─────────────────────┘
```

---

## 🎓 University Project Presentation

### Project Title
**"Azure AI Content Safety: An Automated Content Moderation System for User-Generated Content"**

### Abstract

This project demonstrates the development of an **intelligent content moderation system** using Microsoft Azure's Content Safety API. The system automatically analyzes user-generated text content to detect harmful, inappropriate, or abusive material across four categories: hate speech, violence, sexual content, and self-harm promotion.

### Key Learning Outcomes

1. **Cloud API Integration** - Working with Azure REST APIs and cloud services
2. **Content Moderation** - Understanding ML-based content classification
3. **Error Handling** - Robust exception handling in production systems
4. **Software Architecture** - Clean code structure with separation of concerns
5. **Web Development** - Building APIs for third-party integration
6. **DevOps Practices** - Configuration management and credential security

### Technical Stack

- **Backend:** Python 3.8+
- **API Client:** Requests library
- **Web Framework:** Flask (optional)
- **Cloud Service:** Azure Cognitive Services
- **Architecture:** RESTful API

### Viva Questions & Answers

**Q1: Why use Azure Content Safety instead of building our own classifier?**
- Pre-trained models reduce development time
- Backed by millions of moderation decisions
- Continuously updated with new patterns
- Cost-effective compared to training custom models
- Enterprise-grade reliability and support

**Q2: How does severity scoring work?**
- Azure ML models assign confidence scores (0-6)
- 0 = No harmful content detected
- 6 = Highly unsafe content
- Adjustable threshold allows customization
- Different thresholds for different use cases

**Q3: What are the limitations?**
- Requires internet connection
- Depends on Azure service availability
- May have latency in high-volume scenarios
- Language-specific models (primarily English)
- Cannot detect context-specific harm

**Q4: How would you scale this to millions of posts?**
- Implement message queues (Azure Queue Storage)
- Batch API calls for efficiency
- Add caching layer for repeat content
- Use async processing with workers
- Implement rate limiting and load balancing

**Q5: How do you ensure user privacy?**
- No content stored on our servers
- API calls transmitted over HTTPS
- User data not logged permanently
- Compliant with GDPR/data protection laws
- Azure handles infrastructure security

**Q6: What other use cases exist?**
- Comment moderation on social media
- Email spam and phishing detection
- Review filtering for e-commerce
- Chat monitoring in gaming platforms
- Content approval workflows

---

## 🔐 Security Best Practices

1. **Never hardcode API keys in production**
   ```python
   # ❌ Bad
   AZURE_API_KEY = "actual_key_123"
   
   # ✅ Good
   AZURE_API_KEY = os.getenv("AZURE_API_KEY")
   ```

2. **Use HTTPS for all API calls** ✅ (Already implemented)

3. **Implement rate limiting** (for production)
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   ```

4. **Add authentication to web API** (for production)
   ```python
   from functools import wraps
   
   def require_api_key(f):
       @wraps(f)
       def decorated(*args, **kwargs):
           api_key = request.headers.get('X-API-Key')
           if not api_key or api_key != VALID_API_KEY:
               return jsonify({"error": "Unauthorized"}), 401
           return f(*args, **kwargs)
       return decorated
   ```

5. **Log access attempts** (for auditing)

6. **Rotate API keys regularly** (monthly/quarterly)

---

## 📚 References & Resources

### Azure Documentation
- [Azure Content Safety Documentation](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/)
- [REST API Reference](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-text)

### Python Libraries
- [Requests Library Documentation](https://requests.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Related Concepts
- REST APIs and HTTP protocols
- Machine Learning basics
- Cloud computing with Azure
- Content moderation strategies

---

## 🐛 Troubleshooting

### Issue: "Invalid API Key"
- **Check:** Copy-paste API key correctly from Azure Portal
- **Check:** No extra spaces before/after key
- **Check:** Using correct key (Key1 or Key2)
- **Solution:** Generate new key in Azure Portal if needed

### Issue: "Connection Timeout"
- **Check:** Internet connection is working
- **Check:** Endpoint URL is correct
- **Check:** Azure resource is not in stopped state
- **Solution:** Increase timeout value in config or check Azure service status

### Issue: "ModuleNotFoundError: No module named 'requests'"
- **Solution:** Run `pip install -r requirements.txt`
- **Check:** Using correct Python environment

### Issue: Flask server won't start
- **Check:** Port 5000 is not in use
- **Solution:** Change port in flask_api.py: `app.run(port=5001)`
- **Check:** Flask is installed: `pip install flask`

---

## 📝 License & Attribution

This project is created for educational purposes. Azure AI Content Safety is a Microsoft product.

---

## 📞 Support & Contribution

For questions or improvements:
1. Check the Troubleshooting section
2. Review Azure documentation
3. Test with simple inputs first
4. Check internet connectivity

---

## ✅ Checklist Before Submission

- [ ] Python 3.8+ installed
- [ ] requirements.txt installed via pip
- [ ] Azure API key added to config.py
- [ ] Azure endpoint URL added to config.py
- [ ] app.py runs without errors
- [ ] Flask API (optional) runs on localhost:5000
- [ ] Can analyze text samples successfully
- [ ] Error handling works for empty inputs
- [ ] Code is properly commented
- [ ] README.md is complete

---

**Happy Moderating! 🛡️**
