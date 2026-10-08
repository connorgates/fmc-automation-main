# Set execution policy for this session and activate venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -ErrorAction SilentlyContinue
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
}

function Show-Menu {
    Clear-Host
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "        FMC AUTOMATION TOOLKIT            " -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host " [1] Test FMC Connection" -ForegroundColor Green
    Write-Host " [2] Search/Dump Access Control Rules" -ForegroundColor White
    Write-Host " [3] Audit IPs in Rules (Edit in Script)" -ForegroundColor White
    Write-Host " [4] Export FMC Devices" -ForegroundColor White
    Write-Host " [5] Find Unused Objects" -ForegroundColor White
    Write-Host " [6] Get Full Objects" -ForegroundColor White
    Write-Host " [7] Create Rule from CSV" -ForegroundColor Yellow
    Write-Host " [8] Block/Unblock/View Malicious IP (Dynamic Object)" -ForegroundColor Yellow
    Write-Host " [9] Import Hosts from CSV" -ForegroundColor Yellow
    Write-Host " [Q] Quit" -ForegroundColor Red
    Write-Host "==========================================" -ForegroundColor Cyan
}

do {
    Show-Menu
    $choice = Read-Host "Select an option"
    
    switch ($choice) {
        '1' { python test_conn.py; Pause }
        '2' { python search_rules.py; Pause }
        '3' { python check_ip_rules.py; Pause }
        '4' { python export_devices.py; Pause }
        '5' { python find_unused_objects.py; Pause }
        '6' { python get_full_objects.py; Pause }
        '7' { python create_rule.py; Pause }
        '8' { python ops_dynamic_objects.py; Pause }
        '9' { python import_hosts.py; Pause }
        'Q' { Write-Host "Exiting..." -ForegroundColor Green }
        'q' { Write-Host "Exiting..." -ForegroundColor Green }
        Default { Write-Host "Invalid selection." -ForegroundColor Red; Start-Sleep -Seconds 1 }
    }
} until ($choice -eq 'Q' -or $choice -eq 'q')