from dotenv import load_dotenv
import os

load_dotenv()

url = os.environ.get("SUPABASE_URL", "")
key = os.environ.get("SUPABASE_KEY", "")

print(f"URL_LENGTH: {len(url)}")
if len(url) > 10:
    print(f"URL_START: {url[:8]}...")
else:
    print("URL_START: (too short)")

print(f"KEY_LENGTH: {len(key)}")

if "your-project" in url or "example" in url:
    print("STATUS: PLACEHOLDER_DETECTED")
    
if not url.startswith("https://"):
    print("STATUS: INVALID_PROTOCOL")

try:
    from supabase import create_client
    client = create_client(url, key)
    res = client.table("specialties").select("count", count="exact").execute()
    print("CONNECTION: SUCCESS")
except Exception as e:
    print(f"CONNECTION: FAILED - {str(e)}")
