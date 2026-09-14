# Encerramento da Usina Elétrica (SDK)

| Challenge | Habilidade praticada |
|---|---|
| 0 | Provisionamento compartilhado do Foundry e autenticação |
| 1 | Prompt de agentes, schemas estritos de funções e ancoragem em ferramentas (função + Azure AI Search/RAG) |
| 2 | Rastreamento OpenTelemetry e monitoramento operacional |
| 3 | Avaliação da qualidade das respostas baseada em dataset, incluindo citações da base |
| 4 | Chamadas correlacionadas, conhecimento recuperado e passagem entre múltiplos agentes |

Em seguida, aplique a mesma separação entre evidência e recomendação no seu próprio domínio, popule um índice de busca com a sua documentação de manutenção, adicione mais casos de borda e use regressões de avaliação antes de alterar instruções. O índice de demonstração pode ser recriado com `scripts/deploy-search-electric-plant.ps1`.

## Limpeza

Os recursos continuam gerando cobrança até serem excluídos. Pela raiz do repositório, remova o ambiente `azd` compartilhado:

```powershell
azd down --purge --force
```

Se a API industrial opcional foi implantada, exclua o grupo de recursos separado usando o comando exato impresso por `deploy-api-data.ps1`:

```powershell
az group delete --name <api-resource-group> --yes --no-wait
```

Se o Azure AI Search compartilhado foi provisionado para este laboratório, exclua o grupo de recursos com o nome impresso no final da execução do script `scripts/deploy-search-electric-plant.ps1` (por padrão `rg-search-shared`):

```powershell
az group delete --name rg-search-shared --yes --no-wait
```

Alternativa pelo portal: abra cada grupo de recursos do laboratório no portal do Azure, selecione **Delete resource group**, digite o nome e confirme.