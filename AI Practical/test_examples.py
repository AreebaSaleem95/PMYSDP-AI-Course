"""
Test Script - Azure Content Safety
===================================
This script demonstrates how to use the ContentModerator class
with various test cases and scenarios.

Usage:
    python test_examples.py
"""

import sys
from app import ContentModerator
from config import AZURE_API_KEY, AZURE_ENDPOINT


# Sample test texts for demonstration
TEST_CASES = [
    {
        "text": "Hello, how are you doing today?",
        "expected": "Should be APPROVED - normal conversation"
    },
    {
        "text": "I will hurt you if you don't leave me alone",
        "expected": "Should be BLOCKED - contains violence"
    },
    {
        "text": "You are a terrible person and I hate you",
        "expected": "Should be BLOCKED - contains hate speech"
    },
    {
        "text": "This product is great and I love using it",
        "expected": "Should be APPROVED - positive content"
    },
    {
        "text": "I am thinking about harming myself",
        "expected": "Should be BLOCKED - self-harm content"
    },
]


def run_test_suite():
    """
    Run a series of test cases to demonstrate the content moderator.
    """
    
    print("\n" + "=" * 70)
    print("🧪 AZURE CONTENT SAFETY - TEST SUITE")
    print("=" * 70)
    
    # Step 1: Check credentials
    if not AZURE_API_KEY or not AZURE_ENDPOINT:
        print("\n❌ ERROR: Azure credentials not configured!")
        print("Please update 'config.py' first.")
        return
    
    print("\n✅ Credentials: Configured")
    
    # Step 2: Initialize moderator
    try:
        moderator = ContentModerator(
            api_key=AZURE_API_KEY,
            endpoint=AZURE_ENDPOINT,
            severity_threshold=2
        )
        print("✅ Moderator: Initialized\n")
    except Exception as e:
        print(f"\n❌ Failed to initialize: {str(e)}\n")
        return
    
    # Step 3: Run test cases
    print(f"Running {len(TEST_CASES)} test cases...\n")
    print("-" * 70)
    
    for i, test_case in enumerate(TEST_CASES, 1):
        text = test_case["text"]
        expected = test_case["expected"]
        
        print(f"\n📝 Test Case {i}:")
        print(f"   Text: \"{text}\"")
        print(f"   Expected: {expected}")
        print(f"   Analysis:")
        
        try:
            # Analyze content
            analysis_result = moderator.analyze_content(text)
            
            if analysis_result is None:
                print("   ❌ Failed to get analysis")
                continue
            
            # Extract severity scores
            severity_scores = moderator.extract_severity_scores(analysis_result)
            
            # Decide status
            status, reason = moderator.decide_content_status(severity_scores)
            
            # Display scores
            for category, severity in severity_scores.items():
                severity_bar = "█" * severity + "░" * (6 - severity)
                print(f"      {category:12} | {severity} | {severity_bar}")
            
            # Display decision
            print(f"   Result: {status}")
            print(f"   Reason: {reason}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        print("-" * 70)
    
    print("\n" + "=" * 70)
    print("✅ Test suite completed!")
    print("=" * 70 + "\n")


def run_custom_test():
    """
    Allow user to test with custom input.
    """
    
    print("\n" + "=" * 70)
    print("🧪 AZURE CONTENT SAFETY - CUSTOM TEST")
    print("=" * 70)
    
    # Check credentials
    if not AZURE_API_KEY or not AZURE_ENDPOINT:
        print("\n❌ ERROR: Azure credentials not configured!")
        return
    
    # Initialize moderator
    try:
        moderator = ContentModerator(
            api_key=AZURE_API_KEY,
            endpoint=AZURE_ENDPOINT,
            severity_threshold=2
        )
    except Exception as e:
        print(f"\n❌ Failed to initialize: {str(e)}\n")
        return
    
    print("\nEnter custom text to analyze (or 'quit' to exit):\n")
    
    while True:
        user_input = input("📝 Enter text: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("\n👋 Goodbye!\n")
            break
        
        try:
            analysis_result = moderator.analyze_content(user_input)
            
            if analysis_result is None:
                continue
            
            severity_scores = moderator.extract_severity_scores(analysis_result)
            status, reason = moderator.decide_content_status(severity_scores)
            
            moderator.display_results(user_input, severity_scores, status, reason)
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == "--custom":
        # Run custom test mode
        run_custom_test()
    else:
        # Run predefined test suite
        run_test_suite()
        
        # Optionally run custom test
        response = input("\nWould you like to test with custom input? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            run_custom_test()
