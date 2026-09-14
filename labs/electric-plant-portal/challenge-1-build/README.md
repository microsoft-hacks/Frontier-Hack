# Challenge 1: Build agents in the portal

Time: ~35 minutes

## Objectives
- ✅ Create two exact agent definitions and attach one OpenAPI data tool to the classifier

## Context
An agent combines a model, instructions, and optional tools. A **function** runs application code; **OpenAPI** calls a described HTTP API; **Azure AI Search** retrieves indexed enterprise content; **Code Interpreter** calculates and analyzes files; **File Search** retrieves from uploaded files. The model decides to call a tool based only on its **name and description**, so vague descriptions are the most common reason a tool is ignored.

The facilitator must provide a deployed industrial API URL. `openapi.json` contains `https://YOUR-API-HOST.example.com`, which is a placeholder, not a real deployment. Confirm the supplied URL responds before attaching it.

## Get started

1. Replace the placeholder `servers[0].url` in `labs/electric-plant-portal/challenge-1-build/openapi.json` with the facilitator-confirmed HTTPS base URL. Check it in a browser by opening `<confirmed-url>/assets/DRIVE-103/condition`; JSON containing DRIVE-103 must appear. If it does not, stop and ask the facilitator to confirm the endpoint. Participants do not deploy or write API code.
2. In Foundry, open the project, then **Build** → **Agents** → **+ New agent**. Select the model deployed in Challenge 0 and use this exact name:

   ```text
   electric-plant-1-classifier-agent
   ```

3. Paste these complete instructions:

   ```text
## Purpose
-  You are AI assistant for Northline Electrics that helps user to classify assets conditions. 

## Context
Try load data via tools or use default thresholds =
- vibration: 0-4.0 mm/s RMS
- winding temperature: 20-85 Celsius
- current load: 25-90 % 
- operating efficiency: 90-100 %.

## Output-Format
- Classification Summary table ONLY
- rows = for each drive.
- columns = for each metric
- use 🔴 for critical, ⚠️ for high, and ✅ for low.
- add column priority based on metrics classification

## Scope
- Before answering, check if the request is related to this Purpose.
- If in scope: continue with conversation.
- If out of scope: do not answer the request content. Just explain your purpose

## Guardrails
- Do not create customer data.
- Do not recommend anything
- If key data is missing, ask precise follow-up questions.
   ```

4. Save. Select **Tools** → **+ Add** → **OpenAPI**. Choose **Upload file**, select `labs/electric-plant-portal/challenge-1-build/openapi.json`, use **Anonymous** authentication, and confirm the imported operation is exactly `get_asset_condition`. Save the tool.
5. Create another agent with the same deployed model and exact name:

   ```text
   maintenance-efficiency-advisor-agent
   ```

6. Paste these instructions and save. Do not attach a tool.

   ```text
   ## Purpose
   Turn a classifier's structured findings into maintenance actions, urgency, and escalation guidance for Northline Electrics.

   ## OutputFormat
   For each asset, return Status, Urgency, Evidence received, Recommended action, and Escalation. Use exactly: 🔴 critical, ⚠️ warning, ✅ normal.

   ## Scope
   Use only classifier findings supplied in the request. For compound vibration and winding-temperature failures, require a controlled shutdown, isolation under site procedure, and immediate safety/maintenance escalation. For warnings, recommend inspection or planned maintenance. For normal assets, continue monitoring.

   ## Guardrails
   Do not invent, alter, or reclassify readings or thresholds. Do not claim a shutdown occurred. Preserve uncertainty and direct personnel to approved site safety procedures.
   ```

7. Test the classifier:

   ```text
   Call get_asset_condition for DRIVE-101, DRIVE-102, DRIVE-103, DRIVE-104, and DRIVE-105. Classify every result using each asset's thresholds.
   ```

   Expected: exactly 2 ✅ normal, 2 ⚠️ warning, and 1 🔴 critical; DRIVE-103 evidence includes vibration 7.6 over 4.5 and temperature 112 over 90. Expand tool-call details to inspect each request and response.

8. Test the advisor:

   ```text
   Classifier finding: DRIVE-103 is critical because vibration 7.6 exceeds 4.5 mm/s RMS and winding temperature 112 exceeds 90 C. Give urgency, action, and escalation.
   ```

   Expected: controlled shutdown under site procedure and immediate safety/maintenance escalation, with no invented readings.

If the classifier asks you for readings instead of calling the tool, its tool description is too vague, the placeholder was not replaced, or the endpoint is unreachable.

## Success criteria
- [ ] Both exact agent names exist
- [ ] The classifier calls only `get_asset_condition` and returns only a table
- [ ] The distribution is 2 normal, 2 warning, 1 critical
- [ ] The advisor has no tool and does not invent readings

Next: [Challenge 2 - Monitor](../challenge-2-monitor/README.md)