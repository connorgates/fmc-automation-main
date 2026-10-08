import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

FMC_HOST = os.getenv("FMC_HOST")
FMC_USER = os.getenv("FMC_USER")
FMC_PASS = os.getenv("FMC_PASS")

def get_auth():
    url = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    res = requests.post(url, auth=(FMC_USER, FMC_PASS), verify=False, timeout=10)
    if res.status_code == 204:
        return res.headers.get("X-auth-access-token"), res.headers.get("DOMAIN_UUID")
    raise Exception(f"Auth failed with HTTP {res.status_code}: {res.text}")

def get_dynamic_object_id(headers, domain_uuid, object_name):
    """Locate the Object ID for a given Dynamic Object name."""
    dyn_url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/dynamicobjects?expanded=true"
    res = requests.get(dyn_url, headers=headers, verify=False)
    
    if res.status_code == 200:
        items = res.json().get("items", [])
        for item in items:
            if item.get("name").lower() == object_name.lower():
                return item.get("id"), item.get("name")
    return None, object_name

def list_mappings(headers, domain_uuid, obj_id, object_name):
    """Retrieve all IPs currently mapped to the Dynamic Object."""
    map_url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/dynamicobjects/{obj_id}/mappings"
    res = requests.get(map_url, headers=headers, verify=False)
    
    print(f"\n--- Current Mappings for '{object_name}' ---")
    if res.status_code == 200:
        mappings = res.json().get("mappings", [])
        if mappings:
            for ip in mappings:
                print(f"  - {ip}")
            print(f"Total IPs: {len(mappings)}")
        else:
            print("  (No IPs currently mapped)")
    else:
        print(f"[-] Failed to fetch mappings (HTTP {res.status_code})")

def update_mapping(headers, domain_uuid, obj_id, object_name, ip_address, action):
    """Add or remove an IP from the Dynamic Object."""
    map_url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/dynamicobjects/{obj_id}/mappings"
    
    # Payload key is either 'add' or 'remove'
    payload = {
        action: [ip_address]
    }

    verb = "Blocking" if action == "add" else "Unblocking"
    print(f"[*] {verb} {ip_address} on '{object_name}'...")
    
    post_res = requests.post(map_url, headers=headers, json=payload, verify=False)

    if post_res.status_code in (200, 201, 204):
        status_word = "BLOCKED" if action == "add" else "UNBLOCKED"
        print(f"\n[+] SUCCESS: {ip_address} has been {status_word} on '{object_name}'!")
        print("[i] Change applied instantly without full policy deployment.")
    else:
        print(f"[-] Operation failed (HTTP {post_res.status_code}): {post_res.text}")

def main():
    print(f"[*] Authenticating with FMC ({FMC_HOST})...")
    token, domain_uuid = get_auth()
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}

    obj_name = input("Enter Dynamic Object Name [default: InfoSec_Blocklist]: ").strip()
    if not obj_name:
        obj_name = "InfoSec_Blocklist"

    obj_id, exact_name = get_dynamic_object_id(headers, domain_uuid, obj_name)
    if not obj_id:
        print(f"[-] Dynamic Object '{obj_name}' not found on FMC.")
        print("    [!] Create this object first in FMC under: Objects > Object Management > Dynamic Objects")
        return

    while True:
        print(f"\nTarget Dynamic Object: {exact_name}")
        print("  [1] Block / Add IP")
        print("  [2] Unblock / Remove IP")
        print("  [3] View Currently Blocked IPs")
        print("  [4] Exit")
        
        choice = input("\nSelect action (1-4 or Q to Quit): ").strip().lower()

        if choice == "1":
            ip = input("Enter IP address to BLOCK: ").strip()
            if ip:
                update_mapping(headers, domain_uuid, obj_id, exact_name, ip, "add")
        elif choice == "2":
            ip = input("Enter IP address to UNBLOCK: ").strip()
            if ip:
                update_mapping(headers, domain_uuid, obj_id, exact_name, ip, "remove")
        elif choice == "3":
            list_mappings(headers, domain_uuid, obj_id, exact_name)
        elif choice in ("4", "q", "quit", "exit"):
            print("Exiting Dynamic Object Manager...")
            break
        else:
            print("[-] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()