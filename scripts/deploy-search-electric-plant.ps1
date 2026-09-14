<#
.SYNOPSIS
Deploys the shared Azure AI Search service for the Electric Plant lab and uploads the knowledge base.

.DESCRIPTION
Creates or reuses an Azure AI Search service (default "search-hack-shared") and populates the
"electric-plant-maintenance" index with the chunks from labs\electric-plant\search-knowledge by
running setup_index.py. Idempotent: re-running recreates the index with the current documents.

The Azure AI Search service is a separate shared resource (the Foundry infra in infra\main.bicep
does not provision search). After this script completes, the facilitator must attach the service
to the shared AI Foundry project as a connection named exactly "search-hack-shared" so each lab
can reference it from agents.py.

.EXAMPLE
.\scripts\deploy-search-electric-plant.ps1

.EXAMPLE
.\scripts\deploy-search-electric-plant.ps1 -ServiceName my-search -ResourceGroup rg-search -Sku standard -Location westeurope

.EXAMPLE
.\scripts\deploy-search-electric-plant.ps1 -SkipUpload -Subscription 00000000-0000-0000-0000-000000000000
#>

[CmdletBinding()]
param(
    [string]$ServiceName = "search-hack-shared",
    [string]$ResourceGroup = "rg-search-shared",
    [string]$Location = "swedencentral",
    [string]$Sku = "basic",
    [string]$Subscription,
    [string]$Python = "python",
    [switch]$SkipUpload
)

$ErrorActionPreference = "Stop"

function Invoke-Az {
    param([Parameter(Mandatory)] [string[]]$Arguments)

    $output = & az @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Azure CLI command failed: az $($Arguments -join ' ')"
    }
    return $output
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$setupScript = Join-Path $repoRoot "labs\electric-plant\search-knowledge\setup_index.py"
if (-not (Test-Path $setupScript)) { throw "setup_index.py not found: $setupScript" }

$accountJson = & az account show --only-show-errors 2>$null
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($accountJson)) {
    throw "Run 'az login' before this script."
}
if ($Subscription) {
    Invoke-Az -Arguments @("account", "set", "--subscription", $Subscription) | Out-Null
}
$account = (Invoke-Az -Arguments @("account", "show", "--only-show-errors")) | ConvertFrom-Json
if ($Subscription -and $account.id -ne $Subscription -and $account.name -ne $Subscription) {
    throw "Azure CLI selected '$($account.name)' ($($account.id)), not requested subscription '$Subscription'."
}
Write-Host "Subscription: $($account.name) ($($account.id))" -ForegroundColor Cyan
Write-Warning "This creates billable Azure AI Search resources in '$ResourceGroup' with SKU '$Sku'."

& az search service show -n $ServiceName -g $ResourceGroup --only-show-errors 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    & az group show -n $ResourceGroup --only-show-errors 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Invoke-Az -Arguments @("group", "create", "-n", $ResourceGroup, "-l", $Location) | Out-Null
        Write-Host "Created resource group: $ResourceGroup" -ForegroundColor Green
    }
    Invoke-Az -Arguments @(
        "search", "service", "create",
        "-n", $ServiceName,
        "-g", $ResourceGroup,
        "-l", $Location,
        "--sku", $Sku
    ) | Out-Null
    Write-Host "Created Azure AI Search service: $ServiceName" -ForegroundColor Green
}
else {
    Write-Host "Azure AI Search service already exists: $ServiceName" -ForegroundColor Green
}

$endpoint = "https://$ServiceName.search.windows.net"
Write-Host "Endpoint: $endpoint" -ForegroundColor Cyan

if ($SkipUpload) {
    Write-Host "Skipped index upload (-SkipUpload)." -ForegroundColor Yellow
}
else {
    Write-Host "Retrieving the search admin key for the upload..." -ForegroundColor Cyan
    $adminKey = (Invoke-Az -Arguments @(
            "search", "admin-key", "show",
            "--service-name", $ServiceName,
            "-g", $ResourceGroup,
            "--query", "primaryKey",
            "-o", "tsv"
        )).Trim()
    if ([string]::IsNullOrWhiteSpace($adminKey)) {
        throw "Azure CLI did not return the search admin key. If the service uses role-based access only, pass the key via AZURE_SEARCH_ADMIN_KEY or set -SkipUpload."
    }

    & $Python --version
    if ($LASTEXITCODE -ne 0) {
        throw "Python executable not found ('$Python'). Pass -Python <path> or run setup_index.py manually."
    }
    & $Python -c "import azure.search.documents" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "The azure-search-documents package is missing. Run 'pip install -r labs/electric-plant/requirements.txt' first, or pass -Python to a virtual environment that has it."
    }

    $env:AZURE_SEARCH_ENDPOINT = $endpoint
    $env:AZURE_SEARCH_ADMIN_KEY = $adminKey
    try {
        & $Python $setupScript
        if ($LASTEXITCODE -ne 0) {
            throw "setup_index.py failed with exit code $LASTEXITCODE."
        }
    }
    finally {
        Remove-Item Env:AZURE_SEARCH_ADMIN_KEY -ErrorAction SilentlyContinue
        Remove-Item Env:AZURE_SEARCH_ENDPOINT -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "Next steps (portal):" -ForegroundColor Cyan
Write-Host "  1. Open the AI Foundry project for the lab and go to Management center -> Connected resources -> + New connection -> Azure AI Search."
Write-Host "  2. Select '$ServiceName', name the connection exactly 'search-hack-shared' and mark it as shared."
Write-Host "  3. In the advisor agent, add the Azure AI Search tool and pick the 'electric-plant-maintenance' index."
Write-Host "Cleanup:  az group delete --name $ResourceGroup --yes --no-wait" -ForegroundColor Yellow