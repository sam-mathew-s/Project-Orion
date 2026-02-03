import os 
from supabase import create_client, Client
from dotenv import load_dotenv 

# Load the keys
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: keys are missing from .env file.")
    print(f" Current Key: {key}")
    print(f" Current Url: {url}")
else:
    print(f"Keys Found. Connecting to: {url[:20]}...")

    try:
        supabase: Client = create_client(url, key)
        print(" Connection Successfull! Orion Mainframe is Online.")
    except Exception as e:
        print(f"Connection Failed! : {e}")
        