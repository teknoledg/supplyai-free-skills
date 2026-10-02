# Test Instructions

## Local structure check

From the extracted ui-motion directory run:

```bash
python3 scripts/check_package.py
```

Requires Python 3.9 or newer, standard library only. It checks frontmatter, local links, expected files, and test-case shape. It makes no network calls and writes no files. Exit 0 means pass; exit 1 means failure.

## Behaviour evaluation

Open tests/sample-tests.json. Run each prompt in a fresh conversation with the skill available. Record the host, model, date, activation evidence if exposed, output, and pass or fail notes outside the installed skill.

For positive cases, evaluate every expected assertion and apply references/quality-rubric.md. Do not demand identical wording. Negative cases test whether automatic discovery avoids unrelated tasks; run them without explicitly invoking the skill. A correct answer to an unrelated prompt alone cannot prove non-activation: record host activation logs where available, otherwise mark activation as unobservable.

Test both explicit use and automatic discovery for positive cases. The JSON file is a portable fixture for manual evaluation, not a standardised automatic test runner. The checker validates fixtures but never calls a model. Behaviour tests have not been executed against Claude or other external hosts as part of this package.

## Example project

`tests/example-project/` holds a small workspace (`project/`), `scenarios.json`, and `grade.py` (Python 3.9+, standard library only, no network). See its [README](../tests/example-project/README.md).

```bash
python3 tests/example-project/grade.py list
python3 tests/example-project/grade.py prepare <scenario> --to /tmp/ui-motion-run
# run the printed prompt with an agent inside /tmp/ui-motion-run and save its final reply to reply.md
python3 tests/example-project/grade.py check <scenario> --reply reply.md --project /tmp/ui-motion-run
```

The grader scores the reply and the files the agent left behind. Keep the agent that answers separate from the person or agent that judges the MANUAL lines.
