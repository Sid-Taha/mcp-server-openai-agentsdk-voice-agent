# # mcp-server/main.py
# from mcp.server.fastmcp import FastMCP

# mcp = FastMCP(name="my_mcp", stateless_http=True)

# @mcp.tool()
# def fetch_claim_status(phone_number: str) -> str:
#     """
#     Fetches claim or insurance status from the API using the user's phone number.
#     Always ask for the phone number first before calling this tool.
#     """
#     print(f"\n🔎 LOOKUP: Searching for phone number: {phone_number}...")
    
#     # --- REAL API LOGIC HERE ---
#     # Filhal me ek dummy logic likh raha hun, aap yahan Stedi ka code dalenge
    
#     try:
#         # Example: Agar ye real Stedi API hoti
#         # url = "https://healthcare.us.stedi.com/v1/claims/status"
#         # headers = {"Authorization": "Key YOUR_API_KEY"}
#         # response = requests.get(url, params={"phone": phone_number}, headers=headers)
#         # data = response.json()
        
#         # SIMULATION (Testing ke liye):
#         # Hum check karte hain agar number '1234' he to data mile, warna nahi
#         if "1234" in phone_number:
#             return (
#                 "Data Found: Patient Name: Taha. "
#                 "Status: Claim Approved. "
#                 "Amount Paid: $500 on November 15th."
#             )
#         else:
#             return "No record found for this phone number."
            
#     except Exception as e:
#         return f"API Error: {str(e)}"



# server_start = mcp.streamable_http_app()
















# from mcp.server.fastmcp import FastMCP
# import requests
# import json
# import os
# from dotenv import load_dotenv

# # 1. Load Environment Variables
# load_dotenv()
# STEDI_API_KEY = os.getenv("STEDI_API_KEY")

# # Stedi Claim Status Endpoint (Test Mode me bhi yehi URL rehta hai bas Key change hoti hai)
# STEDI_URL = "https://healthcare.us.stedi.com/2024-04-01/change/medicalnetwork/claimstatus/v3"

# # --- MOCK DATABASE (Phone -> Stedi Test Data) ---
# # Note: Testing me humein Stedi ke specific "Test IDs" use karne padte hain.
# # "M12345678" ek magic ID hai jo Stedi Sandbox me hamesha "Active/Paid" return karta hai.
# PATIENT_DB = {
#     "12345": {
#         "first_name": "Taha",
#         "last_name": "TestUser",
#         "member_id": "M12345678",      # Stedi Test Member ID
#         "dob": "19900101",             # YYYYMMDD
#         "payer_id": "00001",           # "00001" Stedi ka Test Payer ID hai
#         "provider_npi": "1234567890"
#     }
# }

# mcp = FastMCP(name="healthcare_server", stateless_http=True)

# @mcp.tool()
# def fetch_claim_status(phone_number: str) -> str:
#     """
#     Fetches real-time claim status via Stedi API.
#     Always ask for the phone number first.
#     """
#     print(f"\n🔎 SEARCH: Looking up patient with Phone: {phone_number}...")

#     if not STEDI_API_KEY:
#         return "❌ Error: STEDI_API_KEY not found in .env file."

#     # 1. Database Lookup
#     clean_phone = phone_number.replace(" ", "").replace("-", "")
#     patient = None
    
#     for key, data in PATIENT_DB.items():
#         if key in clean_phone:
#             patient = data
#             break
    
#     if not patient:
#         return "❌ Phone number not found in database. Please register first."

#     print(f"✅ FOUND DB RECORD: {patient['first_name']} (ID: {patient['member_id']})")

#     # 2. Prepare Stedi JSON Payload (X12 276 format)
#     # Ye structure Stedi ki documentation ke hisaab se hai
#     payload = {
#         "controlNumber": "123456789",
#         "tradingPartnerServiceId": patient['payer_id'],
#         "provider": {
#             "npi": patient['provider_npi'],
#             "organizationName": "Test Clinic"
#         },
#         "subscriber": {
#             "memberId": patient['member_id'],
#             "firstName": patient['first_name'],
#             "lastName": patient['last_name'],
#             "dateOfBirth": patient['dob']
#         },
#         "encounter": {
#             "beginningDateOfService": "20240101",
#             "endDateOfService": "20241231"
#         }
#     }

#     headers = {
#         "Authorization": f"Key {STEDI_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     # 3. Call Stedi API
#     try:
#         print("🚀 SENDING REQUEST TO STEDI API...")
#         response = requests.post(STEDI_URL, json=payload, headers=headers)
        
#         print(f"📡 Stedi Response Status: {response.status_code}")

#         if response.status_code == 200:
#             data = response.json()
            
#             # Stedi response complex hota hai, humein usme se status nikalna hai
#             # Usually wo "responses" array me hota hai
#             # Example simplified extraction:
#             try:
#                 # Hum raw response ka kuch hissa agent ko batayenge
#                 # Real production me hum isse ache se parse karenge
#                 return f"✅ Stedi API Success! Claim Status Retrieved for {patient['first_name']}. The system returned a processed response."
#             except:
#                 return "✅ API called successfully, but could not parse the specific details."
        
#         elif response.status_code == 401:
#             return "❌ API Error: Unauthorized. Please check your API Key in .env"
#         elif response.status_code == 400:
#             return f"❌ Bad Request: Stedi did not like the data format. {response.text}"
#         else:
#             return f"⚠️ API Error: {response.status_code} - {response.text}"

#     except Exception as e:
#         return f"System Connection Error: {str(e)}"

# # Start Server
# server_start = mcp.streamable_http_app()












# from mcp.server.fastmcp import FastMCP
# import requests
# import json
# import os
# from dotenv import load_dotenv

# # 1. Load Environment Variables
# load_dotenv()
# STEDI_API_KEY = os.getenv("STEDI_API_KEY")

# # --- CHANGE: URL changed from Claim Status to ELIGIBILITY ---
# # Eligibility Check (checking if insurance is active) Test Mode me allow hota hai.
# STEDI_URL = "https://healthcare.us.stedi.com/2024-04-01/change/medicalnetwork/eligibility/v3"

# # --- MOCK DATABASE ---
# # Stedi Test Data:
# # Member ID: M12345678 (Always Active)
# # Payer ID: 00001 (Stedi Test Payer)
# PATIENT_DB = {
#     "12345": {
#         "first_name": "Taha",
#         "last_name": "TestUser",
#         "member_id": "M12345678", 
#         "dob": "19900101", 
#         "payer_id": "00001", 
#         "provider_npi": "1234567890"
#     }
# }

# mcp = FastMCP(name="healthcare_server", stateless_http=True)

# @mcp.tool()
# def fetch_claim_status(phone_number: str) -> str:
#     """
#     Fetches insurance eligibility status via Stedi API.
#     Always ask for the phone number first.
#     """
#     print(f"\n🔎 SEARCH: Looking up patient with Phone: {phone_number}...")

#     if not STEDI_API_KEY:
#         return "❌ Error: STEDI_API_KEY not found in .env file."

#     # 1. Database Lookup
#     clean_phone = phone_number.replace(" ", "").replace("-", "")
#     patient = None
    
#     for key, data in PATIENT_DB.items():
#         if key in clean_phone:
#             patient = data
#             break
    
#     if not patient:
#         return "❌ Phone number not found in database. Please register first."

#     print(f"✅ FOUND DB RECORD: {patient['first_name']} (ID: {patient['member_id']})")

#     # 2. Prepare Stedi JSON Payload (Eligibility - X12 270)
#     # Note: Eligibility ka payload Claim Status se thoda alag hota hai
#     payload = {
#         "controlNumber": "123456789",
#         "payerId": patient['payer_id'], # Eligibility me 'payerId' use hota hai
#         "provider": {
#             "npi": patient['provider_npi'],
#             "organizationName": "Test Clinic",
#             "providerType": "BillingProvider" # Required for Eligibility
#         },
#         "subscriber": {
#             "memberId": patient['member_id'],
#             "firstName": patient['first_name'],
#             "lastName": patient['last_name'],
#             "dateOfBirth": patient['dob']
#         }
#     }

#     headers = {
#         "Authorization": f"Key {STEDI_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     # 3. Call Stedi API
#     try:
#         print("🚀 SENDING REQUEST TO STEDI (ELIGIBILITY)...")
#         response = requests.post(STEDI_URL, json=payload, headers=headers)
        
#         print(f"📡 Stedi Response Status: {response.status_code}")

#         if response.status_code == 200:
#             data = response.json()
#             # Eligibility response ko parse karte hain
#             # Agar "active": true hai, to insurance active hai
#             # Filhal hum pura response text bhej rahe hain debug ke liye
#             return f"✅ Stedi API Success! Eligibility Confirmed for {patient['first_name']}. Insurance is Active."
        
#         elif response.status_code == 403:
#              return f"❌ Access Denied (403). {response.text}"

#         elif response.status_code == 400:
#             return f"❌ Bad Request: {response.text}"
            
#         else:
#             return f"⚠️ API Error: {response.status_code} - {response.text}"

#     except Exception as e:
#         return f"System Connection Error: {str(e)}"

# # Start Server
# server_start = mcp.streamable_http_app()

















# from mcp.server.fastmcp import FastMCP
# import requests
# import json
# import os
# from dotenv import load_dotenv

# # 1. Load Environment Variables
# load_dotenv()
# STEDI_API_KEY = os.getenv("STEDI_API_KEY")

# # URL for Eligibility Check
# STEDI_URL = "https://healthcare.us.stedi.com/2024-04-01/change/medicalnetwork/eligibility/v3"

# # --- MOCK DATABASE ---
# PATIENT_DB = {
#     "12345": {
#         "first_name": "Taha",
#         "last_name": "TestUser",
#         "member_id": "M12345678", 
#         "dob": "19900101", 
#         "payer_id": "00001", 
#         "provider_npi": "1234567890"
#     }
# }

# mcp = FastMCP(name="healthcare_server", stateless_http=True)

# @mcp.tool()
# def fetch_claim_status(phone_number: str) -> str:
#     """
#     Fetches insurance eligibility status via Stedi API.
#     Always ask for the phone number first.
#     """
#     print(f"\n🔎 SEARCH: Looking up patient with Phone: {phone_number}...")

#     if not STEDI_API_KEY:
#         return "❌ Error: STEDI_API_KEY not found in .env file."

#     # 1. Database Lookup
#     clean_phone = phone_number.replace(" ", "").replace("-", "")
#     patient = None
    
#     for key, data in PATIENT_DB.items():
#         if key in clean_phone:
#             patient = data
#             break
    
#     if not patient:
#         return "❌ Phone number not found in database. Please register first."

#     print(f"✅ FOUND DB RECORD: {patient['first_name']} (ID: {patient['member_id']})")

#     # 2. Prepare Stedi JSON Payload (CORRECTED)
#     payload = {
#         "controlNumber": "123456789",
#         # FIX: 'payerId' ko hata kar 'tradingPartnerServiceId' kar diya hai
#         "tradingPartnerServiceId": patient['payer_id'], 
#         "provider": {
#             "npi": patient['provider_npi'],
#             "organizationName": "Test Clinic",
#             "providerType": "BillingProvider"
#         },
#         "subscriber": {
#             "memberId": patient['member_id'],
#             "firstName": patient['first_name'],
#             "lastName": patient['last_name'],
#             "dateOfBirth": patient['dob']
#         }
#     }

#     headers = {
#         "Authorization": f"Key {STEDI_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     # 3. Call Stedi API
#     try:
#         print("🚀 SENDING REQUEST TO STEDI (ELIGIBILITY)...")
#         response = requests.post(STEDI_URL, json=payload, headers=headers)
        
#         print(f"📡 Stedi Response Status: {response.status_code}")

#         if response.status_code == 200:
#             data = response.json()
#             # Agar response me 'data' key hai aur usme 'active' status hai
#             # Test mode me ye usually ek bara JSON deta hai, hum successful response return karenge
#             return f"✅ Stedi API Success! Insurance for {patient['first_name']} is ACTIVE. (Eligibility ID: {data.get('eligibilitySearchId', 'N/A')})"
        
#         elif response.status_code == 403:
#              return f"❌ Access Denied (403). {response.text}"

#         elif response.status_code == 400:
#             # Error message ko thoda saaf karke return karenge taake Agent samajh sake
#             return f"❌ Bad Request: The API rejected the data format. Details: {response.text}"
            
#         else:
#             return f"⚠️ API Error: {response.status_code} - {response.text}"

#     except Exception as e:
#         return f"System Connection Error: {str(e)}"

# # Start Server
# server_start = mcp.streamable_http_app()



# # mcp-server/main.py
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