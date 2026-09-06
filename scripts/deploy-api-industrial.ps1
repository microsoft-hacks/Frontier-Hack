<#
.SYNOPSIS
Deploys the fictional industrial asset FastAPI service to Azure App Service.

.DESCRIPTION
Creates or reuses a Linux App Service plan and web app, then performs a zip deployment.
This adds billable resources outside the shared Foundry infrastructure. Delete the resource
group after the workshop if it was created only for this API.
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string]$AppName,
    [string]$ResourceGroup = "$AppName-rg",
    [string]$Plan = "$AppName-plan",
    [string]$Location = "swedencentral",
    [string]$Sku = "B1",
    [string]$Subscription
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
$apiPath = Join-Path $repoRoot "labs\industrial-asset-health\api-industrial"
if (-not (Test-Path $apiPath)) { throw "API folder not found: $apiPath" }

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
Write-Warning "This creates billable App Service resources in '$ResourceGroup'."

& az group show -n $ResourceGroup --only-show-errors 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Invoke-Az -Arguments @("group", "create", "-n", $ResourceGroup, "-l", $Location) | Out-Null
}

& az appservice plan show -n $Plan -g $ResourceGroup --only-show-errors 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Invoke-Az -Arguments @("appservice", "plan", "create", "-n", $Plan, "-g", $ResourceGroup, "--is-linux", "--sku", $Sku, "-l", $Location) | Out-Null
}

& az webapp show -n $AppName -g $ResourceGroup --only-show-errors 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Invoke-Az -Arguments @("webapp", "create", "-n", $AppName, "-g", $ResourceGroup, "-p", $Plan, "--runtime", "PYTHON:3.12") | Out-Null
}

Invoke-Az -Arguments @("webapp", "config", "appsettings", "set", "-n", $AppName, "-g", $ResourceGroup, "--settings", "SCM_DO_BUILD_DURING_DEPLOYMENT=true") | Out-Null
Invoke-Az -Arguments @("webapp", "config", "appsettings", "delete", "-n", $AppName, "-g", $ResourceGroup, "--setting-names", "WEBSITE_RUN_FROM_PACKAGE") | Out-Null
Invoke-Az -Arguments @("webapp", "config", "set", "-n", $AppName, "-g", $ResourceGroup, "--startup-file", "python -m uvicorn main:app --host 0.0.0.0") | Out-Null

$zipPath = Join-Path $env:TEMP "api-industrial-deploy.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Push-Location $apiPath
try {
    $items = Get-ChildItem -Force | Where-Object { $_.Name -notin @(".venv", "__pycache__") }
    Compress-Archive -Path $items -DestinationPath $zipPath -Force
}
finally { Pop-Location }

try {
    Invoke-Az -Arguments @("webapp", "deploy", "-n", $AppName, "-g", $ResourceGroup, "--src-path", $zipPath, "--type", "zip", "--track-status", "true")
}
finally { Remove-Item $zipPath -Force -ErrorAction SilentlyContinue }

$hostName = Invoke-Az -Arguments @("webapp", "show", "-n", $AppName, "-g", $ResourceGroup, "--query", "defaultHostName", "-o", "tsv")
if ([string]::IsNullOrWhiteSpace($hostName)) { throw "Azure CLI did not return a web app host name." }
$conditionUrl = "https://$hostName/assets/DRIVE-103/condition"
try {
    $condition = Invoke-RestMethod -Uri $conditionUrl -TimeoutSec 60
}
catch {
    throw "Deployment completed, but API verification failed at '$conditionUrl'. Check App Service logs and retry. $($_.Exception.Message)"
}
if ($condition.asset_id -ne "DRIVE-103" -or $condition.reported_status -ne "critical") {
    throw "API verification returned an unexpected DRIVE-103 response."
}

Write-Host "API URL: https://$hostName" -ForegroundColor Green
Write-Host "OpenAPI: https://$hostName/openapi.json" -ForegroundColor Green
Write-Host "Verified: $conditionUrl" -ForegroundColor Green
Write-Host "Cleanup: az group delete --name $ResourceGroup --yes --no-wait" -ForegroundColor Yellow