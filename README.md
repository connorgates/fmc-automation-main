__FMC Automation Toolkit__

A PowerShell-based automation toolkit for managing and auditing Cisco Firepower Management Center (FMC) through the FMC API.

The toolkit provides an interactive menu that brings common FMC administration, security-rule management, object management, and IP-address workflows into a single command-line interface.

__Features__

The toolkit currently provides the following functions:

__1. Test FMC Connection__

Tests connectivity and authentication to the configured Cisco FMC instance.

Use this option to verify that:
The FMC is reachable.
API authentication is working.
The configured FMC credentials are valid.

The automation environment can communicate with FMC before performing changes.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__2. Search / Dump Access Control Rules__

Searches and exports information about Access Control Rules (ACRs) configured in FMC.

This can be used to:

Locate rules by name or other criteria.
Review rule configuration.
Dump rule information for troubleshooting or auditing.
Inspect existing rules before making changes.
This is useful when working with large rulebases where manually searching through the FMC GUI can be time-consuming.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__3. Audit IPs in Rules__

Audits IP addresses referenced by FMC access-control rules.

The toolkit can identify IPs used within rules and produce information that can be reviewed or edited through the automation workflow.

Typical uses include:

Finding where a specific IP is referenced.
Reviewing IP addresses currently used by rules.
Preparing rule changes.
Auditing firewall configuration for outdated or incorrect IP references.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__4. Export FMC Devices__

Exports device information from FMC.

This provides a convenient way to inventory managed devices and maintain an external record of the FMC environment.

Depending on the configured implementation, exported information may include device-related details such as:

Device name
IP address
Device type
Management information
Other FMC device attributes

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__5. Find Unused Objects__

Searches FMC for objects that are no longer referenced by the configuration.

This can help identify configuration that may be safe to clean up, such as:

Unused network objects
Unused host objects
Unused object groups
Other objects that are not referenced by rules or related configuration
Important: An object being reported as unused does not automatically mean it should be deleted. Review the results before removing anything from FMC.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__6. Get Full Objects__

Retrieves detailed FMC object information.

This is intended for situations where the abbreviated information shown in normal searches is not enough.

It can be useful for:

Troubleshooting object configuration.
Inspecting FMC API responses.
Reviewing object attributes.
Developing or validating additional automation.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__7. Create Rule from CSV__

Creates an FMC Access Control Rule using information supplied in a CSV file.

This allows multiple rule parameters to be prepared in a spreadsheet or CSV and then imported through the toolkit rather than manually entering each value in the FMC GUI.

A CSV-driven workflow can be useful for:

Standardizing rule creation.
Creating multiple rules consistently.
Reducing manual configuration.
Preparing changes in advance for review.
Automating repetitive firewall administration.
The exact CSV columns and accepted values depend on the implementation of the script.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__8. Block / Unblock / View Malicious IP__

Manages malicious IP addresses using an FMC Dynamic Object workflow.

The option supports:

Block — Add an IP address to the designated malicious-IP dynamic object.

Unblock — Remove an IP address from the dynamic object.

View — Display the IP addresses currently contained in the object.

This provides a faster way to manage emergency IP blocks without manually navigating through FMC object configuration.

A typical workflow is:

Threat IP identified
        |
        v
Block IP through toolkit
        |
        v
IP added to FMC Dynamic Object
        |
        v
Firewall policy references the object
        |
        v
Traffic from the malicious IP can be blocked

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__9. Import Hosts from CSV__

Imports host/IP information from a CSV file into FMC.

This is intended to simplify the creation or management of host objects when dealing with a larger number of systems.

Example use cases include:

Importing server inventories.
Creating host objects from an existing spreadsheet.
Standardizing object names and IP addresses.
Reducing repetitive object creation through the FMC GUI.
A typical CSV may contain information such as:

Name,IP
WEB01,192.168.1.10
WEB02,192.168.1.11
DB01,192.168.1.20

The exact required column names and supported fields depend on the current script implementation.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__Interactive Menu__

When the toolkit is launched, it presents an interactive PowerShell menu:
Enter the number corresponding to the desired operation and follow the prompts provided by the script.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__Requirements__

The toolkit is intended for environments using Cisco Firepower Management Center (FMC) and its API.

Recommended requirements:

Windows PowerShell
Network connectivity to the FMC management interface
Valid FMC API credentials
Appropriate FMC permissions for the requested operation
Access to any required CSV input files
FMC API compatibility with the version being used
For environments running FMC 7.4.x, verify that the API endpoints and object types used by the toolkit match the installed FMC release.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__Authentication and Configuration__

Before using the toolkit, configure the FMC connection information required by the script.

Depending on the implementation, this may include:

FMC Hostname / IP
Username
Password / API credentials

Credentials should not be hard-coded into scripts or committed to source control.

Recommended practices include:

Use secure credential handling.
Avoid storing passwords in plain text.
Do not commit credentials to Git.
Use a dedicated FMC account with only the permissions required by the automation.
Protect any configuration files containing authentication information.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__CSV Workflows__
Several toolkit functions use CSV files to simplify bulk operations.

CSV files should be reviewed before importing them into FMC.

For example:

Name,IP
Example1,10.10.10.x
Example2,10.10.10.x
BExample3,10.10.10.x

Before running an import:

Verify hostnames and IP addresses.

Check for duplicate entries.
Confirm the CSV column names match what the script expects.
Review the resulting FMC objects.
Test the resulting firewall configuration where appropriate.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__Safety Considerations__

Some functions can make configuration changes to FMC.

In particular:

Creating access-control rules can affect traffic.
Importing objects changes the FMC configuration.
Blocking malicious IPs can immediately affect connectivity.
Removing or modifying objects can have downstream effects on rules.
Before making production changes:
Review the intended change.

Confirm the target FMC.

Verify object names and IP addresses.
Confirm the correct policy/rule context.
Test changes in a controlled environment when possible.
Maintain appropriate configuration backups or change records.
The toolkit should be treated as an administrative automation tool, not as a replacement for change-control procedures.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__Suggested Workflow__

A typical workflow for administering FMC with the toolkit is:

                    +----------------------+
                    | Start Toolkit        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Test FMC Connection  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Select Operation     |
                    +----------+-----------+
                               |
          +--------------------+--------------------+
          |                    |                    |
          v                    v                    v
    Rule Management       Object Management    Threat Management
          |                    |                    |
          v                    v                    v
    Search / Audit       Import / Inspect      Block / Unblock
          |                    |                    |
          +--------------------+--------------------+
                               |
                               v
                    +----------------------+
                    | Review FMC Changes   |
                    +----------------------+
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
__Disclaimer:__

This toolkit is an administrative automation utility for Cisco FMC environments. Changes made through the toolkit can affect firewall behavior and network connectivity.
Always verify the target FMC and review configuration changes before applying them to production.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__License__

Add the appropriate license and/or internal-use statement for your organization here.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

__Maintainer__

FMC Automation Toolkit

For issues or enhancements, document the requested change and include relevant error output, FMC version information, and the toolkit operation that produced the issue.

