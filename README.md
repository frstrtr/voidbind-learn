# P2Pool scientific basics (learn.voidbind.com)

Static pages on decentralized mining, P2Pool and c2pool, in English (the source
of truth), French, Russian, German and Chinese (Simplified). Served by GitHub
Pages at `learn.voidbind.com` (`CNAME`). There is no build step: the files in
this repository are what is served.

## Layout

```
index.html              language chooser (/), picks the stored or browser language
404.html
<lang>/index.html       home page of a language (en, fr, ru, de, zh)
<lang>/<slug>/index.html  one page; slugs are the same in every language
assets/                 site.css, lang.js (same-origin, no third-party code), images
i18n/glossary.tsv       terms per language
i18n/ui.json            interface strings per language
i18n/STATUS.md          translation status, written by tools/site.py check
tools/site.json         page list, languages, review state per language
tools/site.py           editing and checking helper (Python standard library)
FACTS.md                the source of every checked claim
```

## Page format

Each page has three regions maintained by `tools/site.py chrome`: head, top
(brand, language switcher, contents, notices) and foot. Do not edit inside
`<!-- chrome:… -->` markers by hand. The article sits in `<article>`:

- every top-level block starts at column 0 and has a stable `id`; nested lines
  are indented;
- ids never change once published; a new block gets a new id;
- no inline `style`, `<script>` or event handlers (the Content-Security-Policy
  blocks them).

## Translations and staleness

A translated block has the same `id` as its English block, plus
`data-src="<hash>"`: the first 12 hex digits of the sha256 of the English
block's normalized text and link targets.

```
python3 -I tools/site.py stamp ru luck          # after translating or updating ru/luck
python3 -I tools/site.py mark                   # after changing English text
python3 -I tools/site.py check                  # before every PR; must report 0 problems
```

When an English block changes, its hash changes. `mark` sets `data-stale="1"`
on every translated block whose `data-src` no longer matches, and the page then
shows a banner in its own language. `check` fails while a stale block is not
marked, or while a block is missing or extra. Its output goes into the PR body.

## Review

- English facts: checked against the c2pool source and release notes
  (`FACTS.md`), then by the fact checker before publishing.
- Each translation: made from the checked English text using
  `i18n/glossary.tsv`, then compared back against English by a second reader.
  Russian is reviewed by the operator. French, German and Chinese carry
  "machine-assisted translation" until a native reviewer is named
  (`review` in `tools/site.json`).

## Licence

Articles © 2026 technocore.one, all rights reserved, unless a page says
otherwise. The Work Receipts paper and the Ego handbook are © 2026 frstrtr
under the MIT License and are linked, not copied. Quotes from other sources are
attributed where they appear.
