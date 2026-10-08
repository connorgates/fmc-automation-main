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
    """Authenticates with FMC and returns domain_uuid and headers."""
    auth_url = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    res = requests.post(auth_url, auth=(FMC_USER, FMC_PASS), verify=False, timeout=10)
    if res.status_code == 204:
        return res.headers.get("DOMAIN_UUID"), {
            "Content-Type": "application/json",
            "X-auth-access-token": res.headers.get("X-auth-access-token")
        }
    raise Exception(f"Auth failed with HTTP {res.status_code}")

def get_all_devices(domain_uuid, headers):
    """Paginates through FMC device records with expanded details."""
    all_devices = []
    limit, offset = 1000, 0

    while True:
        url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/devices/devicerecords?expanded=true&limit={limit}&offset={offset}"
        res = requests.get(url, headers=headers, verify=False)

        if res.status_code != 200:
            break

        data = res.json()
        items = data.get("items", [])
        if not items:
            break

        all_devices.extend(items)
        total = data.get("paging", {}).get("count", 0)

        if len(all_devices) >= total or len(items) < limit:
            break
        offset += limit

    return all_devices

def main():
    domain_uuid, headers = get_fmc_session()
    
    csv_file = "fmc_device_inventory.csv"
    
    print("[*] Fetching FTD device inventory and health status from FMC...\n")
    devices = get_all_devices(domain_uuid, headers)

    headers_row = [
        "Device Name",
        "Management IP",
        "Model",
        "Software Version",
        "Health Status",
        "Access Policy",
        "Device ID"
    ]

    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers_row)

        for dev in devices:
            name = dev.get("name", "Unknown")
            ip = dev.get("hostName", "N/A")
            model = dev.get("model", "N/A")
            sw_version = dev.get("sw_version", "N/A")
            health_status = dev.get("healthStatus", "N/A")
            
            # Extract access policy assignment if present
            ac_policy = dev.get("accessPolicy", {}).get("name", "N/A")
            device_id = dev.get("id", "N/A")

            writer.writerow([
                name,
                ip,
                model,
                sw_version,
                health_status,
                ac_policy,
                device_id
            ])

            print(f"  [+] {name:<30} | {model:<20} | v{sw_version:<8} | Health: {health_status}")

    print("\n" + "=" * 65)
    print(f"  [SUCCESS] Exported {len(devices)} device records into '{csv_file}'!")
    print("=" * 65)

if __name__ == "__main__":
    main()
