"""
Azure AI Content Safety - Content Moderation Application
=========================================================
This application uses Azure AI Content Safety REST API to analyze user-generated
content for inappropriate or harmful text including:
- Hate speech
- Violence
- Sexual content
- Self-harm content

Author: Your Name
Date: 2026
"""

import requests
import json
import sys
from typing import Dict, Tuple, Optional
from config import AZURE_API_KEY, AZURE_ENDPOINT


class ContentModerator:
    """
    A class to handle content moderation using Azure AI Content Safety API.
    
    Attributes:
        api_key (str): Azure API subscription key
        endpoint (str): Azure API endpoint URL
        categories (list): Categories to analyze - Hate, Violence, Sexual, SelfHarm
        severity_threshold (int): Threshold (0-6) above which content is blocked
    """
    
    def __init__(self, api_key: str, endpoint: str, severity_threshold: int = 2):
        """
        Initialize the ContentModerator with API credentials.
        
        Args:
            api_key (str): Your Azure API subscription key
            endpoint (str): Your Azure API endpoint
            severity_threshold (int): Severity level threshold for blocking (default: 2)
        """
        self.api_key = api_key
        self.endpoint = endpoint
        self.categories = ["Hate", "Violence", "Sexual", "SelfHarm"]
        self.severity_threshold = severity_threshold
        
    def analyze_content(self, text: str) -> Optional[Dict]:
        """
        Send text to Azure Content Safety API for analysis.
        
        Args:
            text (str): The text content to analyze
            
        Returns:
            dict: API response with severity scores for each category
            None: If there's an error during API call
            
        Raises:
            ValueError: If text is empty
            requests.exceptions.RequestException: For network errors
        """
        
        # Step 1: Validate input
        if not text or text.strip() == "":
            raise ValueError("❌ Error: Text input cannot be empty!")
        
        # Step 2: Prepare API endpoint URL
        # API version: 2024-09-01 (latest as of this development)
        api_url = f"{self.endpoint}/contentsafety/text:analyze?api-version=2024-09-01"
        
        # Step 3: Prepare request headers
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Step 4: Prepare request payload
        payload = {
            "text": text,
            "categories": self.categories
        }
        
        try:
            print("\n⏳ Analyzing content... Please wait.")
            
            # Step 5: Send POST request to Azure API
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=10  # 10 second timeout for network requests
            )
            
            # Step 6: Check for HTTP errors
            if response.status_code == 401:
                raise ValueError("❌ Authentication Error: Invalid API key. Please check your credentials in config.py")
            elif response.status_code == 400:
                raise ValueError("❌ Bad Request: Invalid input format or missing parameters")
            elif response.status_code != 200:
                raise requests.exceptions.RequestException(
                    f"❌ API Error: HTTP {response.status_code} - {response.text}"
                )
            
            # Step 7: Parse and return JSON response
            result = response.json()
            return result
            
        except requests.exceptions.Timeout:
            print("❌ Error: Request timed out. Please check your internet connection.")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ Error: Cannot connect to Azure API. Please check your endpoint URL and internet connection.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Network Error: {str(e)}")
            return None
        except json.JSONDecodeError:
            print("❌ Error: Invalid response format from API")
            return None
    
    def extract_severity_scores(self, analysis_result: Dict) -> Dict[str, int]:
        """
        Extract severity scores from API response.
        
        Args:
            analysis_result (dict): Response from Azure API
            
        Returns:
            dict: Dictionary with category names as keys and severity scores as values
        """
        severity_scores = {}
        
        # Extract categoriesAnalysis from the API response
        if "categoriesAnalysis" in analysis_result:
            for category_analysis in analysis_result["categoriesAnalysis"]:
                category = category_analysis.get("category", "Unknown")
                severity = category_analysis.get("severity", 0)
                severity_scores[category] = severity
        
        return severity_scores
    
    def decide_content_status(self, severity_scores: Dict[str, int]) -> Tuple[str, str]:
        """
        Determine if content should be approved or blocked based on severity scores.
        
        Args:
            severity_scores (dict): Dictionary with category names and severity scores
            
        Returns:
            tuple: (status, reason) where status is "Approved" or "Blocked"
        """
        
        # Check if any category exceeds the threshold
        blocked_categories = []
        
        for category, severity in severity_scores.items():
            if severity >= self.severity_threshold:
                blocked_categories.append(f"{category} (Severity: {severity})")
        
        # Decision logic
        if blocked_categories:
            reason = f"Blocked due to: {', '.join(blocked_categories)}"
            status = "Content Blocked ❌"
        else:
            reason = "All categories within acceptable limits"
            status = "Content Approved ✅"
        
        return status, reason
    
    def display_results(self, text: str, severity_scores: Dict[str, int], 
                       status: str, reason: str) -> None:
        """
        Display formatted analysis results to the user.
        
        Args:
            text (str): Original input text
            severity_scores (dict): Severity scores for each category
            status (str): Approval/Block status
            reason (str): Explanation for the decision
        """
        
        print("\n" + "=" * 60)
        print("📋 CONTENT MODERATION ANALYSIS RESULTS")
        print("=" * 60)
        
        # Display input text
        print(f"\n📝 User Input:")
        print(f"   \"{text[:100]}{'...' if len(text) > 100 else ''}\"")
        
        # Display severity scores for each category
        print(f"\n📊 Severity Scores (0-6 scale, where 0=safe, 6=highly unsafe):")
        print("-" * 60)
        for category, severity in severity_scores.items():
            severity_bar = "█" * severity + "░" * (6 - severity)
            print(f"   {category:12} | Severity: {severity} | {severity_bar}")
        
        # Display decision
        print(f"\n🔍 Decision: {status}")
        print(f"   Reason: {reason}")
        print("=" * 60 + "\n")
    
    def run_interactive_mode(self) -> None:
        """
        Run the application in interactive mode where users can continuously
        input text for analysis.
        """
        print("\n" + "=" * 60)
        print("🛡️  AZURE AI CONTENT SAFETY MODERATOR")
        print("=" * 60)
        print("Severity Threshold for Blocking: ", self.severity_threshold)
        print("Type 'quit' or 'exit' to end the program")
        print("-" * 60 + "\n")
        
        while True:
            try:
                # Step 1: Get user input
                user_input = input("📝 Enter text to analyze (or 'quit' to exit): ").strip()
                
                # Step 2: Check for exit commands
                if user_input.lower() in ['quit', 'exit']:
                    print("\n👋 Thank you for using Content Moderator. Goodbye!\n")
                    break
                
                # Step 3: Analyze content
                analysis_result = self.analyze_content(user_input)
                
                # Step 4: Handle API errors
                if analysis_result is None:
                    continue
                
                # Step 5: Extract severity scores
                severity_scores = self.extract_severity_scores(analysis_result)
                
                # Step 6: Decide content status
                status, reason = self.decide_content_status(severity_scores)
                
                # Step 7: Display results
                self.display_results(user_input, severity_scores, status, reason)
                
            except ValueError as e:
                print(f"\n{str(e)}\n")
            except Exception as e:
                print(f"\n❌ Unexpected Error: {str(e)}\n")


def main():
    """
    Main entry point for the application.
    """
    
    # Step 1: Check if API credentials are configured
    if not AZURE_API_KEY or not AZURE_ENDPOINT:
        print("\n❌ ERROR: Azure API credentials not configured!")
        print("Please update 'config.py' with your Azure API key and endpoint.")
        print("See README.md for detailed setup instructions.\n")
        sys.exit(1)
    
    # Step 2: Initialize the content moderator
    try:
        moderator = ContentModerator(
            api_key=AZURE_API_KEY,
            endpoint=AZURE_ENDPOINT,
            severity_threshold=2  # Block content with severity >= 2
        )
    except Exception as e:
        print(f"\n❌ Failed to initialize moderator: {str(e)}\n")
        sys.exit(1)
    
    # Step 3: Run interactive mode
    try:
        moderator.run_interactive_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user. Goodbye!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
