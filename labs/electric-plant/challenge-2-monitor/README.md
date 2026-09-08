# Challenge 2: Monitor agent execution

Time: ~20 minutes

## Objectives
- ✅ Produce and inspect one end-to-end trace in Foundry and Application Insights

## Context
Monitoring answers **is it running?** through spans, latency, tokens, errors, and cost. It does not answer whether a classification or recommendation is correct; Challenge 3 does that.

## Get started

1. Confirm `.env` includes `PROJECT_CONNECTION_STRING`, `APPLICATIONINSIGHTS_CONNECTION_STRING`, `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true`, and `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true`:

   ```powershell
   Get-Content .env | Select-String 'PROJECT_CONNECTION_STRING|APPLICATIONINSIGHTS_CONNECTION_STRING|AZURE_EXPERIMENTAL|OTEL_INSTRUMENTATION'
   ```

2. In Foundry, open **Observability** → **Tracing**. If a connection banner appears, select **Connect Application Insights**, choose the instance in the lab resource group, and save once.
3. Run the tracing script. It enables instrumentation before creating `AIProjectClient`, verifies that Challenge 1 created `electric-plant-1-classifier-agent`, invokes `get_asset_condition` for DRIVE-103, and deletes the temporary conversation.

   ```powershell
   Set-Location labs/electric-plant
   python challenge-2-monitor/monitor.py
   ```

   Expected terminal result: a critical classification for DRIVE-103 with vibration and winding-temperature evidence.

4. In Foundry **Tracing**, open the newest conversation. Expand spans and inspect full message content, model span, token counts, latency, and status. For tool-call spans, inspect arguments and output.
5. Open `electric-plant-1-classifier-agent`, select its **Monitor** panel, and locate agent runs, token usage, and estimated cost.
6. In the Azure portal, open Application Insights → **Transaction search**, select the recent end-to-end transaction, then review the agent dashboard for runs, errors, tool calls, models, and token consumption.

## Success criteria
- [ ] At least one trace is visible in Foundry and Application Insights
- [ ] You can identify spans, tokens, latency, messages, and tool-call details
- [ ] You can explain where to investigate a failed or slow run

Next: [Challenge 3 - Evaluate](../challenge-3-evaluate/README.md)