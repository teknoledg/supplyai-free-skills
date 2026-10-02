# Output Structure

Use these headings in the delivery summary. Fill them with this task's content, not empty placeholders. CSS must be written to project files before summarizing.

## Enter
Name the enter motion, its target selector (for example `main`), its duration, and which file you changed.

## Lift
Name the lift motion, its target selector (for example `.card`), its duration, and which file you changed.

## Reduced motion
Confirm `@media (prefers-reduced-motion: reduce)` is present and that every added duration becomes `0ms` or `animation: none`.

## Still elements
List elements that stay still (for example `.site-header`) and confirm their stylesheets were not given animation or transition.
