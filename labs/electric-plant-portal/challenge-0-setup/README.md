# Challenge 0: Configurar o Microsoft Foundry

Tempo: ~20 minutos

## Objetivos
- ✅ Provisionar o projeto compartilhado do Foundry e verificar o acesso ao portal

## Contexto
O laboratório reutiliza a infraestrutura da raiz do repositório e a convenção `.env` sem alterar `infra/main.bicep`. O trabalho com agentes depois da configuração ocorre inteiramente no portal. Cada participante deve usar um nome de ambiente exclusivo.

## Primeiros passos

1. Confirme o acesso a uma assinatura do Azure com **Contributor** e **Azure AI User/Foundry User**, além de Git, Python 3.10+, Azure CLI, Azure Developer CLI e um terminal. Python faz parte da configuração comum do workshop, mas não é usado para construir este percurso de portal.
2. Clone o repositório e prepare um ambiente.

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

3. Entre com a sua conta, verifique a assinatura e faça o provisionamento. Informe um nome exclusivo como `electric-plant-youralias-01` e use `swedencentral`.

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

4. Copie o `.env` da raiz para a pasta do laboratório.

   PowerShell:

   ```powershell
   Copy-Item .env labs/electric-plant-portal/.env
   ```

   Bash:

   ```bash
   cp .env labs/electric-plant-portal/.env
   ```

5. No [portal do Azure](https://portal.azure.com), confirme que o grupo de recursos contém um recurso/projeto do Foundry, um deployment de modelo, o Application Insights e um workspace do Log Analytics.
6. No [portal do Microsoft Foundry](https://ai.azure.com/nextgen), abra o projeto. Em **Build** → **Models** ou **Deployments**, confirme que o status do modelo implantado é **Succeeded**.
7. Abra o playground do modelo, envie `Reply with: portal setup verified` e confirme que uma resposta aparece.

## Critérios de sucesso
- [ ] O projeto está visível e o deployment do modelo mostra **Succeeded**
- [ ] O playground do modelo responde
- [ ] `labs/electric-plant-portal/.env` existe

Próximo: [Challenge 1 - Build](../challenge-1-build/README.md)