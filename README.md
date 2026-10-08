Cisco FMC REST API Automation Toolkit

A Python-based network automation suite for Cisco Secure Firewall Management Center (FMC). This project streamlines network operations, compliance auditing, inventory tracking, network-object management, and rule provisioning through the FMC REST API.

The toolkit is designed to make common FMC administrative tasks repeatable and easier to perform without manually navigating through the FMC web interface.

Capabilities

The toolkit currently provides automation for:

Device Health & Inventory Exporter (export_devices.py)

Extracts FTD firewall information from FMC.

Exports device names, models, management IP addresses, software versions, and health information to CSV.

Unused Object Audit (find_unused_objects.py)

Searches FMC for network objects that are not currently referenced.

Helps identify objects that may be candidates for cleanup or review.

Network Object Exporter (get_objects.py)

Exports FMC network objects into structured CSV data.

Supports hosts, subnets, ranges, and network object groups.

Network Object & Group Management

Creates network objects and object groups in FMC.

Useful for adding hosts, networks, IP ranges, and groups without manually creating each object through the FMC GUI.

Batch Rule Deployment (create_rules.py)

Reads rule information from CSV templates.

Resolves FTD devices, access-control policies, and security zones.

Creates FMC access-control rules through the REST API.

Interactive FMC Toolkit

Provides a menu-driven interface for common FMC automation tasks.

Additional functions can be added to the toolkit as the project grows.

fmc Command Launcher

A Windows launcher is included so the toolkit can be started from Command Prompt by simply typing:

fmc

The launcher starts the toolkit without requiring the user to manually navigate to the project directory every time.

Requirements

The toolkit is intended to run on a Windows workstation used to administer Cisco FMC.

You will need:

Windows 10 or Windows 11

Internet/network access to the FMC management interface

A GitHub account with access to this repository

Git for Windows

Python 3.x

An FMC account with the required API permissions

PowerShell

Command Prompt

Important: The computer running the toolkit must be able to communicate with the FMC over HTTPS.

Initial Installation

The following instructions are for installing the toolkit on a new Windows computer.

1. Install Git

If Git is not already installed:

Download and install Git for Windows.

Use the default installation options unless your organization's IT policies require something different.

After installation, open Command Prompt or PowerShell.

Verify Git is installed:

git --version

You should see something similar to:

git version 2.x.x

2. Install Python

If Python is not already installed:

Install Python 3.x for Windows.

During installation, make sure to select:

Add Python to PATH

Complete the installation.

Verify Python:

python --version

You should see something similar to:

Python 3.x.x

If python is not recognized, close and reopen Command Prompt/PowerShell after installing Python.

3. Clone the GitHub Repository

Choose where you want to keep the toolkit.

For example, to keep it in your user profile:

cd $HOME

Then clone the repository:

git clone https://github.com/YOUR_GITHUB_USERNAME/fmc-automation.git

Replace:

YOUR_GITHUB_USERNAME

with the actual GitHub username/organization that owns the repository.

For example:

git clone https://github.com/myusername/fmc-automation.git

Git will download the project to a folder named:

fmc-automation

4. Enter the Toolkit Directory

After cloning the repository, change into the project directory:

cd fmc-automation

You can verify that you are in the correct location with:

dir

You should see the project files, such as the Python scripts, PowerShell files, batch launcher, and README.

What does cd mean?

cd means Change Directory.

For example:

cd fmc-automation

means:

"Move into the fmc-automation folder."

This is important because the commands that follow need to be run from the toolkit's directory.

5. Create a Python Virtual Environment

A virtual environment keeps the toolkit's Python packages separate from other Python programs installed on the computer.

From inside the fmc-automation directory, run:

python -m venv venv

This creates a folder called:

venv

inside the project.

6. Activate the Virtual Environment

In PowerShell:

.\venv\Scripts\Activate.ps1

After activation, the command prompt should show something similar to:

(venv) PS C:\Users\Username\fmc-automation>

The (venv) indicates that the toolkit's Python environment is active.

If PowerShell prevents the activation script from running, you may need to allow locally created PowerShell scripts:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then run:

.\venv\Scripts\Activate.ps1

If your organization's security policies restrict PowerShell execution policies, contact your IT administrator rather than changing the policy.

7. Install Python Dependencies

With the virtual environment activated, install the required packages:

pip install requests python-dotenv

If the repository contains a requirements.txt file, use that instead:

pip install -r requirements.txt

Using requirements.txt is preferred because it installs the dependencies defined by the project.

You can verify the installed packages with:

pip list

8. Configure FMC Credentials

The toolkit requires FMC connection information to communicate with the FMC REST API.

The project uses environment variables / a .env configuration rather than placing credentials directly inside the Python scripts.

A typical configuration looks similar to:

FMC_HOST=your-fmc-hostname
FMC_USERNAME=your-username
FMC_PASSWORD=your-password

The exact variable names should match the .env template included with the repository.

If the repository contains:

.env.example

copy it to:

.env

For example:

copy .env.example .env

Then edit .env and enter the appropriate FMC information.

Important

Never commit .env to GitHub.

The .env file contains credentials and should remain local to the computer running the toolkit.

The repository should contain .gitignore rules that prevent .env from being committed.

9. Test the Toolkit

Before setting up the fmc command, test the toolkit directly.

From the project directory:

python <main-toolkit-script>.py

Replace <main-toolkit-script>.py with the actual main Python script included in the repository.

The toolkit should start and display its interactive menu.

For example:

========================================
        FMC AUTOMATION TOOLKIT
========================================

[1] Test FMC Connection
[2] Search/Dump Access Control Rules
[3] Audit IPs in Rules
...
[Q] Quit

Select an option:

Run the FMC connection test first.

If the connection test succeeds, the computer is able to communicate with FMC using the configured credentials.

10. Install the fmc Command

The repository includes a Windows .bat launcher and a PowerShell (.ps1) launcher.

These files are used to make starting the toolkit easier.

Instead of doing this every time:

cd C:\Users\Username\fmc-automation
.\venv\Scripts\Activate.ps1
python <main-toolkit-script>.py

the goal is to simply type:

fmc

from Command Prompt.

Installing the launcher

Use the provided PowerShell setup/launcher script included in the repository.

From the project directory, run the .ps1 setup script according to its filename.

For example:

.\<launcher-script>.ps1

The launcher should configure the Windows environment so the included .bat file can be found when fmc is entered from Command Prompt.

Note: The exact .ps1 filename may change as the project is updated. Use the .ps1 file included in the current repository.

11. Start the Toolkit

After the launcher has been installed, open a new Command Prompt window.

Type:

fmc

Press Enter.

The toolkit should launch.

You should no longer need to manually cd into the project directory each time.

Everyday Usage

Once the initial installation is complete, starting the toolkit should be as simple as:

Open Command Prompt.

Type:

fmc

Press Enter.

Select the desired toolkit function.

Example:

C:\Users\Username>fmc

========================================
        FMC AUTOMATION TOOLKIT
========================================

Select an option:

Updating the Toolkit

The toolkit is maintained in GitHub.

When new features or fixes are added, update the local copy with Git.

Open Command Prompt or PowerShell and navigate to the project directory:

cd $HOME\fmc-automation

Then run:

git pull

Git will download the latest version of the toolkit.

If new Python dependencies were added, update them with:

.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Then the fmc command can be used normally.

Example Update Workflow

A normal update may look like:

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

Git is either not installed or its installation directory is not in PATH.

Install Git for Windows and reopen Command Prompt.

python is not recognized

If you see:

'python' is not recognized as an internal or external command

Install Python and make sure:

Add Python to PATH

was selected during installation.

Close and reopen Command Prompt afterward.

PowerShell will not run the .ps1 file

If PowerShell reports that script execution is disabled, check the current execution policy:

Get-ExecutionPolicy -List

For a normal personal/user installation, the project may be able to use:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

If your organization's policies prevent this, contact IT.

fmc is not recognized

If:

fmc

returns:

'fmc' is not recognized as an internal or external command

first try closing and reopening Command Prompt.

If it still does not work:

Verify the .bat launcher exists.

Verify the launcher installation/setup script was run.

Check that the directory containing the .bat file is in the user's Windows PATH.

Confirm the launcher points to the correct toolkit directory and Python environment.

You can inspect PATH with:

echo %PATH%

FMC connection fails

Check:

FMC hostname/IP address.

FMC is reachable from the computer.

HTTPS access to FMC is available.

Username and password are correct.

The FMC account has the required API permissions.

.env contains the correct values.

No firewall or network ACL is blocking access.

You can test basic connectivity with:

ping <FMC_HOST>

and, where appropriate:

Test-NetConnection <FMC_HOST> -Port 443

Security Considerations

This toolkit can make changes to a production firewall management system.

Use appropriate change-control procedures before making production changes.

In particular:

Protect FMC credentials.

Do not commit .env files to GitHub.

Do not store passwords directly in Python source code.

Use an FMC account with only the permissions required by the toolkit.

Review CSV files before importing them.

Review newly created objects, groups, and rules.

Verify the target FMC before making changes.

Keep appropriate backups and change records.

Test significant changes before applying them to production.

Repository Structure

The project may contain files similar to:

fmc-automation/
│
├── create_rules.py
├── export_devices.py
├── find_unused_objects.py
├── get_objects.py
│
├── <object-management-script>.py
├── <main-toolkit-script>.py
│
├── <launcher>.ps1
├── <launcher>.bat
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

The exact filenames may change as the toolkit is developed.

Recommended First-Time Installation Checklist

For someone installing the toolkit for the first time:

[ ] Install Git
[ ] Install Python 3.x
[ ] Clone the GitHub repository
[ ] cd into the fmc-automation directory
[ ] Create the Python virtual environment
[ ] Activate the virtual environment
[ ] Install Python dependencies
[ ] Create/configure the .env file
[ ] Test the FMC connection
[ ] Run the launcher setup script
[ ] Open a NEW Command Prompt
[ ] Type: fmc
[ ] Confirm the toolkit launches

After that, normal use should only require:

Open CMD
   |
   v
Type: fmc
   |
   v
Use the toolkit

Quick Start

For an experienced user, the initial setup is approximately:

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

License

Add the appropriate license and/or internal-use statement for your organization here.

Maintainer

Cisco FMC REST API Automation Toolkit

For issues or enhancements, document the requested change and include:

The toolkit function being used

Error message/output

FMC version

Python version

Windows version

Relevant configuration details (excluding passwords or other secrets)