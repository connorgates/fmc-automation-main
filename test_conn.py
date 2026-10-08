import os
import requests
import urllib3
from dotenv import load_dotenv

# Suppress warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load variables from .env
load_dotenv()

FMC_HOST = os.getenv("FMC_HOST")
FMC_USER = os.getenv("FMC_USER")
FMC_PASS = os.getenv("FMC_PASS")

def test_fmc_connection():
    url = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    print(f"[*] Connecting to FMC at https://{FMC_HOST}...")

    try:
        response = requests.post(
            url,
            auth=(FMC_USER, FMC_PASS),
            verify=False, 
            timeout=10
        )

        # HTTP status 204 means successful token generation =)
        if response.status_code == 204:
            token = response.headers.get("X-auth-access-token")
            domain_uuid = response.headers.get("DOMAIN_UUID")
            
            print("\n[+] SUCCESS: Connected & Authenticated!")
            print(f"[+] Domain UUID : {domain_uuid}")
            print(f"[+] Token Snippet: {token[:25]}...")
        else:
            print(f"\n[-] Auth Failed! HTTP Status: {response.status_code}")
            print(f"[-] Response: {response.text}")

    except Exception as e:
        print(f"\n[-] Network error connecting to FMC: {e}")

if __name__ == "__main__":
    test_fmc_connection()
