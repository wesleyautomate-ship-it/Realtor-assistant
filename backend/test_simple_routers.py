#!/usr/bin/env python3
"""
Simple Router Import Test
========================

Test script to validate that all AURA routers can be imported
and have the expected endpoints defined.
"""

def test_router_imports():
    """Test that all AURA routers can be imported successfully"""
    print("🧪 Testing AURA Router Imports...")
    
    try:
        from app.api.v1.marketing_automation_router import router as marketing_router
        print("✅ Marketing automation router imported successfully")
        print(f"   - Routes: {len(marketing_router.routes)}")
    except Exception as e:
        print(f"❌ Marketing automation router failed: {e}")
    
    try:
        from app.api.v1.cma_reports_router import router as cma_router  
        print("✅ CMA reports router imported successfully")
        print(f"   - Routes: {len(cma_router.routes)}")
    except Exception as e:
        print(f"❌ CMA reports router failed: {e}")
    
    try:
        from app.api.v1.social_media_router import router as social_router
        print("✅ Social media router imported successfully")
        print(f"   - Routes: {len(social_router.routes)}")
    except Exception as e:
        print(f"❌ Social media router failed: {e}")
    
    try:
        from app.api.v1.analytics_router import router as analytics_router
        print("✅ Analytics router imported successfully")
        print(f"   - Routes: {len(analytics_router.routes)}")
    except Exception as e:
        print(f"❌ Analytics router failed: {e}")


def test_router_endpoints():
    """Test that routers have expected endpoints"""
    print("\n🔍 Testing Router Endpoints...")
    
    # Expected endpoints for each router
    expected_endpoints = {
        'marketing': [
            '/templates', '/campaigns', '/campaigns/full-package', 
            '/analytics/summary'
        ],
        'cma': [
            '/reports', '/valuation/quick', '/market/snapshot',
            '/comparables/{property_id}', '/analytics/summary'
        ],
        'social': [
            '/posts', '/campaigns', '/hashtags/research',
            '/schedule/upcoming', '/analytics/summary'
        ],
        'analytics': [
            '/dashboard/overview', '/performance', '/leads',
            '/market/insights', '/reports/generate'
        ]
    }
    
    try:
        from app.api.v1.marketing_automation_router import router as marketing_router
        marketing_paths = [route.path for route in marketing_router.routes if hasattr(route, 'path')]
        print(f"📊 Marketing router has {len(marketing_paths)} endpoints")
        for expected in expected_endpoints['marketing']:
            if any(expected in path for path in marketing_paths):
                print(f"   ✅ {expected}")
            else:
                print(f"   ❌ Missing: {expected}")
    except Exception as e:
        print(f"❌ Could not test marketing endpoints: {e}")
    
    try:
        from app.api.v1.cma_reports_router import router as cma_router
        cma_paths = [route.path for route in cma_router.routes if hasattr(route, 'path')]
        print(f"📊 CMA router has {len(cma_paths)} endpoints")
        for expected in expected_endpoints['cma']:
            if any(expected in path for path in cma_paths):
                print(f"   ✅ {expected}")
            else:
                print(f"   ❌ Missing: {expected}")
    except Exception as e:
        print(f"❌ Could not test CMA endpoints: {e}")
    
    try:
        from app.api.v1.social_media_router import router as social_router
        social_paths = [route.path for route in social_router.routes if hasattr(route, 'path')]
        print(f"📊 Social router has {len(social_paths)} endpoints")
        for expected in expected_endpoints['social']:
            if any(expected in path for path in social_paths):
                print(f"   ✅ {expected}")
            else:
                print(f"   ❌ Missing: {expected}")
    except Exception as e:
        print(f"❌ Could not test social endpoints: {e}")
    
    try:
        from app.api.v1.analytics_router import router as analytics_router
        analytics_paths = [route.path for route in analytics_router.routes if hasattr(route, 'path')]
        print(f"📊 Analytics router has {len(analytics_paths)} endpoints")
        for expected in expected_endpoints['analytics']:
            if any(expected in path for path in analytics_paths):
                print(f"   ✅ {expected}")
            else:
                print(f"   ❌ Missing: {expected}")
    except Exception as e:
        print(f"❌ Could not test analytics endpoints: {e}")


def test_pydantic_models():
    """Test that Pydantic models are correctly defined"""
    print("\n📝 Testing Pydantic Models...")
    
    try:
        from app.api.v1.marketing_automation_router import CampaignCreateRequest, CampaignResponse
        print("✅ Marketing models imported successfully")
    except Exception as e:
        print(f"❌ Marketing models failed: {e}")
    
    try:
        from app.api.v1.cma_reports_router import CMAReportRequest, QuickValuationResponse
        print("✅ CMA models imported successfully")
    except Exception as e:
        print(f"❌ CMA models failed: {e}")
    
    try:
        from app.api.v1.social_media_router import SocialPostRequest, HashtagRecommendations
        print("✅ Social media models imported successfully")
    except Exception as e:
        print(f"❌ Social media models failed: {e}")
    
    try:
        from app.api.v1.analytics_router import PerformanceMetrics, MarketInsights
        print("✅ Analytics models imported successfully")
    except Exception as e:
        print(f"❌ Analytics models failed: {e}")


if __name__ == "__main__":
    print("🚀 PropertyPro AI AURA Router Validation Test")
    print("=" * 50)
    
    test_router_imports()
    test_router_endpoints()
    test_pydantic_models()
    
    print("\n" + "=" * 50)
    print("✅ Router validation test completed!")
    print("\nNext steps:")
    print("1. Start the FastAPI server: uvicorn app.main:app --reload")
    print("2. Visit http://localhost:8000/docs for interactive API documentation")
    print("3. Test endpoints using the Swagger UI or Postman")
    print("4. Implement workflow package manager for AURA orchestration")
