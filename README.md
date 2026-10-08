# Cisco FMC REST API Automation Toolkit

A Python-based network automation suite for Cisco Secure Firewall Management Center (FMC). This project streamlines network operations, compliance auditing, inventory tracking, and rule provisioning via the FMC REST API.

---

## Capabilities

- **Device Health & Inventory Exporter (`export_devices.py`):** Extracts FTD firewall models, management IPs, software versions, and health statuses into CSV reports.
- **Unused Object Audit (`find_unused_objects.py`):** Queries FMC native database filters to identify unreferenced network objects across all policy sets.
- **Network Object Exporter (`get_objects.py`):** Dumps network objects, subnets, ranges, and groups into structured CSV inventories.
- **Batch Rule Deployment (`create_rules.py`):** Resolves target FTD device names, policy mappings, and security zone UUIDs to automate rule creation from CSV templates.

---

## Setup Instructions

1. **Clone Repository & Set Up Venv:**
   ```powershell
   git clone [https://github.com/YOUR_GITHUB_USERNAME/fmc-automation.git](https://github.com/YOUR_GITHUB_USERNAME/fmc-automation.git)
   cd fmc-automation
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install requests python-dotenv
