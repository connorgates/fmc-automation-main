import csv
import ipaddress
import os
import sys

import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

FMC_HOST = os.getenv("FMC_HOST")
FMC_USER = os.getenv("FMC_USER")
FMC_PASS = os.getenv("FMC_PASS")

DEFAULT_CSV = "fmc_hosts.csv"   # columns: Name,Value
CHUNK = 100                     # hosts per bulk POST (FMC allows up to 1000)


def get_auth():
    url = f"https://{FMC_HOST}/api/fmc_platform/v1/auth/generatetoken"
    res = requests.post(url, auth=(FMC_USER, FMC_PASS), verify=False, timeout=10)
    if res.status_code == 204:
        return res.headers.get("X-auth-access-token"), res.headers.get("DOMAIN_UUID")
    raise Exception(f"Auth failed with HTTP {res.status_code}: {res.text}")


def get_all(url, headers):
    """Fetch every item from a paged FMC list endpoint."""
    items, offset, limit = [], 0, 1000
    while True:
        res = requests.get(f"{url}?expanded=true&limit={limit}&offset={offset}",
                           headers=headers, verify=False, timeout=30)
        res.raise_for_status()
        batch = res.json().get("items", [])
        items.extend(batch)
        if len(batch) < limit:
            return items
        offset += limit


def load_csv(path):
    """Read Name,Value rows, validating IPs and dropping duplicate names."""
    rows, seen = [], set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            name = (row.get("Name") or "").strip()
            value = (row.get("Value") or "").strip()
            try:
                ipaddress.ip_address(value)
            except ValueError:
                print(f"[!] Line {i}: skipping '{name}' - invalid IP '{value}'")
                continue
            if not name or name.lower() in seen:
                print(f"[!] Line {i}: skipping duplicate/blank name '{name}'")
                continue
            seen.add(name.lower())
            rows.append({"name": name, "type": "Host", "value": value})
    return rows


def create_group(base, headers, group_name, rows):
    """Create a network group of the CSV hosts, reusing existing objects by IP."""
    hosts = get_all(f"{base}/object/hosts", headers)
    by_value, by_name = {}, {}
    for h in hosts:
        by_value.setdefault(h.get("value"), h)
        by_name[h["name"].lower()] = h

    members, missing = [], []
    for r in rows:
        obj = by_value.get(r["value"])   # match on IP only, never on name
        if obj:
            members.append({"type": "Host", "id": obj["id"], "name": obj["name"]})
        else:
            missing.append(r["name"])
    if missing:
        print(f"[!] Not in FMC, left out of group: {', '.join(missing)}")

    res = requests.post(f"{base}/object/networkgroups", headers=headers, verify=False,
                        json={"name": group_name, "type": "NetworkGroup", "objects": members})
    if res.status_code in (200, 201):
        print(f"[+] Group '{group_name}' created with {len(members)} hosts.")
    else:
        print(f"[-] Group creation failed ({res.status_code}): {res.text[:500]}")


def main():
    path = input(f"CSV file [{DEFAULT_CSV}]: ").strip() or DEFAULT_CSV
    if not os.path.exists(path):
        print(f"[-] File not found: {path}")
        return

    hosts = load_csv(path)
    print(f"[*] Loaded {len(hosts)} valid hosts from {path}")

    token, domain = get_auth()
    headers = {"X-auth-access-token": token, "Content-Type": "application/json"}
    base = f"https://{FMC_HOST}/api/fmc_config/v1/domain/{domain}"

    # Compare against what already exists in FMC (nothing is ever overwritten)
    existing = get_all(f"{base}/object/hosts", headers)
    by_name = {h["name"].lower(): h for h in existing}
    by_value = {}
    for h in existing:
        by_value.setdefault(h.get("value"), h)

    to_create = []
    for h in hosts:
        same_name = by_name.get(h["name"].lower())
        same_ip = by_value.get(h["value"])
        if same_name and same_name.get("value") != h["value"]:
            print(f"[!] CONFLICT: name '{h['name']}' already used for {same_name.get('value')} "
                  f"(CSV says {h['value']}) - skipped")
        elif same_name:
            pass                                    # exact match, already there
        elif same_ip:
            print(f"[~] {h['value']} already exists as '{same_ip['name']}' - skipped (will reuse in group)")
        else:
            to_create.append(h)

    print(f"[*] {len(to_create)} to create, {len(hosts) - len(to_create)} skipped (already present or conflict)")

    if to_create:
        if input("Proceed with import? (y/n): ").strip().lower() != "y":
            print("Cancelled.")
            return

        created = 0
        for i in range(0, len(to_create), CHUNK):
            chunk = to_create[i:i + CHUNK]
            res = requests.post(f"{base}/object/hosts?bulk=true", headers=headers,
                                json=chunk, verify=False, timeout=60)
            if res.status_code in (200, 201):
                created += len(chunk)
                print(f"[+] Created {len(chunk)} hosts (batch {i // CHUNK + 1})")
            else:
                print(f"[-] Batch {i // CHUNK + 1} failed ({res.status_code}): {res.text[:500]}")
        print(f"[*] Done. {created}/{len(to_create)} hosts created.")

    group = input("Group name to put all of these hosts in (blank to skip): ").strip()
    if group:
        create_group(base, headers, group, hosts)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)