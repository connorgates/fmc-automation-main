import os
import csv
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

FMC_HOST = os.getenv("FMC_HOST")
FMC_USER = os.getenv("FMC_USER")
FMC_PASS = os.getenv("FMC_PASS")

def get_fmc_session():
    """Authenticates with FMC and returns domain_uuid and session headers."""
    auth_url = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    res = requests.post(auth_url, auth=(FMC_USER, FMC_PASS), verify=False, timeout=10)
    if res.status_code == 204:
        return res.headers.get("DOMAIN_UUID"), {
            "Content-Type": "application/json",
            "X-auth-access-token": res.headers.get("X-auth-access-token")
        }
    raise Exception(f"Auth failed with HTTP {res.status_code}")

def get_unused_objects_by_endpoint(domain_uuid, headers, endpoint):
    """Queries FMC using the built-in 'unusedOnly:true' filter parameter."""
    unused_items = []
    limit, offset = 1000, 0
    
    while True:
        url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/{endpoint}?limit={limit}&offset={offset}&filter=unusedOnly:true"
        res = requests.get(url, headers=headers, verify=False)
        
        if res.status_code != 200:
            break
            
        data = res.json()
        items = data.get("items", [])
        if not items:
            break
            
        unused_items.extend(items)
        total = data.get("paging", {}).get("count", 0)
        
        if len(unused_items) >= total or len(items) < limit:
            break
        offset += limit
        
    return unused_items

def main():
    domain_uuid, headers = get_fmc_session()
    
    endpoints = {
        "Hosts": "hosts",
        "Networks (Subnets)": "networks",
        "Ranges": "rangeobjects",
        "Network Groups": "networkgroups",
        "FQDNs": "fqdns"
    }

    csv_file = "fmc_unused_objects.csv"
    
    print("[*] Scanning FMC database for unused objects across all categories...\n")
    
    total_unused = 0

    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Object Name", "Type", "UUID"])  # Column Headers

        for cat_name, endpoint in endpoints.items():
            items = get_unused_objects_by_endpoint(domain_uuid, headers, endpoint)
            total_unused += len(items)
            
            for item in items:
                writer.writerow([
                    cat_name,
                    item.get("name"),
                    item.get("type"),
                    item.get("id")
                ])
                
            print(f"  [!] {cat_name:<20} : {len(items)} unused object(s) found")

    print("\n" + "=" * 55)
    print(f"  [SUMMARY] TOTAL UNUSED OBJECTS IDENTIFIED : {total_unused}")
    print("=" * 55)
    print(f"\n[SUCCESS] Exported unused objects report to '{csv_file}'!")

if __name__ == "__main__":
    main()
