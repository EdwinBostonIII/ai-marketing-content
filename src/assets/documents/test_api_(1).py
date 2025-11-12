#!/usr/bin/env python3
"""
SPLANTS Marketing Engine - API Test Suite
Tests all major endpoints and features
"""

import requests
import json
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8080"
API_KEY = "change-this-to-a-secure-password-123"  # Change this to match your .env

# Headers
headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def test_endpoint(name: str, method: str, endpoint: str, data: Dict[str, Any] = None) -> bool:
    """Test a single endpoint"""
    print(f"\nTesting: {name}")
    print(f"  Endpoint: {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
        else:
            print(f"  ❌ Unsupported method: {method}")
            return False
        
        if response.status_code in [200, 201]:
            print(f"  ✅ Success (Status: {response.status_code})")
            print(f"  Response preview: {str(response.json())[:200]}...")
            return True
        else:
            print(f"  ❌ Failed (Status: {response.status_code})")
            print(f"  Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"  ❌ Exception: {str(e)}")
        return False

def run_tests():
    """Run all API tests"""
    print("================================================")
    print("SPLANTS Marketing Engine - API Test Suite")
    print("================================================")
    
    results = []
    
    # Test 1: Root endpoint
    results.append(test_endpoint(
        "Root Endpoint",
        "GET",
        "/"
    ))
    
    # Test 2: Health check
    results.append(test_endpoint(
        "Health Check",
        "GET",
        "/health"
    ))
    
    # Test 3: Generate blog content
    content_data = {
        "content_type": "blog",
        "topic": "5 Ways AI Can Help Small Businesses Save Time",
        "keywords": ["AI", "small business", "automation", "efficiency"],
        "tone": "professional",
        "target_audience": "Small business owners with 1-10 employees",
        "length": 300,
        "platform": "blog",
        "seo_optimize": True
    }
    
    results.append(test_endpoint(
        "Generate Blog Content",
        "POST",
        "/v1/generate",
        content_data
    ))
    
    # Test 4: Generate social media content
    social_data = {
        "content_type": "social_post",
        "topic": "Announcing our new AI-powered marketing tool!",
        "keywords": ["AI", "marketing", "automation"],
        "tone": "enthusiastic",
        "platform": "twitter",
        "include_hashtags": True
    }
    
    results.append(test_endpoint(
        "Generate Social Post",
        "POST",
        "/v1/generate",
        social_data
    ))
    
    # Test 5: List content
    results.append(test_endpoint(
        "List Content",
        "GET",
        "/v1/content?limit=5"
    ))
    
    # Test 6: Get analytics dashboard
    results.append(test_endpoint(
        "Analytics Dashboard",
        "GET",
        "/v1/analytics/dashboard?days=7"
    ))
    
    # Test 7: Get templates
    results.append(test_endpoint(
        "List Templates",
        "GET",
        "/v1/templates"
    ))
    
    # Test 8: Get cost usage
    results.append(test_endpoint(
        "Cost Usage Report",
        "GET",
        "/v1/costs/usage"
    ))
    
    # Test 9: System status
    results.append(test_endpoint(
        "System Status",
        "GET",
        "/v1/system/status"
    ))
    
    # Test 10: Email content generation
    email_data = {
        "content_type": "email",
        "topic": "Welcome to our AI marketing platform - here's how to get started",
        "tone": "friendly",
        "target_audience": "New users who just signed up",
        "length": 200
    }
    
    results.append(test_endpoint(
        "Generate Email Content",
        "POST",
        "/v1/generate",
        email_data
    ))
    
    # Summary
    print("\n================================================")
    print("TEST SUMMARY")
    print("================================================")
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
    else:
        print(f"❌ {total - passed} test(s) failed")
    
    print("\n📊 Features Tested:")
    print("  • Content generation (blog, social, email)")
    print("  • SEO optimization")
    print("  • Platform-specific formatting")
    print("  • Analytics dashboard")
    print("  • Cost tracking")
    print("  • Template system")
    print("  • System monitoring")

if __name__ == "__main__":
    # Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ API is not responding. Make sure it's running:")
            print("   docker-compose up -d")
            exit(1)
    except:
        print("❌ Cannot connect to API at", BASE_URL)
        print("   Make sure the system is running:")
        print("   docker-compose up -d")
        exit(1)
    
    # Run tests
    run_tests()