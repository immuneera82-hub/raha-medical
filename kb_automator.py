
import argparse
import sys
from backend.automation.ai_engine import AIEngine
from backend.automation.db_manager import DBManager
from dotenv import load_dotenv

# Load env vars (including Supabase creds)
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Raha Medical Knowledge Base Automator")
    parser.add_argument("--disease", type=str, help="Name of the disease to generate (e.g., 'Breast Cancer')")
    parser.add_argument("--doctor", type=str, help="Name of the doctor to generate (NOT IMPLEMENTED YET)")
    
    args = parser.parse_args()
    
    if not args.disease:
        print("Please provide a disease name: python kb_automator.py --disease 'Disease Name'")
        return

    # 1. Init AI Engine
    ai = AIEngine()
    
    # 2. Generate Content
    print(f"🚀 Starting automation for: {args.disease}")
    content = ai.generate_disease_profile(args.disease)
    
    if not content:
        print("❌ Failed to generate content.")
        return

    # 3. Save to DB
    db = DBManager()
    success = db.save_disease_profile(content)
    
    if success:
        print("✨ DONE! Check your Knowledge Base URL.")
        print(f"URL: /knowledge-base/disease/{content['slug']}")

if __name__ == "__main__":
    main()
