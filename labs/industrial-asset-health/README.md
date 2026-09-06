# Industrial Asset Health (SDK)

Northline Motion Works operates the fictional Riverbend Electrification Plant. Five drive assets report vibration, winding temperature, current load, and operating efficiency. Your mission is to build a tool-grounded classifier and a separate maintenance advisor, observe and evaluate them, then orchestrate their handoff.

| Asset | Name | Status | Current issue |
|---|---|---|---|
| DRIVE-101 | Primary Coil Line Drive | ✅ normal | None |
| DRIVE-102 | Busbar Forming Drive | ⚠️ warning | Vibration above its asset-specific maximum |
| DRIVE-103 | High-Load Lamination Press Drive | 🔴 critical | Compound vibration and temperature failure; controlled shutdown and escalation required |
| DRIVE-104 | Rotor Assembly Conveyor Drive | ✅ normal | None |
| DRIVE-105 | Final Test Dynamometer Drive | ⚠️ warning | Efficiency below its asset-specific minimum |

The canonical readings and thresholds are in [`api-industrial/data/industrial_asset_data.json`](api-industrial/data/industrial_asset_data.json).

| Challenge | Time | Outcome |
|---|---:|---|
| [0 - Setup](challenge-0-setup/README.md) | 20 min | Provision and verify Foundry |
| [1 - Build](challenge-1-build/README.md) | 35 min | Create both agents and attach one function tool |
| [2 - Monitor](challenge-2-monitor/README.md) | 20 min | Inspect traces and operational telemetry |
| [3 - Evaluate](challenge-3-evaluate/README.md) | 30 min | Evaluate 10 quality cases |
| [4 - Workflow](challenge-4-workflow/README.md) | 25 min | Run classifier-to-advisor orchestration |

Start with [Challenge 0](challenge-0-setup/README.md).