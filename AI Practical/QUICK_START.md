# Quick Start Guide 🚀

## 5-Minute Setup

### 1️⃣ Install Dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

### 2️⃣ Get Azure Credentials (2 minutes)

1. Go to https://portal.azure.com
2. Create **Content Safety** resource
3. Go to **Keys and Endpoint**
4. Copy the **Key** and **Endpoint URL**

### 3️⃣ Configure Credentials (1 minute)

Edit `config.py`:
```python
AZURE_API_KEY = "your_key_here"
AZURE_ENDPOINT = "https://your_resource.cognitiveservices.azure.com"
```

## Run the Application

### Terminal Mode (Interactive)
```bash
python app.py
```

### Web API Mode
```bash
python flask_api.py
```

### Test Mode
```bash
python test_examples.py
```

## API Quick Test

### Using Python requests
```python
import requests

response = requests.post(
    'http://localhost:5000/api/moderate',
    json={'text': 'I will hurt you'}
)

print(response.json())
```

### Using cURL
```bash
curl -X POST http://localhost:5000/api/moderate \
  -H "Content-Type: application/json" \
  -d '{"text": "I will hurt you"}'
```

## Severity Scores Reference

| Score | Level | Action |
|-------|-------|--------|
| 0 | Safe | ✅ Approved |
| 1-2 | Minor | ✅ Approved* |
| 3-4 | Moderate | ❌ Blocked |
| 5-6 | Severe | ❌ Blocked |

*Default threshold is 2, change in `app.py` line 133

## Troubleshooting

### Error: Invalid API Key
→ Check Azure Portal credentials

### Error: Connection Timeout
→ Check internet connection and endpoint URL

### Error: ModuleNotFoundError
→ Run `pip install -r requirements.txt`

## Next Steps

- Read [README.md](README.md) for complete documentation
- Check [test_examples.py](test_examples.py) for code examples
- Review [flask_api.py](flask_api.py) for API integration

---

**Need help?** Check README.md → Troubleshooting section
