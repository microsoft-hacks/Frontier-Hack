# Encerramento da Usina Elétrica (Portal)

| Challenge | Habilidade praticada |
|---|---|
| 0 | Provisionamento compartilhado do Foundry e verificação no portal |
| 1 | Instruções de agentes e ferramentas OpenAPI no portal |
| 2 | Monitoramento no Foundry e no Application Insights |
| 3 | Avaliação de qualidade baseada em dataset |
| 4 | Orquestração visual de fluxo de trabalho com múltiplos agentes |

Em seguida, expanda o dataset com casos aprovados do domínio, execute novamente avaliações após mudanças de instruções e use traces para distinguir falhas operacionais de falhas de qualidade.

## Limpeza

Os recursos do Azure continuam gerando custo até serem excluídos. Pela raiz do repositório:

```powershell
azd down --purge --force
```

O facilitador que implantou a API opcional também deve executar o comando de limpeza impresso por `deploy-api-data.ps1`:

```powershell
az group delete --name <api-resource-group> --yes --no-wait
```

Alternativa pelo portal: abra cada grupo de recursos do workshop no portal do Azure, selecione **Delete resource group**, digite o nome e confirme.