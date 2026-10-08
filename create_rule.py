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

def get_policy_mappings(domain_uuid, headers):
    """Builds lookup maps for FTD Device -> Policy ID and Policy Name -> Policy ID."""
    device_to_policy_id = {}
    policy_name_to_id = {}

    p_url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/policy/accesspolicies?limit=1000"
    p_res = requests.get(p_url, headers=headers, verify=False)
    if p_res.status_code == 200:
        for p in p_res.json().get("items", []):
            policy_name_to_id[p.get("name").lower()] = (p.get("id"), p.get("name"))

    d_url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/devices/devicerecords?expanded=true&limit=1000"
    d_res = requests.get(d_url, headers=headers, verify=False)
    if d_res.status_code == 200:
        for dev in d_res.json().get("items", []):
            dev_name = dev.get("name", "").lower()
            ac_policy = dev.get("accessPolicy", {})
            if ac_policy.get("id"):
                device_to_policy_id[dev_name] = (ac_policy.get("id"), ac_policy.get("name"))

    return device_to_policy_id, policy_name_to_id

def get_security_zones(domain_uuid, headers):
    """Fetches all Security Zones defined in FMC and maps Name -> Object Dict."""
    zone_map = {}
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/object/securityzones?limit=1000"
    res = requests.get(url, headers=headers, verify=False)
    if res.status_code == 200:
        for z in res.json().get("items", []):
            zone_map[z.get("name").lower()] = z
    return zone_map

def resolve_target_policy(target_str, dev_map, pol_map):
    """Matches an input string against FTD device names or Access Policy names."""
    key = target_str.strip().lower()
    if key in dev_map:
        pol_id, pol_name = dev_map[key]
        return pol_id, pol_name, f"Matched FTD Device '{target_str}'"
    if key in pol_map:
        pol_id, pol_name = pol_map[key]
        return pol_id, pol_name, f"Matched Policy Name '{pol_name}'"
    return None, None, f"Could NOT find FTD device or Policy named '{target_str}'"

def build_zone_container(zone_str, zone_map):
    """Resolves comma-separated zone names into FMC SecurityZone payload structure."""
    if not zone_str or zone_str.strip().upper() in ["ANY", ""]:
        return None
    
    zone_objs = []
    zones = [z.strip() for z in zone_str.split(",")]
    for z in zones:
        z_key = z.lower()
        if z_key in zone_map:
            zone_objs.append({
                "id": zone_map[z_key].get("id"),
                "type": "SecurityZone",
                "name": zone_map[z_key].get("name")
            })
        else:
            print(f"      [WARNING] Zone '{z}' not found in FMC database!")
            
    return {"objects": zone_objs} if zone_objs else None

def build_network_container(ip_or_obj_str):
    """Parses IP/Subnet string or 'ANY' into FMC JSON literals structure."""
    if not ip_or_obj_str or ip_or_obj_str.strip().upper() in ["ANY", ""]:
        return None
    
    literals = []
    items = [x.strip() for x in ip_or_obj_str.split(",")]
    for item in items:
        lit_type = "Network" if "/" in item else "Host"
        literals.append({"type": lit_type, "value": item})
        
    return {"literals": literals}

def add_access_rule(domain_uuid, headers, policy_id, rule_name, action, src_zones_str, src_net, dst_zones_str, dst_net, zone_map):
    """Posts a new Access Rule into the target Access Control Policy."""
    url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/policy/accesspolicies/{policy_id}/accessrules"
    
    payload = {
        "name": rule_name,
        "action": action.upper(),  # ALLOW, BLOCK, TRUST, PERMIT
        "enabled": True,
        "type": "AccessRule"
    }

    src_zones = build_zone_container(src_zones_str, zone_map)
    if src_zones:
        payload["sourceZones"] = src_zones

    dst_zones = build_zone_container(dst_zones_str, zone_map)
    if dst_zones:
        payload["destinationZones"] = dst_zones

    src_container = build_network_container(src_net)
    if src_container:
        payload["sourceNetworks"] = src_container

    dst_container = build_network_container(dst_net)
    if dst_container:
        payload["destinationNetworks"] = dst_container

    res = requests.post(url, headers=headers, json=payload, verify=False)
    return res.status_code, res.json()

def main():
    domain_uuid, headers = get_fmc_session()
    
    print("[*] Pre-fetching policies, devices, and security zones from FMC...")
    dev_map, pol_map = get_policy_mappings(domain_uuid, headers)
    zone_map = get_security_zones(domain_uuid, headers)
    print(f"    [+] Discovered {len(zone_map)} security zones in FMC.\n")

    csv_file = "new_rules.csv"
    if not os.path.exists(csv_file):
        print(f"[!] File '{csv_file}' not found. Please create it first!")
        return

    print(f"[*] Reading rules from '{csv_file}' and processing...")

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            target = row.get("Target_Device_Or_Policy")
            rule_name = row.get("Rule_Name")
            action = row.get("Action", "ALLOW")
            src_zones = row.get("Source_Zones", "ANY")
            src_net = row.get("Source_Networks", "ANY")
            dst_zones = row.get("Destination_Zones", "ANY")
            dst_net = row.get("Destination_Networks", "ANY")

            policy_id, policy_name, match_msg = resolve_target_policy(target, dev_map, pol_map)

            if not policy_id:
                print(f"  [ERROR] Skipping rule '{rule_name}': {match_msg}")
                continue

            print(f"  [*] Creating rule '{rule_name}' in Policy '{policy_name}' ({match_msg})...")
            
            status, response = add_access_rule(
                domain_uuid, headers, policy_id, rule_name, action, 
                src_zones, src_net, dst_zones, dst_net, zone_map
            )
            
            if status in [200, 201]:
                print(f"      [SUCCESS] Rule '{rule_name}' created successfully (HTTP {status})!")
            else:
                err_msg = response.get("error", {}).get("messages", [{}])[0].get("description", "Unknown error")
                print(f"      [FAILED] HTTP {status}: {err_msg}")

    print("\n[*] Rule creation completed!")

if __name__ == "__main__":
    main()
