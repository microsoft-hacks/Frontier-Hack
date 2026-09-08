# Challenge 2: Monitor in Foundry

Time: ~20 minutes

## Objectives
- ✅ Generate and inspect traces in Foundry and Application Insights without code

## Context
Monitoring answers **is it running?** It exposes spans, tool calls, latency, tokens, errors, and cost, but does not prove the answer is correct.

## Get started

1. Open the copied `.env` and confirm it contains `PROJECT_CONNECTION_STRING`, `APPLICATIONINSIGHTS_CONNECTION_STRING`, `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true`, and `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`.
2. In Foundry, open **Observability** → **Tracing**. If a connect banner appears, select **Connect Application Insights**, choose the instance in the lab resource group, and save this one-time connection.
3. Open `electric-plant-1-classifier-agent` in the playground and run:

   ```text
   Call get_asset_condition for DRIVE-103 and classify it. Return only the required table.
   ```

   Expected: a 🔴 critical row and a visible `get_asset_condition` call.

4. Return to **Observability** → **Tracing**, open the newest conversation, and inspect the root span, model span, OpenAPI tool call, request/response, full message content, tokens, latency, and status.
5. Open the agent's **Monitor** panel and read agent runs, token usage, and estimated cost.
6. In Azure portal, open Application Insights → **Transaction search**, choose the recent end-to-end transaction, and review the agent dashboard for runs, errors, tool calls, models, and token consumption.

## Success criteria
- [ ] At least one trace appears in Foundry and Application Insights
- [ ] The OpenAPI request and response are visible
- [ ] You can explain where to investigate errors, latency, and unexpected tool behavior

Next: [Challenge 3 - Evaluate](../challenge-3-evaluate/README.md)