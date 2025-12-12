from backend.database.client import get_supabase_client
from dotenv import load_dotenv
import os

load_dotenv()

def verify():
    print(f"URL: {os.getenv('SUPABASE_URL')}")
    # Partial key mask
    key = os.getenv('SUPABASE_KEY')
    print(f"Key: {key[:5]}...{key[-5:] if key else 'None'}")
    
    supabase = get_supabase_client()
    try:
        res = supabase.table("hospitals").select("*").execute()
        print(f"Count: {len(res.data)}")
        for h in res.data:
            print(f"- {h['slug']} ({h['name_en']}) Partner={h['is_partner']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify()
