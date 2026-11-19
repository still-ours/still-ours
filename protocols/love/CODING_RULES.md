# Chapter One: Love — Coding Rules (frozen before full viewing)

Frozen: 2026-11-09 (America/New_York), before any coder viewed the full set of 270 runs.
Prior exposure: only run 1 of each machine × each of the six prompts (54 of 270) had been viewed, as a contact sheet.
Decided by the artist (Haotian Liu); written down by Claude.

## Unit
One run = one painting (painting.png) + its title + its artist statement, as returned by the model.
Runs with no rendered painting (render_failed / truncated without image) are coded from title and statement only, and marked `evidence = text_only`. If there is no title and no statement either, code `unreadable`.

## Question A — Main kind of love (choose exactly one)
1. `romantic` — lovers, partners, couples, romantic longing (includes unrequited love, secret crushes, missing an ex).
2. `family` — parent/child, siblings, grandparents, family.
3. `friendship` — friends, companions explicitly framed as friends.
4. `self` — love of oneself as the main subject.
5. `universal` — love for people at large, a community, a country, humanity, a thing, a place, a practice.
6. `cosmic_divine` — love toward or from God, the universe, nature, the cosmos.
7. `unclear` — the painting is abstract and neither title nor statement says who loves whom.

## Question B — Two yes/no flags (independent of A)
- `self_love` — yes if self-love / self-acceptance / loving oneself appears anywhere (painting, title or statement), even if A is not `self`.
- `beyond_partner` — yes ONLY if the work explicitly shows love for someone outside an existing fixed partnership: a third person, an affair, extramarital love, a love triangle, someone with a partner whose heart belongs to another. Unrequited love, secret crushes and missing an ex do NOT count (they are `romantic`). Never inferred; must be explicit.

## Evidence order
Painting first. If the painting alone does not decide, use the title, then the statement. Record which evidence decided: `painting`, `title`, `statement`, or `text_only`.
Abstract shapes (two lights, two blobs) do not count as two people unless the title or statement names them as lovers, family, etc. If the statement says "two" without saying what relationship, code `unclear`.

## Blind procedure
Runs are shuffled with a fixed seed and given anonymous IDs (L001–L270). Coders see only the image, title and statement — not the machine, language-prompt label, or run number. Titles/statements in Chinese or French are shown as-is.
Two independent coders apply these rules separately. Disagreements are listed for the artist, whose decision is final. Once decided, codes are not changed.
