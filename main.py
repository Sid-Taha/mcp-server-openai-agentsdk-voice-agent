# mcp-server/main.py
from mcp.server.fastmcp import FastMCP
import requests
import json
import os
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()
STEDI_API_KEY = os.getenv("STEDI_API_KEY")

# URL for Eligibility Check
STEDI_URL = "https://healthcare.us.stedi.com/2024-04-01/change/medicalnetwork/eligibility/v3"

# --- MOCK DATABASE (Verified from Stedi Dashboard) ---
PATIENT_DB = {
    "12345": {
        "first_name": "Jane",
        "last_name": "Doe",
        # Screenshot se confirm hua ID
        "member_id": "AETNA12345",  
        # Screenshot wali Date (04/04/2004) -> YYYYMMDD format
        "dob": "20040404",          
        "payer_id": "60054",        # Aetna
        # Screenshot wala NPI (Safe side ke liye yehi use karein)
        "provider_npi": "1999999984" 
    }
}

mcp = FastMCP(name="healthcare_server", stateless_http=True)

@mcp.tool()
def fetch_claim_status(phone_number: str) -> str:
    """
    Fetches insurance eligibility status via Stedi API.
    Always ask for the phone number first.
    """
    print(f"\n🔎 SEARCH: Looking up patient with Phone: {phone_number}...")

    if not STEDI_API_KEY:
        return "❌ Error: STEDI_API_KEY not found in .env file."

    # 1. Database Lookup
    clean_phone = phone_number.replace(" ", "").replace("-", "")
    patient = None
    
    for key, data in PATIENT_DB.items():
        if key in clean_phone:
            patient = data
            break
    
    if not patient:
        return "❌ Phone number not found in database. Please register first."

    print(f"✅ FOUND DB RECORD: {patient['first_name']} (ID: {patient['member_id']})")

    # 2. Prepare Stedi JSON Payload
    payload = {
        "controlNumber": "123456789",
        "tradingPartnerServiceId": patient['payer_id'], 
        "provider": {
            "npi": patient['provider_npi'],
            "organizationName": "Test Clinic",
            "providerType": "provider" 
        },
        "subscriber": {
            "memberId": patient['member_id'],
            "firstName": patient['first_name'],
            "lastName": patient['last_name'],
            "dateOfBirth": patient['dob']
        }
    }

    headers = {
        "Authorization": f"Key {STEDI_API_KEY}",
        "Content-Type": "application/json"
    }

    # 3. Call Stedi API
    try:
        print("🚀 SENDING REQUEST TO STEDI (ELIGIBILITY)...")
        response = requests.post(STEDI_URL, json=payload, headers=headers)
        
        print(f"📡 Stedi Response Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            # Stedi Response Parsing
            # Hum check karte hain ke data wapas aya ya nahi
            eligibility_id = data.get('eligibilitySearchId', 'N/A')
            
            return f"✅ Success! Insurance for {patient['first_name']} is ACTIVE. (Ref ID: {eligibility_id})"
        
        elif response.status_code == 403:
             return f"❌ Access Denied (403). {response.text}"

        elif response.status_code == 400:
            return f"❌ Bad Request: {response.text}"
            
        else:
            return f"⚠️ API Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"System Connection Error: {str(e)}"

# Start Server
server_start = mcp.streamable_http_app()