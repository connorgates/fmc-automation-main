import os
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

FMC_HOST = os.getenv("FMC_HOST")
FMC_USER = os.getenv("FMC_USER")
FMC_PASS = os.getenv("FMC_PASS")

TARGET_IPS = ["x.x.x.x", "x.x.x.x", "x.x.x.x"]
REF_IPS = ["x.x.x.x", "x.x.x.x"]
CHECK_IP = "x.x.x.x"

def get_auth():
    url = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    res = requests.post(url, auth=(FMC_USER, FMC_PASS), verify=False, timeout=10)
    if res.status_code == 204:
        return res.headers.get("X-auth-access-token"), res.headers.get("DOMAIN_UUID")
    raise Exception(f"Auth failed with HTTP {res.status_code}: {res.text}")

def audit_ip_rules():
    token, domain_uuid = get_auth()
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}

    print("[*] Resolving FMC network objects for target IPs...")
    
    # Map network objects/hosts in FMC to target IPs
    obj_url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/networkaddresses?expanded=true&limit=1000"
    obj_res = requests.get(obj_url, headers=headers, verify=False)
    objects = obj_res.json().get("items", []) if obj_res.status_code == 200 else []

    ip_identifiers = {ip: {ip} for ip in TARGET_IPS}
    
    for obj in objects:
        obj_id = obj.get("id")
        obj_name = obj.get("name")
        obj_val = obj.get("value", "")
        
        for ip in TARGET_IPS:
            if ip in str(obj_val) or ip in str(obj_name):
                if obj_id:
                    ip_identifiers[ip].add(obj_id)
                if obj_name:
                    ip_identifiers[ip].add(obj_name)

    print("[*] IP Mappings resolved:")
    for ip, idents in ip_identifiers.items():
        print(f"    - {ip}: {list(idents)}")

    # Fetch Access Control Policies
    policies_url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/policy/accesspolicies"
    pol_res = requests.get(policies_url, headers=headers, verify=False)
    policies = pol_res.json().get("items", []) if pol_res.status_code == 200 else []

    if not policies:
        print("[-] No Access Policies found.")
        return

    print(f"\n[*] Auditing Access Rules across {len(policies)} policy/policies...\n")

    matches_found = 0
    for pol in policies:
        policy_id = pol["id"]
        policy_name = pol["name"]

        rules_url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/policy/accesspolicies/{policy_id}/accessrules?expanded=true&limit=1000"
        rules_res = requests.get(rules_url, headers=headers, verify=False)
        rules = rules_res.json().get("items", []) if rules_res.status_code == 200 else []

        for rule in rules:
            rule_name = rule.get("name", "Unnamed Rule")
            rule_str = str(rule)

            matched_ref_ips = [
                ip for ip in REF_IPS
                if any(ident in rule_str for ident in ip_identifiers[ip])
            ]

            if matched_ref_ips:
                matches_found += 1
                has_check_ip = any(ident in rule_str for ident in ip_identifiers[CHECK_IP])

                src_zones = [z.get("name") for z in rule.get("sourceZones", {}).get("objects", [])]
                dst_zones = [z.get("name") for z in rule.get("destinationZones", {}).get("objects", [])]
                action = rule.get("action", "UNKNOWN")

                print(f"Policy: '{policy_name}' | Rule: '{rule_name}' (Action: {action})")
                print(f"  Source Zones : {src_zones or ['Any']}")
                print(f"  Dest Zones   : {dst_zones or ['Any']}")
                print(f"  Reference IPs: {matched_ref_ips}")
                print(f"  Status       : {'[MATCH] ' + CHECK_IP + ' is included' if has_check_ip else '[MISSING] ' + CHECK_IP + ' NOT found'}")
                print("-" * 65)

    if matches_found == 0:
        print("[-] No rules were found containing 128.226.157.31 or 128.226.157.33.")

if __name__ == "__main__":
    audit_ip_rules()
