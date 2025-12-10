
from typing import Dict, Any
from backend.database.client import get_supabase_client

class DBManager:
    def __init__(self):
        self.supabase = get_supabase_client()
        
    def save_disease_profile(self, data: Dict[str, Any]) -> bool:
        """
        Saves a disease profile to Supabase 'medical_conditions' table.
        """
        try:
            # Check if exists
            result = self.supabase.table("medical_conditions").select("id").eq("slug", data["slug"]).execute()
            
            if result.data:
                print(f"⚠ Disease '{data['slug']}' already exists. Skipping.")
                return False
                
            # Insert
            self.supabase.table("medical_conditions").insert(data).execute()
            print(f"✅ Successfully saved: {data['name_en']}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving to DB: {e}")
            return False
