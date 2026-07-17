# Automated project deployment script for Windows
$ErrorActionPreference = "Stop"

echo "=== Starting project deployment ==="

$ProjectRoot = (Get-Item $PSScriptRoot).Parent.FullName

# Check if Python 3.12+ is installed in the system
$pythonValid = $false
if (Get-Command python -ErrorAction SilentlyContinue) {
    $version = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
    if ([version]$version -ge [version]"3.12") {
        $pythonValid = $true
        echo "Found compatible system Python version: $version`n"
    }
}   

# If Python is missing or outdated — download and install Python 3.12.10 in silent mode
if (-not $pythonValid) {
    echo "Python 3.12+ not found.`nDownloading Python 3.12.10 in silent mode..."
    $url = "https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe"
    $installerPath = "$PSScriptRoot\python-3.12.10-installer.exe"
    Invoke-WebRequest -Uri $url -OutFile $installerPath
    
    echo "Installing Python, please wait..."
    Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=0 SimpleInstall=1" -Wait
    
    $userPath = [System.Environment]::GetEnvironmentVariable("USERPROFILE")
    $newPythonPath = "$userPath\AppData\Local\Programs\Python\Python312\python.exe"

    echo "Python 3.12.10 binary path: $newPythonPath"

    # Fix for the "Access Denied" error: release file and force delete
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
    Start-Sleep -Seconds 2
    if (Test-Path $installerPath) {
        Unblock-File -Path $installerPath -ErrorAction SilentlyContinue
        Set-ItemProperty -Path $installerPath -Name IsReadOnly -Value $false -ErrorAction SilentlyContinue
        Remove-Item -Path $installerPath -Force
    }
    
    # Update PATH environment variable for the current session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    echo "Python 3.12.10 successfully installed`n"
}

# Create an isolated virtual environment (.venv)
echo "Checking for .venv virtual environment..."
if (Test-Path "$ProjectRoot\.venv") { 
    echo "Virtual environment detected.`n" 
}
else {
    echo "Virtual environment not found.`nCreating .venv..."
    & $newPythonPath -m venv "$ProjectRoot\.venv"
    echo "Environment created successfully`n"
}

# Upgrade pip and install libraries INSIDE .venv
echo "Upgrading pip and installing dependencies..."
& $ProjectRoot\.venv\Scripts\python.exe -m pip install --upgrade pip

try {
    echo "Attempting to install the project package..."
    & $ProjectRoot\.venv\Scripts\python.exe -m pip install .
    echo "Project package installed successfully."
}
catch {
    echo "`n[ERROR] Project deployment failed during package installation."
    echo "Please check your pyproject.toml configuration and file layout.`n"
    
    throw "Deployment halted: pip install . failed to execute successfully."
}

echo "`n=== Deployment successfully completed! ==="

.\.venv\Scripts\Activate.ps1