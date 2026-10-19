#!/usr/bin/env python3
"""OBS WebSocket v5 controller for Python30Days-Day01 profile."""
import json
import sys
import time
import websocket

WS_URL = "ws://127.0.0.1:4455"
MSG_ID = [0]

def next_msg_id():
    MSG_ID[0] += 1
    return str(MSG_ID[0])

def obs_request(action, params=None):
    """Send a request to OBS websocket and return the response."""
    ws = websocket.create_connection(WS_URL, timeout=10)
    
    # Receive Hello
    hello = json.loads(ws.recv())
    if hello.get("op") != 0:
        raise RuntimeError(f"Expected Hello, got: {hello}")
    
    # Send Identify
    identify = {"op": 1, "d": {"rpcVersion": 1}}
    ws.send(json.dumps(identify))
    
    # Receive Identified
    identified = json.loads(ws.recv())
    if identified.get("op") != 2:
        raise RuntimeError(f"Expected Identified, got: {identified}")
    
    # Send request
    req = {"op": 6, "d": {
        "requestType": action,
        "requestId": next_msg_id(),
        "messageId": next_msg_id()
    }}
    if params:
        req["d"]["requestData"] = params
    ws.send(json.dumps(req))
    
    # Receive response
    resp = json.loads(ws.recv())
    ws.close()
    return resp

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None
    try:
        resp = obs_request(action, params)
        print(json.dumps(resp, indent=2))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
