# Challenge 0: Set up Microsoft Foundry

Time: ~20 minutes

## Objectives
- ✅ Provision the shared Foundry project and verify portal access

## Context
The lab reuses the repository-root infrastructure and `.env` convention without changing `infra/main.bicep`. Agent work after setup is entirely in the portal. Each participant must use a unique environment name.

## Get started

1. Confirm access to an Azure subscription with **Contributor** and **Azure AI User/Foundry User**, plus Git, Python 3.10+, Azure CLI, Azure Developer CLI, and a terminal. Python is part of the common workshop setup but is not used to build this portal track.
2. Clone the repository and prepare an environment.

   Windows PowerShell:

   ```powershell
   git clone https://github.com/microsoft-hacks/Frontier-Hack.git
   Set-Location Frontier-Hack
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Linux/macOS bash:

   ```bash
   git clone https://github.com/microsoft-hacks/Frontier-Hack.git
   cd Frontier-Hack
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Sign in, verify the subscription, and provision. Enter a unique name such as `electric-plant-youralias-01` and use `swedencentral`.

   ```powershell
   az login --tenant <your-tenant-id>
   az account list --output table
   az account set --subscription <subscription-id>
   az account show --output table
   azd auth login
   azd env new electric-plant-youralias-01
   azd env set AZURE_LOCATION swedencentral
   azd up
   ```

4. Copy the root `.env` into the lab folder.

   PowerShell:

   ```powershell
   Copy-Item .env labs/electric-plant-portal/.env
   ```

   Bash:

   ```bash
   cp .env labs/electric-plant-portal/.env
   ```

5. In the [Azure portal](https://portal.azure.com), confirm the resource group contains a Foundry resource/project, model deployment, Application Insights, and Log Analytics workspace.
6. In the [Microsoft Foundry portal](https://ai.azure.com/nextgen), open the project. Under **Build** → **Models** or **Deployments**, confirm the deployed model status is **Succeeded**.
7. Open the model playground, send `Reply with: portal setup verified`, and confirm a response appears.

## Success criteria
- [ ] The project is visible and model deployment shows **Succeeded**
- [ ] The model playground answers
- [ ] `labs/electric-plant-portal/.env` exists

Next: [Challenge 1 - Build agents](../challenge-1-build/README.md)