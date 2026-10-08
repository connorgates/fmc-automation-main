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

def extract_names_and_literals(field_dict):
    """Extract object names and raw literal values from rule field dictionaries."""
    if not field_dict:
        return ["Any"]
    
    results = []
    # Named objects or network groups
    for obj in field_dict.get("objects", []):
        results.append(obj.get("name", obj.get("id")))
    
    # Inline literal IPs, subnets, or port ranges
    for lit in field_dict.get("literals", []):
        results.append(lit.get("value", str(lit)))
        
    return results if results else ["Any"]

def search_rules():
    print(f"[*] Authenticating with FMC ({FMC_HOST})...")
    token, domain_uuid = get_auth()
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}

    print("[*] Fetching Access Control Policies...")
    policies_url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/policy/accesspolicies"
    pol_res = requests.get(policies_url, headers=headers, verify=False)
    policies = pol_res.json().get("items", []) if pol_res.status_code == 200 else []

    if not policies:
        print("[-] No Access Control Policies found.")
        return

    # Display Policy Menu
    print("\n--- Available Access Control Policies ---")
    for idx, pol in enumerate(policies, 1):
        print(f"  [{idx}] {pol['name']}")
    print("  [*] All Policies")

    policy_choice = input("\nSelect Policy number or name (or '*' / Enter for All): ").strip()

    # Filter Policies based on selection
    selected_policies = []
    if not policy_choice or policy_choice == "*":
        selected_policies = policies
    elif policy_choice.isdigit() and 1 <= int(policy_choice) <= len(policies):
        selected_policies = [policies[int(policy_choice) - 1]]
    else:
        # Match by policy name substring
        matched = [p for p in policies if policy_choice.lower() in p["name"].lower()]
        if matched:
            selected_policies = matched
        else:
            print(f"[-] No policy found matching '{policy_choice}'. Searching across ALL policies.")
            selected_policies = policies

    # Keyword Prompt
    env_keyword = os.getenv("SEARCH_KEYWORD", "").strip()
    if env_keyword:
        prompt_text = f"Enter keyword to search (or '*' / Enter for all rules) [{env_keyword}]: "
    else:
        prompt_text = "Enter keyword, object name, or IP to search (or '*' / Enter for all rules): "
        
    user_input = input(prompt_text).strip()
    keyword = user_input if user_input else (env_keyword if env_keyword else "*")

    search_all = (keyword == "*")
    total_matches = 0

    print(f"\n[*] Searching across {len(selected_policies)} policy/policies for keyword: '{keyword}'")
    print("=" * 75)

    for pol in selected_policies:
        policy_id = pol["id"]
        policy_name = pol["name"]

        rules_url = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain_uuid}/policy/accesspolicies/{policy_id}/accessrules?expanded=true&limit=1000"
        rules_res = requests.get(rules_url, headers=headers, verify=False)
        rules = rules_res.json().get("items", []) if rules_res.status_code == 200 else []

        for rule in rules:
            rule_str = str(rule)

            if search_all or (keyword.lower() in rule_str.lower()):
                total_matches += 1
                
                rule_name = rule.get("name", "Unnamed Rule")
                action = rule.get("action", "UNKNOWN")
                enabled = rule.get("enabled", True)

                # Extract Source details
                src_zones = extract_names_and_literals(rule.get("sourceZones"))
                src_nets = extract_names_and_literals(rule.get("sourceNetworks"))
                src_ports = extract_names_and_literals(rule.get("sourcePorts"))

                # Extract Destination details
                dst_zones = extract_names_and_literals(rule.get("destinationZones"))
                dst_nets = extract_names_and_literals(rule.get("destinationNetworks"))
                dst_ports = extract_names_and_literals(rule.get("destinationPorts"))

                print(f"Policy : {policy_name}")
                print(f"Rule   : {rule_name}  (Action: {action} | Enabled: {enabled})")
                print("  SOURCE:")
                print(f"    - Zones    : {', '.join(src_zones)}")
                print(f"    - Networks : {', '.join(src_nets)}")
                print(f"    - Ports    : {', '.join(src_ports)}")
                print("  DESTINATION:")
                print(f"    - Zones    : {', '.join(dst_zones)}")
                print(f"    - Networks : {', '.join(dst_nets)}")
                print(f"    - Ports    : {', '.join(dst_ports)}")
                print("-" * 75)

    print(f"\n[+] Finished. Found {total_matches} rule(s) matching '{keyword}'.")

if __name__ == "__main__":
    search_rules()