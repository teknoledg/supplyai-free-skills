# Package Instructions

## Format and compatibility

This package follows the shared Agent Skills directory format used by Claude and other adopting agents. The required file is uppercase SKILL.md with YAML frontmatter containing name and description, followed by Markdown instructions. The skill directory name equals its frontmatter name: `ui-motion`.

There is no format supported by every AI system. Discovery paths, installation UI, permissions, and resource execution are host-specific. This package requires no external services or MCP connectors. The optional checker requires Python 3.9+.

## Host conflicts flagged on 29 September 2026

- The shared specification allows descriptions up to 1024 characters. Claude's help page currently recommends a 200-character maximum. This package stays at or below 200 and puts non-activation guidance in the body and in the negative test.
- Claude's help example shows a lowercase skill.md and a display-style name. The specification requires uppercase SKILL.md and a lowercase hyphenated name that matches the directory. This package follows the specification and the sample package.
- Optional specification fields such as license, compatibility, metadata, and allowed-tools are omitted. The sample checker pattern expects exactly name and description, which also avoids host-specific fields.
- Claude help mentions a dependencies frontmatter field. The specification does not. Dependencies for the checker are stated here: Python 3.9+, standard library only.

## Provenance

Rebuilt from the current catalogue kit `@supplyaipro/ui-motion` version `1.0.1` in the `ia` collection. The catalogue record lists licence text "MIT". This package does not assign a new licence or ownership. Add an explicit licence before publishing if one is required.

Older catalogue copies of the same kit were not packaged again. A malformed catalogue directory whose name contains spaces was excluded because it is not a single kit.

## Files

| Path | Status | Purpose |
| --- | --- | --- |
| SKILL.md | Required shared format | Metadata and workflow |
| references/ | Optional shared convention | On-demand guidance |
| assets/output-structure.md | Optional shared convention | Output structure resource |
| assets/ui-motion-starter.css | Optional shared convention | Copy-paste page-enter and card-lift CSS with reduced-motion overrides |
| references/implementation-guide.md | Optional shared convention | Where to map selectors and which files to leave alone |
| scripts/check_package.py | Optional shared convention | Executable package checker |
| tests/sample-tests.json | Package-specific optional file | Behaviour prompts and expected assertions |
| agents/openai.yaml | Optional OpenAI-specific metadata | Display name and example invocation |

No universal README, manifest, or test filename is required. Hosts may ignore agents/openai.yaml. The portable workflow does not depend on it.

## Install and use

For Claude's custom-skill upload, upload `ui-motion.zip` through its Skills interface and enable it. The archive contains one `ui-motion` folder at its root, with SKILL.md immediately inside.

For a filesystem-based compatible agent, extract the folder into the skill-discovery directory specified by that agent's documentation. Avoid adding another wrapper folder. For hosts without skill loading, provide SKILL.md and its referenced resources as context. Automatic discovery will not be available.

Creating this archive does not install the skill. Example request: "Apply the ui-motion starter enter and lift patterns, and honour prefers-reduced-motion."

## Adapt and redistribute

Change the folder name and frontmatter name together. Update the description with concrete trigger terms. Replace workflow, examples, and tests for a new domain. Update optional OpenAI metadata if retained. Re-run checks and behavioural evaluations after changes.

Never include credentials or private customer data in reusable examples.

## Sources checked 29 September 2026

- Shared format: https://agentskills.io/specification
- Authoring practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude packaging: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- Example skills: https://github.com/anthropics/skills
