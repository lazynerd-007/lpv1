#!/usr/bin/env python3
"""
Simple WebSocket client test for notification system
"""
import asyncio
import json
import websockets
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


async def test_websocket_connection():
    """Test WebSocket connection for notifications"""
    
    # You would need a valid JWT token here
    # For testing, you can get one by logging in through the API
    token = "your-jwt-token-here"  # Replace with actual token
    
    uri = f"ws://localhost:8000/ws/notifications?token={token}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")
            
            # Send a ping
            await websocket.send(json.dumps({
                "type": "ping",
                "timestamp": asyncio.get_event_loop().time()
            }))
            print("📤 Sent ping")
            
            # Listen for messages
            async for message in websocket:
                data = json.loads(message)
                print(f"📥 Received: {data}")
                
                if data.get("type") == "pong":
                    print("✅ Received pong response")
                    
                    # Request unread count
                    await websocket.send(json.dumps({
                        "type": "get_unread_count"
                    }))
                    print("📤 Requested unread count")
                
                elif data.get("type") == "unread_count":
                    print(f"✅ Unread count: {data.get('count')}")
                    break
                    
    except websockets.exceptions.ConnectionClosed:
        print("❌ WebSocket connection closed")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")


if __name__ == "__main__":
    print("Testing WebSocket connection...")
    print("Note: You need to replace 'your-jwt-token-here' with a valid JWT token")
    print("You can get a token by logging in through the API first")
    
    # Uncomment the line below to run the test (after adding a valid token)
    # asyncio.run(test_websocket_connection())