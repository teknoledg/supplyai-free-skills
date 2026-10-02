# Quality Rubric

Score each dimension 0 (missing or contradictory), 1 (partial), or 2 (clear and useful):

1. Names: enter and lift are both named.
2. Duration: durations are stated in the summary and reflected in CSS.
3. Reduced motion: a `@media (prefers-reduced-motion: reduce)` block sets every added duration to 0.
4. Path: motion without that block fails — the agent stops instead of shipping.
5. Still: README-still elements (for example `.site-header`) have no added animation or transition; header-only stylesheets stay unchanged.
6. Stop: a non-zero reduced-motion duration, or a user request to skip reduced motion, stops the job.

Target at least 10/12, with no zero. Any fabricated evidence, printed secret, or violation of an explicit stop condition fails regardless of score. This is a package-specific evaluation rubric, not an industry certification.
