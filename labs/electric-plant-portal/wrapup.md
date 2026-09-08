# Electric Plant portal wrap-up

| Challenge | Skill practiced |
|---|---|
| 0 | Shared Foundry provisioning and portal verification |
| 1 | Portal agent instructions and OpenAPI tools |
| 2 | Foundry and Application Insights monitoring |
| 3 | Dataset-based quality evaluation |
| 4 | Visual multi-agent workflow orchestration |

Next, expand the dataset with approved domain cases, rerun evaluations after instruction changes, and use traces to distinguish operational faults from quality faults.

## Cleanup

Azure resources keep costing money until deleted. From the repository root:

```powershell
azd down --purge --force
```

The facilitator who deployed the optional API must also run the cleanup command printed by `deploy-api-data.ps1`:

```powershell
az group delete --name <api-resource-group> --yes --no-wait
```

Portal alternative: open each workshop resource group in Azure portal, select **Delete resource group**, type its name, and confirm.