import requests
import socket

# Force Python to prioritize IPv6 for this connection
requests.packages.urllib3.util.connection.HAS_IPV6 = True

CLIENT_ID = "b826e72b8a094b7abbbbe03569a28dcd"
CLIENT_SECRET = "0693d8c758424dae80d7c47c824083c2"

def test_ipv6_connection():
    url = "https://oauth.fatsecret.com/connect/token"
    print("🛰️ Attempting handshake via IPv6...")
    
    try:
        response = requests.post(
            url, 
            auth=(CLIENT_ID, CLIENT_SECRET),
            data={"grant_type": "client_credentials", "scope": "basic"}
        )
        
        if response.status_code == 200:
            print("✅ SUCCESS! The IPv6 whitelist worked.")
            print(f"Access Token: {response.json().get('access_token')[:10]}...")
        else:
            print(f"❌ Status {response.status_code}")
            # If this is still HTML, we wait 10 mins for the whitelist to refresh
            if "html" in response.text:
                print("Server still thinks you're a stranger. Wait 10 minutes.")
            else:
                print(f"Server Response: {response.text}")
                
    except Exception as e:
        print(f"📡 Connection Error: {e}")

if __name__ == "__main__":
    test_ipv6_connection()