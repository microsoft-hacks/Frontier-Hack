# Challenge 1: Build tool-grounded agents

Time: ~35 minutes

## Objectives
- ✅ Create the classifier with exactly one attached function tool and the tool-free advisor

## Context
An agent combines a model, instructions, and optional tools. A **function** runs local code; **OpenAPI** calls a described HTTP API; **Azure AI Search** retrieves indexed enterprise content; **Code Interpreter** calculates and analyzes files; **File Search** retrieves from uploaded files. The model decides whether to call a tool only from its **name and description**, so a vague description is the most common reason a tool is ignored.

The classifier obtains evidence and never recommends actions. The advisor receives grounded findings and never invents readings.

## Get started

1. Open `agents.py`. It defines `get_asset_condition(asset_id)` and an identically named `FunctionTool`, attaches that tool to `asset-health-classifier-agent`, and creates `maintenance-efficiency-advisor-agent` without tools.
2. From the repository root, run:

   ```powershell
   Set-Location labs/industrial-asset-health
   python challenge-1-build/agents.py
   ```

   Expected output names both created agent versions, explicitly says the classifier has `get_asset_condition`, and prints a DRIVE-103 classification containing 🔴 critical with vibration and winding-temperature evidence.

3. In Foundry, open **Build** → **Agents**. Confirm both exact names exist:

   ```text
   asset-health-classifier-agent
   maintenance-efficiency-advisor-agent
   ```

4. Test inline classification in the classifier playground:

   ```text
   Classify this asset using the supplied readings: DRIVE-101, vibration 2.4 mm/s RMS (0-4.0), winding temperature 68 C (20-85), current load 72 percent rated (25-90), operating efficiency 94 percent (90-100).
   ```

   Expected: one table row marked ✅ normal, four in-range readings, and no recommendation.

5. Force the data tool:

   ```text
   Call get_asset_condition for DRIVE-101, DRIVE-102, DRIVE-103, DRIVE-104, and DRIVE-105. Classify every result using each asset's thresholds.
   ```

   Expected: 2 ✅ normal, 2 ⚠️ warning, and 1 🔴 critical. Expand each `get_asset_condition` event in run details and inspect its `asset_id` request and JSON response.

6. Test the advisor with grounded context:

   ```text
   Classifier finding: DRIVE-103 is critical because vibration 7.6 exceeds 4.5 mm/s RMS and winding temperature 112 exceeds 90 C. Give urgency, action, and escalation.
   ```

   Expected: immediate controlled shutdown under site procedure and safety/maintenance escalation, without new readings.

## Success criteria
- [ ] Both exact agent names exist
- [ ] The classifier calls its one tool and returns only a classification table
- [ ] The result distribution is 2 normal, 2 warning, 1 critical
- [ ] The advisor gives actions and urgency without inventing readings

Next: [Challenge 2 - Monitor](../challenge-2-monitor/README.md)