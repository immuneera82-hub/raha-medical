
from backend.database.client import get_supabase_client
from dotenv import load_dotenv
import os

# Explicitly set env vars because local .env might be broken
os.environ["SUPABASE_URL"] = 'https://rusuwljflrremkszgstn.supabase.co'
os.environ["SUPABASE_KEY"] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ1c3V3bGpmbHJyZW1rc3pnc3RuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0Njk3NjgsImV4cCI6MjA3MDA0NTc2OH0.DFioJz2FNQwpzFEilgagcAFtvQftCkVn4ts-yTjT5vU'

client = get_supabase_client()

try:
    print("Checking 'medical_conditions' table...")
    response = client.table("medical_conditions").select("slug, name_en").execute()
    print(f"Data found: {response.data}")
except Exception as e:
    print(f"Error: {e}")
