"""
Configuration File - Azure AI Content Safety
=============================================
This file stores your Azure API credentials.

IMPORTANT: Keep your API key confidential and never share it publicly.
In production, use environment variables instead of hardcoding credentials.
"""

# Replace these with your actual Azure credentials
# Get these values from Azure Portal -> Your Resource -> Keys and Endpoint

# Your Azure API Subscription Key
# Location: Azure Portal -> Your Resource -> Keys and Endpoint -> Key1 or Key2
AZURE_API_KEY = "YOUR_API_KEY_HERE"

# Your Azure API Endpoint
# Location: Azure Portal -> Your Resource -> Keys and Endpoint -> Endpoint
# Format: https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com
AZURE_ENDPOINT = "https://YOUR_RESOURCE_NAME.cognitiveservices.azure.com"

# Optional: Severity threshold for content blocking
# Range: 0-6 (0=safe, 6=highly unsafe)
# Default: 2 (blocks content with severity 2 or higher)
SEVERITY_THRESHOLD = 2

# Optional: Debug mode (set to True for verbose output)
DEBUG_MODE = False
