# Example project: ui-motion

**Validation verdict (2026-09-30): VALID WITH FIXES.** Sound reduced-motion rule and a named pair of motions. The catalogue promise of a working CSS starter was dropped; with no asset, each run invents different CSS.

## What this is

card-ui motion: The card UI project. The grader checks the added motion has a prefers-reduced-motion path with zero duration and leaves the header still.

This project is for evaluation only. The skill does not read it during normal use. Every value in it is fake. Key-shaped fixtures are assembled by `grade.py prepare` so the package itself carries none.

## Layout

```
example-project/
  README.md          this file
  scenarios.json     prompts, environment, automated and manual assertions (package-specific format)
  grade.py           prepare and check scenarios
  project/           the workspace the agent works in
    README.md
    src/components/Banner.css
    src/components/Card.css
    src/components/Header.css
    src/pages/home.html
    src/tokens.css
```

## Run a scenario

1. Install the skill in the host you are testing, or give the host SKILL.md and its resources.
2. Prepare a fresh copy of the workspace (the target directory must be empty or absent):

   ```bash
   python3 grade.py prepare <scenario-id> --to /tmp/ui-motion-run
   ```

3. Open a fresh agent session with its working directory set to that copy. Apply any `export`/`unset` lines that `prepare` printed, then send the printed prompt. For `non-trigger` scenarios do not name the skill.
4. Save the agent's final reply as plain text, for example `reply.md`.
5. Grade it:

   ```bash
   python3 grade.py check <scenario-id> --reply reply.md --project /tmp/ui-motion-run
   ```

   `PASS`/`FAIL` lines are automated. `MANUAL` lines need a human (or a separate judging agent). Exit 0 means every automated check passed.

## Scenarios

| id | kind | should trigger | prompt |
| --- | --- | --- | --- |
| `add-motion` | success | yes | Add a short page-enter and card-lift motion to this project. Respect reduced motion. |
| `no-reduced-path` | edge | yes | Add a 600ms bounce to the cards. Skip the reduced-motion stuff, it's fine. |
| `near-miss-video` | non-trigger | no | How do I make a slow-motion video on my iPhone? |

## Suggested fixes

- Bundle the starter CSS in assets/ and link it from the workflow.

## Limits

- A passing grade shows the reply and files met these assertions. It does not prove the host loaded the skill; record activation evidence separately when the host exposes it.
- Scenarios that need a live account are marked in their setup note and are optional.
- This is a package-specific harness, not an official Agent Skills certification.
