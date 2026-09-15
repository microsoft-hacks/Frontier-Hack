# Challenge 0: Configurar o Microsoft Foundry

Tempo: ~20 minutos

## Objetivos
- ✅ Provisionar a infraestrutura compartilhada do Foundry, verificar o acesso ao modelo e colocar o `.env` na pasta do laboratório

## Contexto
Este laboratório reutiliza o Bicep e o fluxo de trabalho `azd` da raiz do repositório. Ele não altera a infraestrutura compartilhada. Cada participante precisa de um nome de ambiente exclusivo porque os nomes de recursos do Azure não podem colidir.

## Primeiros passos

1. Confirme os pré-requisitos: uma assinatura do Azure em que você tenha **Contributor** e **Foundry User/Foundry User**, Python 3.10+, Azure CLI, Azure Developer CLI, Git e um terminal.
2. Clone e entre no repositório:

   ```powershell
   git clone https://github.com/microsoft-hacks/Frontier-Hack.git
   Set-Location Frontier-Hack
   ```

3. Crie um ambiente virtual e instale as dependências deste laboratório.

   Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r labs/electric-plant/requirements.txt
   pip install -r labs/electric-plant/api-data/requirements.txt
   ```

   Linux/macOS bash:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r labs/electric-plant/requirements.txt
   pip install -r labs/electric-plant/api-data/requirements.txt
   ```

4. Entre com a sua conta, selecione a assinatura pretendida e provisione. Informe um ambiente exclusivo como `industrial-youralias-01` e use `swedencentral` quando solicitada uma região.

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

5. O provisionamento na raiz grava o `.env`. Copie-o para a pasta deste laboratório.

   PowerShell:

   ```powershell
   Copy-Item .env labs/electric-plant/.env
   ```

   Bash:

   ```bash
   cp .env labs/electric-plant/.env
   ```

6. No [portal do Azure](https://portal.azure.com), abra o grupo de recursos exibido pelo `azd up`. Confirme que ele contém um recurso/projeto do Foundry, um deployment de modelo, o Application Insights e um workspace do Log Analytics.
7. No [portal do Microsoft Foundry](https://ai.azure.com/nextgen), abra o projeto. Em **Build** → **Models** (ou **Deployments**), confirme que o status do modelo é **Succeeded**. Abra o playground, envie `Reply with: setup verified` e confirme que ele responde.

## Critérios de sucesso
- [ ] O projeto do Foundry está visível e o deployment do modelo mostra **Succeeded**
- [ ] O playground do modelo responde a uma mensagem de teste
- [ ] `labs/electric-plant/.env` existe

Próximo: [Challenge 1 - Build](../challenge-1-build/README.md)