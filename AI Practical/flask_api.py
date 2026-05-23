"""
Azure AI Content Safety - Flask Web API
=======================================
This is an optional Flask-based web API version for integrating content
moderation into web applications.

Features:
- REST API endpoints for content analysis
- JSON request/response format
- Health check endpoint
- Error handling and logging
- CORS support for cross-origin requests

Usage:
    python flask_api.py

The API will be available at: http://localhost:5000
"""

from flask import Flask, request, jsonify
import json
import sys
import os

# Import the ContentModerator class from app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import ContentModerator
from config import AZURE_API_KEY, AZURE_ENDPOINT


# Initialize Flask application
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize ContentModerator instance
try:
    moderator = ContentModerator(
        api_key=AZURE_API_KEY,
        endpoint=AZURE_ENDPOINT,
        severity_threshold=2
    )
except Exception as e:
    print(f"❌ Failed to initialize ContentModerator: {str(e)}")
    moderator = None


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        JSON with status and message
        
    Example:
        GET /api/health
        Response: {"status": "healthy", "message": "..."}
    """
    if moderator and AZURE_API_KEY and AZURE_ENDPOINT:
        return jsonify({
            "status": "healthy",
            "message": "Content Moderator API is running",
            "api_configured": True
        }), 200
    else:
        return jsonify({
            "status": "unhealthy",
            "message": "API credentials not configured",
            "api_configured": False
        }), 503


# ============================================================================
# CONTENT MODERATION ENDPOINT
# ============================================================================

@app.route('/api/moderate', methods=['POST'])
def moderate_content():
    """
    Main content moderation endpoint.
    
    Accepts JSON payload with text and returns analysis results.
    
    Request Format:
        {
            "text": "Text to analyze"
        }
    
    Response Format (Success):
        {
            "status": "success",
            "input_text": "...",
            "severity_scores": { ... },
            "decision": "Content Approved ✅ | Content Blocked ❌",
            "reason": "..."
        }
    
    Response Format (Error):
        {
            "status": "error",
            "error_type": "...",
            "message": "..."
        }
    
    Example:
        curl -X POST http://localhost:5000/api/moderate \
             -H "Content-Type: application/json" \
             -d '{"text": "Hello world"}'
    """
    
    try:
        # Step 1: Check if ContentModerator is initialized
        if not moderator:
            return jsonify({
                "status": "error",
                "error_type": "ConfigurationError",
                "message": "API not properly configured. Check your credentials in config.py"
            }), 503
        
        # Step 2: Get JSON payload from request
        if not request.is_json:
            return jsonify({
                "status": "error",
                "error_type": "InvalidContentType",
                "message": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        # Step 3: Validate request payload
        if not data or 'text' not in data:
            return jsonify({
                "status": "error",
                "error_type": "MissingField",
                "message": "Request must contain 'text' field"
            }), 400
        
        text = data.get('text', '').strip()
        
        # Step 4: Check if text is empty
        if not text:
            return jsonify({
                "status": "error",
                "error_type": "EmptyInput",
                "message": "Text field cannot be empty"
            }), 400
        
        # Step 5: Analyze content using ContentModerator
        analysis_result = moderator.analyze_content(text)
        
        # Step 6: Check for API errors
        if analysis_result is None:
            return jsonify({
                "status": "error",
                "error_type": "APIError",
                "message": "Failed to analyze content. Please check your API key and endpoint."
            }), 503
        
        # Step 7: Extract severity scores
        severity_scores = moderator.extract_severity_scores(analysis_result)
        
        # Step 8: Decide content status
        status, reason = moderator.decide_content_status(severity_scores)
        
        # Step 9: Return success response
        return jsonify({
            "status": "success",
            "input_text": text,
            "severity_scores": severity_scores,
            "decision": status,
            "reason": reason
        }), 200
    
    except Exception as e:
        # Handle unexpected errors
        return jsonify({
            "status": "error",
            "error_type": "UnexpectedError",
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500


# ============================================================================
# BATCH MODERATION ENDPOINT (Advanced)
# ============================================================================

@app.route('/api/moderate-batch', methods=['POST'])
def moderate_batch():
    """
    Batch content moderation endpoint.
    
    Analyze multiple texts in a single request.
    
    Request Format:
        {
            "texts": [
                "Text 1 to analyze",
                "Text 2 to analyze",
                "Text 3 to analyze"
            ]
        }
    
    Response Format:
        {
            "status": "success",
            "total_items": 3,
            "results": [
                {
                    "text": "...",
                    "severity_scores": { ... },
                    "decision": "...",
                    "reason": "..."
                },
                ...
            ]
        }
    
    Example:
        curl -X POST http://localhost:5000/api/moderate-batch \
             -H "Content-Type: application/json" \
             -d '{"texts": ["Hello", "Bad word"]}'
    """
    
    try:
        if not moderator:
            return jsonify({
                "status": "error",
                "error_type": "ConfigurationError",
                "message": "API not properly configured"
            }), 503
        
        if not request.is_json:
            return jsonify({
                "status": "error",
                "error_type": "InvalidContentType",
                "message": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({
                "status": "error",
                "error_type": "MissingField",
                "message": "Request must contain 'texts' field (array)"
            }), 400
        
        texts = data.get('texts', [])
        
        if not isinstance(texts, list):
            return jsonify({
                "status": "error",
                "error_type": "InvalidFormat",
                "message": "'texts' must be an array"
            }), 400
        
        if len(texts) == 0:
            return jsonify({
                "status": "error",
                "error_type": "EmptyArray",
                "message": "'texts' array cannot be empty"
            }), 400
        
        if len(texts) > 100:
            return jsonify({
                "status": "error",
                "error_type": "LimitExceeded",
                "message": "Maximum 100 texts per batch request"
            }), 400
        
        # Process each text
        results = []
        for text in texts:
            text = str(text).strip()
            
            if not text:
                results.append({
                    "text": "",
                    "severity_scores": {},
                    "decision": "Error",
                    "reason": "Empty text"
                })
                continue
            
            analysis_result = moderator.analyze_content(text)
            
            if analysis_result is None:
                results.append({
                    "text": text,
                    "severity_scores": {},
                    "decision": "Error",
                    "reason": "Failed to analyze"
                })
                continue
            
            severity_scores = moderator.extract_severity_scores(analysis_result)
            status, reason = moderator.decide_content_status(severity_scores)
            
            results.append({
                "text": text,
                "severity_scores": severity_scores,
                "decision": status,
                "reason": reason
            })
        
        return jsonify({
            "status": "success",
            "total_items": len(texts),
            "results": results
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error_type": "UnexpectedError",
            "message": f"An unexpected error occurred: {str(e)}"
        }), 500


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.route('/', methods=['GET'])
def index():
    """
    Root endpoint providing API documentation.
    """
    return jsonify({
        "name": "Azure Content Safety API",
        "version": "1.0.0",
        "endpoints": {
            "health": {
                "method": "GET",
                "path": "/api/health",
                "description": "Check API status"
            },
            "moderate": {
                "method": "POST",
                "path": "/api/moderate",
                "description": "Analyze single text for harmful content"
            },
            "moderate_batch": {
                "method": "POST",
                "path": "/api/moderate-batch",
                "description": "Analyze multiple texts in one request"
            }
        }
    }), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({
        "status": "error",
        "error_type": "NotFound",
        "message": "Endpoint not found. See GET / for available endpoints"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors."""
    return jsonify({
        "status": "error",
        "error_type": "MethodNotAllowed",
        "message": "HTTP method not allowed for this endpoint"
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    return jsonify({
        "status": "error",
        "error_type": "InternalServerError",
        "message": "Internal server error occurred"
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🌐 AZURE CONTENT SAFETY - FLASK WEB API")
    print("=" * 60)
    
    # Check credentials
    if not AZURE_API_KEY or not AZURE_ENDPOINT:
        print("\n❌ ERROR: Azure API credentials not configured!")
        print("Please update 'config.py' with your Azure credentials.\n")
        sys.exit(1)
    
    print("\n✅ API Credentials: Configured")
    print("📍 Server starting on: http://localhost:5000")
    print("\n📚 Available Endpoints:")
    print("   - GET  /              (API info)")
    print("   - GET  /api/health    (Health check)")
    print("   - POST /api/moderate  (Single text analysis)")
    print("   - POST /api/moderate-batch (Batch analysis)")
    print("\n🧪 Test with:")
    print("   curl http://localhost:5000/api/health")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    # Start Flask server
    app.run(
        host='localhost',
        port=5000,
        debug=True,  # Change to False in production
        use_reloader=True
    )
