# Governed Builds (free)

Run B0-B6 ship gates and refuse to mark work shipped while a gate is missing or failing. Use when preparing a merge or running verify.

Published by Intelligent Assembly. Part of the SupplyAI catalogue: https://supplyai.pro/kits/supplyaipro/governed-builds

## Install

- **Claude Code:** `claude plugin marketplace add teknoledg/supplyai-free-skills`, then `claude plugin install governed-builds@supplyai-free`
- **Codex:** `codex plugin marketplace add teknoledg/supplyai-free-skills`, then `codex plugin add governed-builds@supplyai-free`
- **claude.ai:** upload `skills-zips/governed-builds.zip` under Customize > Skills
- **Cursor, VS Code, Antigravity, Devin:** `./install.sh --host <cursor|vscode|antigravity|devin> --skill governed-builds`
- **npm:** `npx @supplyaipro/governed-builds --host <cursor|vscode|antigravity|devin|codex|claude>`

## Get the full set

- [governed-builds-plugin](https://supplyai.pro/kits/supplyaipro/governed-builds-plugin): Governed Builds plugin: rules, hooks, charter and status CLI installed into your repo
- [enterprise-delivery-stack](https://supplyai.pro/kits/supplyaipro/enterprise-delivery-stack): Enterprise Delivery Stack: UI foundation, vault and ship gates in one install

## Verification

Certified on 2026-10-02 in Cursor (default model) against its bundled example project: every scenario, activation check and gate passed. Certificate tree hash `be57fb762825bc11`. Scenarios and grader: `skills/governed-builds/tests/example-project/`.

Licence: MIT. See `LICENSE`.
