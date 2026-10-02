#!/usr/bin/env python3
"""Check this package's structure and fixtures. Not an official skills-ref certification."""
import json
import re
import sys
from pathlib import Path

SKILL_NAME = 'ui-motion'
FIXTURE_FORMAT = 'ui-motion-example-tests-v1'
MAX_DESCRIPTION = 200


def check(root):
    errors = []
    required = [
        "SKILL.md",
        "assets/output-structure.md",
        "references/quality-rubric.md",
        "references/testing.md",
        "references/package-instructions.md",
        "tests/sample-tests.json",
        "agents/openai.yaml",
        "scripts/check_package.py",
    ]
    for relative in required:
        if not (root / relative).is_file():
            errors.append("Missing file: " + relative)
    skill = root / "SKILL.md"
    content = ""
    if skill.is_file():
        content = skill.read_text(encoding="utf-8")
        if content.count("\n") + 1 > 500:
            errors.append("SKILL.md exceeds 500 lines")
        match = re.match(r"\A---\n(.*?)\n---\n(.+)\Z", content, re.S)
        if not match:
            errors.append("Expected YAML frontmatter followed by a non-empty Markdown body")
        else:
            fields = {}
            for line in match.group(1).splitlines():
                key, separator, value = line.partition(":")
                if not separator or key in fields:
                    errors.append("Invalid or duplicate frontmatter line: " + line)
                    continue
                fields[key] = value.strip()
            if set(fields) != {"name", "description"}:
                errors.append("This package requires exactly name and description")
            name = fields.get("name", "")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or not 1 <= len(name) <= 64:
                errors.append("Invalid skill name")
            if name != root.name or name != SKILL_NAME:
                errors.append("Skill name differs from parent directory")
            raw = fields.get("description", "")
            if len(raw) >= 2 and raw[0] == raw[-1] == '"':
                try:
                    description = json.loads(raw)
                except ValueError:
                    description = None
                    errors.append("Description is not valid JSON string syntax")
            else:
                description = raw
            if not isinstance(description, str) or not 1 <= len(description) <= MAX_DESCRIPTION:
                errors.append("Description must contain 1-200 characters for the Claude help limit")
            elif "<" in description or ">" in description:
                errors.append("Description contains an XML-like angle bracket")
            body = match.group(2)
            for heading in ("## Workflow", "## Rules", "## Example", "## Evaluation and Maintenance"):
                if heading not in body:
                    errors.append("Missing section: " + heading)
        for link in re.findall(r"\]\(([^)]+)\)", content):
            if "://" in link or link.startswith("#"):
                continue
            target = (root / link.split("#")[0]).resolve()
            if root.resolve() not in target.parents or not target.is_file():
                errors.append("Missing or unsafe resource link: " + link)
    fixture = root / "tests/sample-tests.json"
    if fixture.is_file():
        try:
            data = json.loads(fixture.read_text(encoding="utf-8"))
            if data.get("format") != FIXTURE_FORMAT:
                errors.append("Unexpected fixture format")
            cases = data.get("cases")
            if not isinstance(cases, list) or len(cases) < 3:
                errors.append("Cases must include success, edge, and non-trigger prompts")
            else:
                identifiers = set()
                triggers = []
                for case in cases:
                    if not isinstance(case, dict):
                        errors.append("Each case must be an object")
                        continue
                    identifier = case.get("id")
                    if not isinstance(identifier, str) or not identifier or identifier in identifiers:
                        errors.append("Case identifiers must be unique non-empty strings")
                    else:
                        identifiers.add(identifier)
                    if not isinstance(case.get("should_trigger"), bool):
                        errors.append("should_trigger must be boolean")
                    else:
                        triggers.append(case["should_trigger"])
                    if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
                        errors.append("Each prompt must be non-empty")
                    expected = case.get("expected")
                    if not isinstance(expected, list) or not expected or not all(isinstance(x, str) and x.strip() for x in expected):
                        errors.append("Expected assertions must be non-empty strings")
                    kind = case.get("kind")
                    if kind not in ("success", "edge", "non-trigger"):
                        errors.append("Each case needs kind success, edge, or non-trigger")
                if True not in triggers or False not in triggers:
                    errors.append("Include a positive case and a negative discovery case")
                kinds = [c.get("kind") for c in cases if isinstance(c, dict)]
                if "success" not in kinds or "edge" not in kinds or "non-trigger" not in kinds:
                    errors.append("Include success, edge, and non-trigger kinds")
        except (ValueError, AttributeError) as exc:
            errors.append("Invalid fixture: " + str(exc))
    return errors


def main():
    root = Path(__file__).resolve().parents[1]
    try:
        errors = check(root)
    except (OSError, UnicodeError) as exc:
        errors = [str(exc)]
    print(json.dumps({"status": "failed" if errors else "passed", "skill": SKILL_NAME, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
