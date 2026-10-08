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
    auth_url = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    res = requests.post(auth_url, auth=(FMC_USER, FMC_PASS), verify=False, timeout=10)
    if res.status_code == 204:
        return res.headers.get("DOMAIN_UUID"), {
            "Content-Type": "application/json",
            "X-auth-access-token": res.headers.get("X-auth-access-token")
        }
    raise Exception(f"Auth failed with HTTP {res.status_code}")

def get_all_objects(domain_uuid, headers, endpoint):
    all_items = []
    limit, offset = 1000, 0
    while True:
        url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/{endpoint}?limit={limit}&offset={offset}"
        res = requests.get(url, headers=headers, verify=False)
        if res.status_code != 200:
            break
        items = res.json().get("items", [])
        if not items:
            break
        all_items.extend(items)
        if len(all_items) >= res.json().get("paging", {}).get("count", 0) or len(items) < limit:
            break
        offset += limit
    return all_items

def main():
    domain_uuid, headers = get_fmc_session()
    
    endpoints = {
        "Host": "hosts",
        "Network": "networks",
        "Range": "rangeobjects",
        "NetworkGroup": "networkgroups",
        "FQDN": "fqdns"
    }

    csv_file = "fmc_objects_inventory.csv"
    
    print("[*] Fetching all objects from FMC and exporting to CSV...")
    
    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Type", "UUID"])  # Column Headers

        total = 0
        for cat_name, endpoint in endpoints.items():
            items = get_all_objects(domain_uuid, headers, endpoint)
            for item in items:
                writer.writerow([item.get("name"), item.get("type"), item.get("id")])
            total += len(items)
            print(f"  [+] Exported {len(items)} {cat_name} objects")

    print(f"\n[SUCCESS] Exported {total} objects into '{csv_file}'!")

if __name__ == "__main__":
    main()
