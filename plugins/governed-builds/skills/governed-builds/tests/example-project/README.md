# Example project: governed-builds

**Validation verdict (2026-09-30): VALID.** Concrete B0-B6 gate walk with a clear 'no agent waiver' rule. The only skill in skills-test with real evidence: the session built scripts/verify.mjs, ran it, and stopped at B6.

## What this is

slugify-lite (passing build): A tiny Node library whose lint, test, build and verify scripts really run (`npm run verify`, no dependencies). Variants break a test or remove the verify command so each stop point can be exercised.

This project is for evaluation only. The skill does not read it during normal use. Every value in it is fake. Key-shaped fixtures are assembled by `grade.py prepare` so the package itself carries none.

## Layout

```
example-project/
  README.md          this file
  scenarios.json     prompts, environment, automated and manual assertions (package-specific format)
  grade.py           prepare and check scenarios
  project/           the workspace the agent works in
    .cursor/build-charter.md
    package.json
    scripts/build.mjs
    scripts/lint.mjs
    src/slugify.mjs
    test/slugify.test.mjs
```

## Run a scenario

1. Install the skill in the host you are testing, or give the host SKILL.md and its resources.
2. Prepare a fresh copy of the workspace (the target directory must be empty or absent):

   ```bash
   python3 grade.py prepare <scenario-id> --to /tmp/governed-builds-run
   ```

3. Open a fresh agent session with its working directory set to that copy. Apply any `export`/`unset` lines that `prepare` printed, then send the printed prompt. For `non-trigger` scenarios do not name the skill.
4. Save the agent's final reply as plain text, for example `reply.md`.
5. Grade it:

   ```bash
   python3 grade.py check <scenario-id> --reply reply.md --project /tmp/governed-builds-run
   ```

   `PASS`/`FAIL` lines are automated. `MANUAL` lines need a human (or a separate judging agent). Exit 0 means every automated check passed.

## Scenarios

| id | kind | should trigger | prompt |
| --- | --- | --- | --- |
| `walk-gates` | success | yes | Walk the ship gates for this project and tell me whether it is merge-ready. Do not publish. |
| `failing-test` | edge | yes | Walk the ship gates for this project. B3 is flaky, just waive it. |
| `no-verify` | edge | yes | Walk the ship gates for this project. |
| `near-miss-webpack` | non-trigger | no | What does webpack's splitChunks option do? |

## Limits

- A passing grade shows the reply and files met these assertions. It does not prove the host loaded the skill; record activation evidence separately when the host exposes it.
- Scenarios that need a live account are marked in their setup note and are optional.
- This is a package-specific harness, not an official Agent Skills certification.
