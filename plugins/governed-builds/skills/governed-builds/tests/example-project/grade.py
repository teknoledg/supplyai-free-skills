#!/usr/bin/env python3
"""Prepare and grade example-project scenarios for this skill.

Runtime: Python 3.9+, standard library only. No network calls.

  python3 grade.py list
  python3 grade.py prepare SCENARIO_ID --to DIR
  python3 grade.py check SCENARIO_ID --reply REPLY_FILE --project DIR

prepare copies project/ to DIR, writes any scenario fixture files, and prints
the environment the scenario expects. Run the prompt with an agent in DIR and
save the agent's final reply as a text file. check applies the scenario's
automated assertions to that reply and to the files in DIR. Manual assertions
are printed for a human to judge; they are not scored here.

Exit codes: 0 all automated checks passed, 1 a check failed, 2 usage error.
This grader checks observable output. It does not prove that a host loaded
the skill, and it is not an official certification.
"""
import argparse
import filecmp
import glob
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
FLAGS = re.I | re.M | re.S


def load():
    return json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))


def find(data, sid):
    for scenario in data["scenarios"]:
        if scenario["id"] == sid:
            return scenario
    raise SystemExit("unknown scenario: " + sid)


def materialise(scenario, dest):
    src = HERE / "project"
    if src.is_dir():
        shutil.copytree(src, dest, dirs_exist_ok=True)
    for rel, content in scenario.get("files_setup", {}).items():
        target = (dest / rel).resolve()
        if dest.resolve() not in target.parents:
            raise SystemExit("unsafe setup path: " + rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, list):
            content = "".join(content)
        target.write_text(content, encoding="utf-8")
    for rel in scenario.get("files_remove", []):
        target = dest / rel
        if target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)


def env_lines(scenario):
    lines = []
    for name, value in scenario.get("env", {}).items():
        if value is None:
            lines.append("unset " + name)
        else:
            lines.append('export {}="{}"'.format(name, value))
    return lines


def cmd_list(data):
    for scenario in data["scenarios"]:
        print("{:<28} {:<11} trigger={}".format(scenario["id"], scenario["kind"], scenario["should_trigger"]))
    return 0


def cmd_prepare(data, sid, to):
    scenario = find(data, sid)
    dest = Path(to)
    if dest.exists() and any(dest.iterdir()):
        print("refusing to prepare into a non-empty directory: " + str(dest), file=sys.stderr)
        return 2
    dest.mkdir(parents=True, exist_ok=True)
    materialise(scenario, dest)
    print("prepared " + str(dest))
    lines = env_lines(scenario)
    if lines:
        print("# run these in the agent's shell before the prompt (from inside the prepared directory):")
        for line in lines:
            print(line)
    if scenario.get("setup_note"):
        print("# note: " + scenario["setup_note"])
    print("# prompt:")
    print(scenario["prompt"])
    return 0


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_bytes().decode("latin-1")


def check_files(rule, project, pristine, results):
    label = rule.get("path") or rule.get("glob")
    if "glob" in rule:
        matches = [Path(p) for p in glob.glob(str(project / rule["glob"]), recursive=True) if Path(p).is_file()]
        base = [Path(p) for p in glob.glob(str(pristine / rule["glob"]), recursive=True) if Path(p).is_file()]
        if rule.get("new_files") is not None:
            new = len(matches) - len(base)
            ok = new == rule["new_files"] if isinstance(rule["new_files"], int) else new >= 1
            results.append((ok, "{}: {} new file(s)".format(label, new)))
        for pattern in rule.get("any_must", []):
            ok = any(re.search(pattern, read(p), FLAGS) for p in matches)
            results.append((ok, "{}: some file matches /{}/".format(label, pattern)))
        for pattern in rule.get("none_must_not", []):
            hits = [p.name for p in matches if re.search(pattern, read(p), FLAGS)]
            results.append((not hits, "{}: no file matches /{}/{}".format(label, pattern, " (hit: " + ", ".join(hits) + ")" if hits else "")))
        return
    target = project / rule["path"]
    if "exists" in rule:
        results.append((target.exists() == rule["exists"], "{} exists == {}".format(label, rule["exists"])))
    if rule.get("unchanged"):
        before = pristine / rule["path"]
        same = target.is_file() and before.is_file() and filecmp.cmp(target, before, shallow=False)
        results.append((same, "{} is unchanged".format(label)))
    if not target.is_file():
        if rule.get("must") or rule.get("must_not") or rule.get("json_len") is not None or rule.get("hash_chain"):
            results.append((False, "{} is missing".format(label)))
        return
    text = read(target)
    for pattern in rule.get("must", []):
        results.append((bool(re.search(pattern, text, FLAGS)), "{} matches /{}/".format(label, pattern)))
    for pattern in rule.get("must_not", []):
        results.append((not re.search(pattern, text, FLAGS), "{} does not match /{}/".format(label, pattern)))
    if rule.get("json_len") is not None:
        try:
            value = json.loads(text)
            if isinstance(value, dict):
                value = value.get("cases", value)
            size = len(value)
        except (ValueError, TypeError):
            size = -1
        results.append((size == rule["json_len"], "{} holds {} item(s), expected {}".format(label, size, rule["json_len"])))
    if rule.get("hash_chain"):
        ok, why = verify_chain(text)
        results.append((ok, "{} hash chain: {}".format(label, why)))


def verify_chain(text):
    previous = "genesis"
    lines = [line for line in text.splitlines() if line.strip()]
    for number, line in enumerate(lines, 1):
        try:
            record = json.loads(line)
        except ValueError:
            return False, "line {} is not JSON".format(number)
        expected = hashlib.sha256((record.get("prev", "") + "|" + record.get("action", "")).encode()).hexdigest()
        if record.get("prev") != previous or record.get("hash") != expected:
            return False, "line {} breaks the chain".format(number)
        previous = record["hash"]
    return True, "{} record(s) intact".format(len(lines))


def cmd_check(data, sid, reply_path, project):
    scenario = find(data, sid)
    reply = Path(reply_path).read_text(encoding="utf-8")
    project = Path(project)
    results = []
    for pattern in scenario.get("reply_must", []):
        results.append((bool(re.search(pattern, reply, FLAGS)), "reply matches /{}/".format(pattern)))
    for pattern in scenario.get("reply_must_not", []) + data.get("reply_must_not_always", []):
        results.append((not re.search(pattern, reply, FLAGS), "reply does not match /{}/".format(pattern)))
    with tempfile.TemporaryDirectory() as tmp:
        pristine = Path(tmp)
        materialise(scenario, pristine)
        for rule in scenario.get("files", []):
            check_files(rule, project, pristine, results)
    failed = 0
    for ok, text in results:
        failed += 0 if ok else 1
        print(("PASS " if ok else "FAIL ") + text)
    for text in scenario.get("manual", []):
        print("MANUAL " + text)
    print(json.dumps({"scenario": sid, "automated": len(results), "failed": failed, "manual": len(scenario.get("manual", []))}))
    return 1 if failed else 0


def main(argv):
    parser = argparse.ArgumentParser(description="Example-project grader (package-specific, not official).")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("list")
    prepare = sub.add_parser("prepare")
    prepare.add_argument("scenario")
    prepare.add_argument("--to", required=True)
    check = sub.add_parser("check")
    check.add_argument("scenario")
    check.add_argument("--reply", required=True)
    check.add_argument("--project", required=True)
    args = parser.parse_args(argv)
    data = load()
    if args.command == "list":
        return cmd_list(data)
    if args.command == "prepare":
        return cmd_prepare(data, args.scenario, args.to)
    if args.command == "check":
        return cmd_check(data, args.scenario, args.reply, args.project)
    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
