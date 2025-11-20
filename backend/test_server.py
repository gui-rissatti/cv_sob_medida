"""Quick test script to validate the application startup and endpoints."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

print("=" * 60)
print("BACKEND API HEALTH CHECK")
print("=" * 60)

# Test 1: Health endpoint
print("\n[TEST 1] Testing /health endpoint...")
try:
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 200
    print("✓ Health endpoint working!")
except Exception as e:
    print(f"✗ Health endpoint failed: {e}")

# Test 2: App info
print("\n[TEST 2] Checking app routes...")
routes = [route.path for route in app.routes]
print(f"Available routes: {routes}")

# Test 3: Settings
print("\n[TEST 3] Checking environment settings...")
try:
    from core.config import get_settings
    settings = get_settings()
    print(f"Environment: {settings.environment}")
    print(f"API Port: {settings.api_port}")
    print(f"CORS Origins: {settings.cors_origins}")
    print(f"Google API Key configured: {'Yes' if settings.google_api_key else 'No'}")
    print(f"LangChain Tracing: {settings.langchain_tracing_v2}")
except Exception as e:
    print(f"✗ Settings check failed: {e}")

print("\n" + "=" * 60)
print("DIAGNOSTICS COMPLETE")
print("=" * 60)
