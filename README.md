# SupplyAI free skills

Free, tested Agent Skills from [SupplyAI](https://supplyai.pro), published by Intelligent Assembly. Each one is a working slice of a larger SupplyAI kit; the full plugins and paid kits are at https://supplyai.pro.

| Skill | What it does | Full version |
| --- | --- | --- |
| [Governed Builds](plugins/governed-builds/README.md) | Run B0-B6 ship gates and refuse to mark work shipped while a gate is missing or failing. Use when preparing a merge or running verify. | [governed-builds-plugin](https://supplyai.pro/kits/supplyaipro/governed-builds-plugin), [enterprise-delivery-stack](https://supplyai.pro/kits/supplyaipro/enterprise-delivery-stack) |
| [UI Motion](plugins/ui-motion/README.md) | Adds page-enter and card-lift CSS with prefers-reduced-motion overrides. Use when implementing UI animation, transitions, or hover lift. | [ui-motion-plugin](https://supplyai.pro/kits/supplyaipro/ui-motion-plugin) |

## Install

| Host | Command |
| --- | --- |
| Claude Code | `claude plugin marketplace add teknoledg/supplyai-free-skills` then `claude plugin install <skill>@supplyai-free` |
| Codex | `codex plugin marketplace add teknoledg/supplyai-free-skills` then `codex plugin add <skill>@supplyai-free` |
| claude.ai | Upload `skills-zips/<skill>.zip` under Customize > Skills |
| Cursor | `./install.sh --host cursor` (project) or `--scope user` |
| VS Code (GitHub Copilot) | `./install.sh --host vscode` (`.github/skills`) |
| Antigravity | `./install.sh --host antigravity` (`.agents/skills`) or `--scope user` (`~/.gemini/config/skills`) |
| Devin | `./install.sh --host devin` (`.agents/skills`) |
| npm (any host above) | `npx @supplyaipro/<skill> --host <cursor\|vscode\|antigravity\|devin\|codex\|claude>` |

## Verification

Every skill here was certified in Cursor against its own example project (`plugins/<skill>/skills/<skill>/tests/example-project/`): behaviour scenarios, activation checks, a no-test-leakage gate and the Agent Skills validator. Run a scenario yourself with `python3 tests/example-project/grade.py list` from the skill folder.

Licence: MIT. Privacy: https://supplyai.pro/privacy. Terms: https://supplyai.pro/terms.
