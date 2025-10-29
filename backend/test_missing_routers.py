#!/usr/bin/env python3
"""
Test for routers that weren't included in the original test
"""
import sys
import traceback

def test_router(router_module, router_name):
    """Test importing and creating a router"""
    try:
        print(f"Testing {router_name} Router...")
        module = __import__(router_module, fromlist=[router_name])
        router = getattr(module, router_name)
        print(f"✓ {router_name} Router - SUCCESS")
        return True
    except Exception as e:
        print(f"✗ {router_name} Router - FAILED: {e}")
        traceback.print_exc()
        return False

def main():
    """Test missing routers"""
    routers_to_test = [
        ("app.api.v1.auth", "router"),
        ("app.api.v1.movies", "router"),
        ("app.api.v1.reviews", "router"),
    ]
    
    success_count = 0
    total_count = len(routers_to_test)
    
    for router_module, router_name in routers_to_test:
        if test_router(router_module, router_name):
            success_count += 1
    
    print(f"\nRouter testing complete!")
    print(f"Success: {success_count}/{total_count}")

if __name__ == "__main__":
    main()