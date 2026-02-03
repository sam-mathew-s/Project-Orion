import os 
import pandas as pd 
from supabase import create_client, Client
from dotenv import load_dotenv

# Initialize connection
load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url,key)

def fetch_all_leads():
    try:
        #query the database
        response = supabase.table("leads").select("*").execute()

        data = response.data 
        if data:
            return pd.DataFrame(data)
        else:
            return pd.DataFrame()
        
    except Exception as e:
        print(f"Error fetching leads: {e}")
        return pd.DataFrame()