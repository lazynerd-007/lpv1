#!/usr/bin/env python3
"""
Incremental router test to identify problematic router combinations
"""
import sys
import traceback
from fastapi import FastAPI

def test_router_combination(router_modules):
    """Test a combination of routers"""
    try:
        print(f"Testing combination: {[r[1] for r in router_modules]}")
        
        # Create a test FastAPI app
        app = FastAPI()
        
        # Import and include routers one by one
        for router_module, router_name in router_modules:
            print(f"  Adding {router_name}...")
            module = __import__(router_module, fromlist=[router_name])
            router = getattr(module, router_name)
            app.include_router(router, prefix="/api/v1")
            print(f"  ✓ {router_name} added successfully")
        
        print(f"✓ Combination successful: {[r[1] for r in router_modules]}")
        return True
        
    except Exception as e:
        print(f"✗ Combination failed: {[r[1] for r in router_modules]} - {e}")
        return False

def main():
    """Test router combinations incrementally"""
    routers = [
        ("app.api.v1.auth", "router"),
        ("app.api.v1.movies", "router"),
        ("app.api.v1.reviews", "router"),
        ("app.api.v1.users", "router"),
        ("app.api.v1.uploads", "router"),
        ("app.api.v1.admin", "router"),
        ("app.api.v1.notifications", "router"),
        ("app.api.v1.analytics", "router"),
    ]
    
    # Test each router individually first
    print("=== Testing individual routers ===")
    for router in routers:
        test_router_combination([router])
    
    print("\n=== Testing cumulative combinations ===")
    # Test cumulative combinations
    for i in range(2, len(routers) + 1):
        combination = routers[:i]
        if not test_router_combination(combination):
            print(f"\n✗ Error first occurred when adding: {routers[i-1][1]}")
            print(f"Previous working combination: {[r[1] for r in routers[:i-1]]}")
            break
    else:
        print("\n✓ All router combinations work!")

if __name__ == "__main__":
    main()