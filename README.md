Cisco FMC REST API Automation Toolkit

A Python-based network automation suite for Cisco Secure Firewall Management Center (FMC).

This toolkit is designed to make common FMC administration tasks faster, easier, and more repeatable by using the FMC REST API instead of manually performing every task through the FMC web interface.

It can be used for:

 Device inventory and health reporting

 Unused object auditing

 Network object and object-group management

 Access-control rule creation

 CSV-based bulk operations

 General FMC administration and automation

 What Does This Toolkit Do?

The toolkit provides several automation functions for managing FMC.

 Device Health & Inventory

export_devices.py

Exports information about managed FTD devices from FMC.

Information can include:

Device name

FTD model

Management IP address

Software version

Health/status information

The information is exported into CSV reports, making it easy to review or use in other administrative workflows.

 Unused Object Audit

find_unused_objects.py

Searches FMC for network objects that are not currently being referenced.

This can help identify:

Old objects

Objects created for previous projects

Unused hosts

Unused networks

Objects that may be candidates for cleanup

 Important: An object being identified as unused does not automatically mean it should be deleted. Always review the results before removing configuration from FMC.

 Network Object Exporter

get_objects.py

Exports FMC network objects into structured CSV files.

Supported object types can include:

Host objects

Subnets

IP ranges

Network objects

Network object groups

This is useful for inventory, auditing, documentation, and troubleshooting.

 Network Object & Group Management

The toolkit can also create network objects and network object groups directly in FMC.

This allows administrators to add objects without manually navigating through the FMC GUI for every entry.

For example:

Server Name       IP Address
-----------       ----------
WEB01             10.20.10.15
WEB02             10.20.10.16
DB01              10.20.20.10

These can then be created in FMC through the automation workflow.

Object groups can also be created to organize multiple objects together.

 Batch Rule Deployment

create_rules.py

Creates FMC Access Control Rules using information provided through CSV templates.

The script can resolve:

FTD device names

Access-control policies

Security zones

Other required FMC identifiers

This makes it possible to prepare firewall rules in a spreadsheet and then automatically deploy them to FMC.

 Requirements

Before installing the toolkit, the computer should have:

Requirement

Purpose

Windows 10/11

Operating system

Git

Downloads and updates the toolkit

Python 3.x

Runs the automation scripts

PowerShell

Runs the launcher/setup scripts

Command Prompt

Used to launch the fmc command

Network access to FMC

Allows the toolkit to communicate with FMC

FMC account

Provides API access

 You do not need to understand Python to use the finished toolkit. Once the initial setup is complete, the normal workflow is simply opening Command Prompt and typing fmc.

 Initial Installation

The following instructions assume this is the first time the toolkit is being installed on the computer.

1️ Install Git

Git is used to download the toolkit from GitHub and later retrieve updates.

If Git is not already installed:

Install Git for Windows.

Use the default installation options.

Open Command Prompt after installation.

Verify Git is working:

git --version

You should see something similar to:

git version 2.x.x

 If a Git version is displayed, Git is installed correctly.

2️ Install Python

The toolkit uses Python to communicate with the FMC REST API.

Install Python 3.x for Windows.

During installation, make sure the following option is enabled:

 Add Python to PATH

After installation, open a new Command Prompt window.

Verify Python:

python --version

You should see something similar to:

Python 3.x.x

 If Windows says that python is not recognized, close Command Prompt and open it again.

3️ Download the Toolkit from GitHub

This is where Git comes in.

Open Command Prompt or PowerShell.

First, choose where you want to store the toolkit.

For example:

cd $HOME

Then download the repository:

git clone https://github.com/YOUR_GITHUB_USERNAME/fmc-automation.git

Replace:

YOUR_GITHUB_USERNAME

with the GitHub account or organization that owns the repository.

For example:

git clone https://github.com/mycompany/fmc-automation.git

Git will download the project into a folder named:

fmc-automation

4️ Enter the Toolkit Folder

Now move into the folder you just downloaded:

cd fmc-automation

What does cd mean?

cd = Change Directory

Think of it like opening a folder in File Explorer.

For example:

cd fmc-automation

means:

"Go into the fmc-automation folder."

You can confirm you are in the correct folder with:

dir

You should see the toolkit files.

5️ Create the Python Virtual Environment

The toolkit uses a virtual environment so its Python packages do not interfere with other Python applications on the computer.

From inside the fmc-automation directory:

python -m venv venv

This creates:

fmc-automation
│
├── venv
├── create_rules.py
├── export_devices.py
├── ...
└── README.md

 You normally only need to create the virtual environment once.

6️ Activate the Virtual Environment

In PowerShell, run:

.\venv\Scripts\Activate.ps1

You should now see:

(venv)

at the beginning of your command prompt.

For example:

(venv) PS C:\Users\Username\fmc-automation>

The (venv) tells you that the toolkit's Python environment is active.

 PowerShell Execution Policy

If PowerShell refuses to run the activation script, you may see an error saying that script execution is disabled.

For a normal user installation, you may be able to run:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then try again:

.\venv\Scripts\Activate.ps1

 If this is a managed company computer and PowerShell execution policies are controlled by IT, do not bypass the organization's policy. Contact your IT administrator if necessary.

7️ Install the Required Python Packages

With the virtual environment activated, install the packages required by the toolkit.

If the repository contains a requirements.txt file, run:

pip install -r requirements.txt

This is the preferred method because it installs the dependencies defined by the project.

If there is no requirements.txt, install the required packages directly:

pip install requests python-dotenv

Verify the installed packages:

pip list

 8️ Configure FMC Credentials

The toolkit needs information about the FMC it will connect to.

The project uses a .env file so credentials do not need to be written directly into the Python scripts.

A configuration may look similar to:

FMC_HOST=your-fmc-hostname
FMC_USERNAME=your-username
FMC_PASSWORD=your-password

The exact variable names must match the .env.example file included with the repository.

If the repository contains:

.env.example

copy it:

copy .env.example .env

Then open .env and enter the appropriate FMC information.

 IMPORTANT — Protect Your Credentials

Never commit .env to GitHub.

The .env file contains sensitive information and should remain local to the computer running the toolkit.

The repository should include .env in .gitignore.

 9️ Test the Toolkit

Before setting up the fmc command, test that the toolkit itself works.

From the project directory, run the main toolkit Python script.

For example:

python <main-toolkit-script>.py

Replace <main-toolkit-script>.py with the actual launcher/main Python file in the repository.

The toolkit should display its menu.

For example:

===========================================
          FMC AUTOMATION TOOLKIT
===========================================

[1] Test FMC Connection
[2] Search/Dump Access Control Rules
[3] Audit IPs in Rules
[4] Export FMC Devices
[5] Find Unused Objects
[6] Get Full Objects
[7] Create Rule from CSV
[8] Block/Unblock/View Malicious IP
[9] Import Hosts from CSV

[Q] Quit

Select an option:

 First Test

Run the FMC connection test first.

If the connection test succeeds, the computer is able to communicate with FMC using the configured credentials.

 Set Up the fmc Command

The repository includes a PowerShell (.ps1) script and a Windows batch (.bat) launcher.

These are designed to make starting the toolkit much easier.

Without the launcher, you would normally need to do something like:

cd C:\Users\Username\fmc-automation
.\venv\Scripts\Activate.ps1
python <main-toolkit-script>.py

That's a lot to remember.

Instead, the launcher allows you to simply type:

fmc

from Command Prompt.

 Install the Launcher

Run the provided .ps1 setup script from the repository.

For example:

.\<launcher-script>.ps1

ℹ The exact .ps1 filename may change as the project is updated. Use the PowerShell launcher included in the repository.

The setup script configures Windows so the .bat launcher can be found when you type fmc.

 Start the Toolkit

After installing the launcher:

Close Command Prompt and open a NEW Command Prompt window.

Then simply type:

fmc

Press Enter.

 The FMC Automation Toolkit should start.

You should see the interactive menu.

 Everyday Usage

Once the toolkit has been installed, using it should be extremely simple.

Step 1

Open Command Prompt.

Step 2

Type:

fmc

Step 3

Press Enter.

Step 4

Choose the desired operation from the toolkit menu.

That's it.

 You should not need to manually cd into the project directory every time you want to use the toolkit.

 Updating the Toolkit

The toolkit is stored in GitHub, which means updates can be pulled down without reinstalling everything.

When a new feature or bug fix is pushed to GitHub:

1. Open PowerShell or Command Prompt.

2. Go to the project:

cd $HOME\fmc-automation

3. Download the latest version:

git pull

4. If dependencies changed:

.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

5. Start the toolkit:

fmc

 Typical Update Workflow

cd $HOME\fmc-automation
git pull
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Then:

fmc

 Troubleshooting

 git is not recognized

If you see:

'git' is not recognized as an internal or external command

Git is either not installed or its installation directory is not in Windows PATH.

Fix

Install Git for Windows, then close and reopen Command Prompt.

 python is not recognized

If you see:

'python' is not recognized as an internal or external command

Python is either not installed or was not added to PATH.

Fix

Reinstall Python and make sure:

Add Python to PATH

is selected.

Then close and reopen Command Prompt.

 PowerShell will not run the .ps1 file

Check the current execution policies:

Get-ExecutionPolicy -List

If appropriate for your environment:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then retry the launcher.

 On managed corporate computers, security policies may prevent this. Contact IT if necessary.

 fmc is not recognized

If:

fmc

returns:

'fmc' is not recognized as an internal or external command

try these steps:

1. Close Command Prompt

Open a new Command Prompt window.

2. Verify the launcher exists

Make sure the .bat launcher is present.

3. Run the PowerShell setup script again

Use the launcher setup script from the repository.

4. Check Windows PATH

Run:

echo %PATH%

The directory containing the fmc.bat launcher should be included.

 FMC Connection Fails

If the toolkit starts but cannot connect to FMC, check:

FMC hostname/IP address

Username

Password

FMC API permissions

Network connectivity

HTTPS/443 access

.env configuration

Firewall/ACL rules between the workstation and FMC

You can test HTTPS connectivity with:

Test-NetConnection <FMC_HOST> -Port 443

If the connection succeeds, you should see:

TcpTestSucceeded : True

🗂️ Repository Structure

The project may look similar to:

fmc-automation/
│
├── 📄 create_rules.py
├── 📄 export_devices.py
├── 📄 find_unused_objects.py
├── 📄 get_objects.py
│
├── 📄 <object-management-script>.py
├── 📄 <main-toolkit-script>.py
│
├── ⚙️ <launcher>.ps1
├── ⚙️ <launcher>.bat
│
├── 🔐 .env.example
├── 🚫 .gitignore
├── 📦 requirements.txt
└── 📖 README.md

The exact filenames may change as the project develops.

🔐 Security & Change Management

This toolkit can make real configuration changes to a production firewall management system.

Please use normal organizational change-control procedures.

Before making production changes:

✅ Verify the correct FMC

✅ Review the intended configuration change

✅ Verify object names and IP addresses

✅ Review CSV files before importing them

✅ Review newly created objects and groups

✅ Review newly created rules

✅ Use appropriate FMC permissions

✅ Protect API credentials

✅ Keep appropriate backups/change records

 A mistake made through automation can potentially affect many firewall configurations at once. Always verify the target environment before making changes.

 Credential Security

Never put passwords directly into Python source code.

Use the .env configuration instead.

Never commit:

.env

to GitHub.

The .gitignore file should prevent this from happening.

If credentials are accidentally committed to GitHub, rotate the affected credentials immediately.

 First-Time Installation Checklist

Use this checklist when installing the toolkit on a new computer:

☐ Install Git
☐ Install Python 3.x
☐ Clone the GitHub repository
☐ cd into the fmc-automation directory
☐ Create the Python virtual environment
☐ Activate the virtual environment
☐ Install Python dependencies
☐ Create/configure the .env file
☐ Test the FMC connection
☐ Run the launcher setup script
☐ Open a NEW Command Prompt
☐ Type: fmc
☐ Confirm the toolkit launches

 Quick Start

For someone who already has Git and Python installed, the setup is approximately:

git clone https://github.com/YOUR_GITHUB_USERNAME/fmc-automation.git
cd fmc-automation

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Configure .env

# Run the launcher setup script
.\<launcher-script>.ps1

Then open a new Command Prompt:

fmc

 After Installation

Once everything is configured, the normal workflow is simply:

┌─────────────────────────┐
│ Open Command Prompt     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Type: fmc               │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ FMC Automation Toolkit  │
│ launches                 │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Select an operation     │
└─────────────────────────┘

No need to manually navigate to the project folder every time.

 Summary

The Cisco FMC REST API Automation Toolkit provides a centralized way to automate common FMC administration tasks.

It combines:

Python + FMC REST API + CSV workflows + PowerShell + Windows launcher

to provide a simple administrator experience:

Open CMD → type fmc → choose what you want to do.

 License

Add the appropriate license and/or internal-use statement for your organization here.

 Maintainer

Cisco FMC REST API Automation Toolkit

For issues or enhancements, include:

Toolkit function being used

Error message/output

FMC version

Python version

Windows version

Relevant configuration details

 Never include passwords, API tokens, or other secrets when reporting an issu