#!/usr/bin/env node
// Install this SupplyAI skill into an Agent Skills host. Node 18+, no dependencies.
// npx @supplyaipro/governed-builds --host <cursor|vscode|antigravity|devin|codex|claude> [--scope project|user] [--dest DIR]
import { cpSync, existsSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const skill = "governed-builds";
const args = process.argv.slice(2);
const opt = (flag, fallback) => { const i = args.indexOf(flag); return i >= 0 && args[i + 1] ? args[i + 1] : fallback; };
if (args.includes("-h") || args.includes("--help") || !args.includes("--host")) {
  console.log(`Usage: npx @supplyaipro/${skill} --host <cursor|vscode|antigravity|devin|codex|claude> [--scope project|user] [--dest DIR]`);
  process.exit(args.includes("--host") ? 0 : 2);
}
const host = opt("--host"), scope = opt("--scope", "project");
const base = scope === "user" ? homedir() : process.cwd();
const targets = {
  cursor: join(base, ".cursor/skills"),
  vscode: scope === "user" ? join(homedir(), ".copilot/skills") : join(base, ".github/skills"),
  antigravity: scope === "user" ? join(homedir(), ".gemini/config/skills") : join(base, ".agents/skills"),
  devin: join(base, ".agents/skills"),
  codex: join(base, ".agents/skills"),
  claude: join(base, ".claude/skills"),
};
const dest = opt("--dest") ? resolve(opt("--dest")) : targets[host];
if (!dest) { console.error(`unknown --host '${host}' (${Object.keys(targets).join(", ")})`); process.exit(2); }
const src = join(dirname(fileURLToPath(import.meta.url)), "..", "skills", skill);
const out = join(dest, skill);
if (existsSync(out)) { console.error(`exists, not overwriting: ${out}`); process.exit(1); }
mkdirSync(dest, { recursive: true });
cpSync(src, out, { recursive: true });
console.log(`installed ${skill} -> ${out}`);
