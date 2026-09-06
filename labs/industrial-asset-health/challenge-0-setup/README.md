# Challenge 0: Set up Microsoft Foundry

Time: ~20 minutes

## Objectives
- ✅ Provision the shared Foundry infrastructure, verify model access, and place `.env` in the lab folder

## Context
This lab reuses the repository-root Bicep and `azd` workflow. It does not change shared infrastructure. Each participant needs a unique environment name because Azure resource names must not collide.

## Get started

1. Confirm the prerequisites: an Azure subscription where you have **Contributor** and **Azure AI User/Foundry User**, Python 3.10+, Azure CLI, Azure Developer CLI, Git, and a terminal.
2. Clone and enter the repository:

   ```powershell
   git clone https://github.com/microsoft-hacks/Frontier-Hack.git
   Set-Location Frontier-Hack
   ```

3. Create a virtual environment and install this lab's dependencies.

   Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r labs/industrial-asset-health/requirements.txt
   pip install -r labs/industrial-asset-health/api-industrial/requirements.txt
   ```

   Linux/macOS bash:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r labs/industrial-asset-health/requirements.txt
   pip install -r labs/industrial-asset-health/api-industrial/requirements.txt
   ```

4. Sign in, select the intended subscription, and provision. Enter a unique environment such as `industrial-youralias-01` and use `swedencentral` when prompted for a region.

   ```powershell
   az login --tenant <your-tenant-id>
   az account list --output table
   az account set --subscription <subscription-id>
   az account show --output table
   azd auth login
   azd env new industrial-youralias-01
   azd env set AZURE_LOCATION swedencentral
   azd up
   ```

5. Root provisioning writes `.env`. Copy it to this lab folder.

   PowerShell:

   ```powershell
   Copy-Item .env labs/industrial-asset-health/.env
   ```

   Bash:

   ```bash
   cp .env labs/industrial-asset-health/.env
   ```

6. In the [Azure portal](https://portal.azure.com), open the resource group printed by `azd up`. Confirm it contains a Foundry resource/project, model deployment, Application Insights, and Log Analytics workspace.
7. In the [Microsoft Foundry portal](https://ai.azure.com/nextgen), open the project. Under **Build** → **Models** (or **Deployments**), confirm the model status is **Succeeded**. Open its playground, send `Reply with: setup verified`, and confirm it responds.

## Success criteria
- [ ] The Foundry project is visible and the model deployment shows **Succeeded**
- [ ] The model playground answers a test message
- [ ] `labs/industrial-asset-health/.env` exists

Next: [Challenge 1 - Build agents](../challenge-1-build/README.md)