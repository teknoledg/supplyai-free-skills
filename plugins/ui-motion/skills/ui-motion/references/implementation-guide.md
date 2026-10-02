# Implementation Guide

Use this when dropping motion into a real project. The starter file lives at [ui-motion-starter.css](../assets/ui-motion-starter.css).

## Discover targets

1. Read the project README for still elements. Common rule: the site header must never animate.
2. Find the page wrapper — usually `main`, `[role="main"]`, or a layout route outlet.
3. Find card or tile selectors — usually `.card`, `[data-card]`, or a component class from the design system.

## Where to write CSS

| Motion | Typical selector | Typical file |
| --- | --- | --- |
| Page enter | `main` (or project wrapper) | New `src/styles/motion.css`, or an existing component sheet that already styles the wrapper |
| Card lift | `.card` (or project card class) | The stylesheet that already defines the card component |

## Files to leave alone

Do not edit stylesheets whose sole job is still layout chrome when the README forbids header motion — for example a header stylesheet that only contains `.site-header`. Do not add `animation` or `transition` to `.site-header`, `header`, nav bars, or other still selectors.

If a stylesheet mixes still chrome and animated content, add motion only to the animated selectors inside that file; never to the still selectors.

## Reduced motion block

Every implementation must end with a block like:

```css
@media (prefers-reduced-motion: reduce) {
  /* every selector you animated or transitioned above */
  /* set animation: none and/or transition-duration: 0ms */
}
```

Under reduced motion, no added motion may keep a non-zero duration.

## Durations

Keep enter around 150–250ms and lift around 120–180ms. Use project motion tokens when they exist; otherwise pick one short value and state it in the summary.

## HTML changes

Optional. Prefer selector-based CSS (`main`, `.card`) when markup already matches. Add utility classes from the starter only when the project uses that pattern.

## Stop conditions

Stop without shipping CSS when:

- The user asks to skip or ignore reduced motion.
- You cannot add a `prefers-reduced-motion: reduce` override for every animation and transition you introduce.
- The only available target for enter or lift is a still element the README marks as non-animated.
