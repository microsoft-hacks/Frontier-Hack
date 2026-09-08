# Electric Plant SDK wrap-up

| Challenge | Skill practiced |
|---|---|
| 0 | Shared Foundry provisioning and authentication |
| 1 | Prompt agents, strict function schemas, and tool grounding |
| 2 | OpenTelemetry tracing and operational monitoring |
| 3 | Dataset-based answer quality evaluation |
| 4 | Correlated function calls and multi-agent handoff |

Next, apply the same separation of evidence and advice to your own domain, add more edge cases, and use evaluation regressions before changing instructions.

## Cleanup

Resources continue to incur charges until deleted. From the repository root, remove the shared `azd` environment:

```powershell
azd down --purge --force
```

If the optional industrial API was deployed, delete its separate resource group using the exact command printed by `deploy-api-data.ps1`:

```powershell
az group delete --name <api-resource-group> --yes --no-wait
```

Portal alternative: open each lab resource group in the Azure portal, select **Delete resource group**, type its name, and confirm.