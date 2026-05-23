# Azure Content Safety - API Documentation

## Overview

The Content Safety API provides endpoints for analyzing text content for harmful, inappropriate, or abusive material.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. For production use, implement API key authentication:

```python
headers = {
    "X-API-Key": "your_api_key",
    "Content-Type": "application/json"
}
```

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /api/health`

**Description:** Check if the API is running and properly configured.

**Response:**
```json
{
  "status": "healthy",
  "message": "Content Moderator API is running",
  "api_configured": true
}
```

**Status Codes:**
- `200` - API is healthy and configured
- `503` - API is not properly configured

---

### 2. Single Text Analysis

**Endpoint:** `POST /api/moderate`

**Description:** Analyze a single text for harmful content.

**Request Body:**
```json
{
  "text": "Text to analyze"
}
```

**Response (Success):**
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

**Response (Error):**
```json
{
  "status": "error",
  "error_type": "EmptyInput",
  "message": "Text field cannot be empty"
}
```

**Status Codes:**
- `200` - Analysis successful
- `400` - Bad request (missing field, empty text)
- `503` - Service unavailable (credentials not configured)

**Example cURL:**
```bash
curl -X POST http://localhost:5000/api/moderate \
  -H "Content-Type: application/json" \
  -d '{"text": "Sample text"}'
```

**Example Python:**
```python
import requests

response = requests.post(
    'http://localhost:5000/api/moderate',
    json={'text': 'Sample text to analyze'},
    timeout=10
)

data = response.json()
print(f"Status: {data['decision']}")
print(f"Scores: {data['severity_scores']}")
```

---

### 3. Batch Text Analysis

**Endpoint:** `POST /api/moderate-batch`

**Description:** Analyze multiple texts in a single request.

**Request Body:**
```json
{
  "texts": [
    "Text 1 to analyze",
    "Text 2 to analyze",
    "Text 3 to analyze"
  ]
}
```

**Response (Success):**
```json
{
  "status": "success",
  "total_items": 3,
  "results": [
    {
      "text": "Text 1 to analyze",
      "severity_scores": {
        "Hate": 0,
        "Violence": 0,
        "Sexual": 0,
        "SelfHarm": 0
      },
      "decision": "Content Approved ✅",
      "reason": "All categories within acceptable limits"
    },
    {
      "text": "Text 2 to analyze",
      "severity_scores": {
        "Hate": 4,
        "Violence": 0,
        "Sexual": 0,
        "SelfHarm": 0
      },
      "decision": "Content Blocked ❌",
      "reason": "Blocked due to: Hate (Severity: 4)"
    }
  ]
}
```

**Status Codes:**
- `200` - Analysis successful
- `400` - Bad request
- `503` - Service unavailable

**Constraints:**
- Maximum 100 texts per request
- Each text must not be empty
- Texts must be strings

**Example cURL:**
```bash
curl -X POST http://localhost:5000/api/moderate-batch \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Hello world",
      "I hate you",
      "Good day"
    ]
  }'
```

**Example Python:**
```python
import requests

texts = [
    "Hello, how are you?",
    "I will hurt you",
    "This is great!"
]

response = requests.post(
    'http://localhost:5000/api/moderate-batch',
    json={'texts': texts}
)

results = response.json()['results']
for result in results:
    print(f"Text: {result['text']}")
    print(f"Decision: {result['decision']}")
    print()
```

---

## Error Responses

### Error Format
```json
{
  "status": "error",
  "error_type": "ErrorType",
  "message": "Error description"
}
```

### Common Error Types

| Error Type | Status | Meaning |
|-----------|--------|---------|
| `EmptyInput` | 400 | Text field is empty |
| `MissingField` | 400 | Required field is missing |
| `InvalidContentType` | 400 | Content-Type is not application/json |
| `InvalidFormat` | 400 | Request format is invalid |
| `ConfigurationError` | 503 | API credentials not configured |
| `APIError` | 503 | Azure API call failed |
| `LimitExceeded` | 400 | Too many items in batch |
| `UnexpectedError` | 500 | Unexpected server error |

---

## Response Fields

### `severity_scores`
Dictionary containing severity scores for each category (0-6 scale):

```json
{
  "Hate": 0,        // Hate speech detection
  "Violence": 5,    // Violent content detection
  "Sexual": 0,      // Sexual content detection
  "SelfHarm": 0     // Self-harm content detection
}
```

**Severity Scale:**
- `0` - Safe (no harmful content)
- `1-2` - Minor (low severity)
- `3-4` - Moderate (concerning content)
- `5-6` - Severe (highly unsafe content)

### `decision`
- `"Content Approved ✅"` - Text is safe
- `"Content Blocked ❌"` - Text contains harmful content

### `reason`
Explanation of the decision and which categories triggered it.

---

## Usage Examples

### JavaScript/Node.js
```javascript
const axios = require('axios');

async function analyzeContent(text) {
  try {
    const response = await axios.post(
      'http://localhost:5000/api/moderate',
      { text: text },
      { headers: { 'Content-Type': 'application/json' } }
    );
    
    console.log('Decision:', response.data.decision);
    console.log('Scores:', response.data.severity_scores);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

analyzeContent('Sample text');
```

### Java
```java
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import com.google.gson.Gson;

HttpClient client = HttpClient.newHttpClient();

String json = "{\"text\": \"Sample text\"}";

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("http://localhost:5000/api/moderate"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(json))
    .build();

HttpResponse<String> response = client.send(request, 
    HttpResponse.BodyHandlers.ofString());

System.out.println(response.body());
```

### C#/.NET
```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

var client = new HttpClient();

var content = new StringContent(
    "{\"text\": \"Sample text\"}",
    System.Text.Encoding.UTF8,
    "application/json"
);

var response = await client.PostAsync(
    "http://localhost:5000/api/moderate",
    content
);

var result = await response.Content.ReadAsStringAsync();
Console.WriteLine(result);
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, add rate limiting:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/moderate', methods=['POST'])
@limiter.limit("10 per minute")
def moderate_content():
    # ...
```

---

## Best Practices

1. **Error Handling**: Always check the `status` field before processing response
   ```python
   if response.json()['status'] == 'success':
       # Process results
   else:
       # Handle error
   ```

2. **Batch Processing**: Use batch endpoint for multiple texts to improve efficiency
   ```python
   # Bad: Multiple individual requests
   for text in texts:
       response = requests.post('/api/moderate', json={'text': text})
   
   # Good: Single batch request
   response = requests.post('/api/moderate-batch', json={'texts': texts})
   ```

3. **Timeout Handling**: Set appropriate timeouts for requests
   ```python
   response = requests.post(url, json=data, timeout=10)
   ```

4. **Logging**: Log all API calls for audit trails
   ```python
   import logging
   logging.info(f"Analyzed text: {text[:50]}... Decision: {decision}")
   ```

5. **Caching**: Cache results for repeated content
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=1000)
   def get_analysis(text):
       # API call
   ```

---

## Troubleshooting

### 503 Service Unavailable
**Cause**: Azure credentials not configured
**Solution**: Update `config.py` with your API key and endpoint

### 400 Bad Request
**Cause**: Invalid request format
**Solution**: Verify JSON structure and required fields

### Request Timeout
**Cause**: Network connectivity issue
**Solution**: Check internet connection and increase timeout value

### Azure API Error
**Cause**: Invalid API key or endpoint
**Solution**: Verify credentials in Azure Portal

---

## Support

For issues or questions:
1. Check this documentation
2. Review the test examples in [test_examples.py](test_examples.py)
3. Check [README.md](README.md) troubleshooting section
4. Review Azure Content Safety [official documentation](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/)
