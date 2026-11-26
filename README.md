# Programming Language Lineage: version 1 (pre-review, 6 October 2026)

An interactive lineage map of 82 programming languages and 129 influence links. As a data scientist, I made it to understand the programming language landscape, its history and above all its lineage: which language influenced which, directly or indirectly.

I built the map with Claude Opus 5.5 in Cowork. I described each feature in a series of prompts and Claude wrote the code. The order was: the basic lineage graph with each language's ancestors and successors; the country where each language was developed and its designers' countries of birth; its health today (thriving, alive, dying or dead); and its outlook to 2046 (bullish, steady or bearish).

This is the frozen first version, as it stood before I sent it for AI review by ChatGPT 6.1 Sol and Gemini 3.1 Pro. The current version is on the `main` branch.

## Files

| File | What it is |
|---|---|
| `site/index.html` | Stand-alone copy of the page. Open it in any browser; it works offline except for the Google web fonts. |
| `docs/method.md` | Method note: goal, how links are chosen, health and 2046 outlook categories, graph analysis, and the alphabetical table of every language with its influences. |
| `source/build.py` | Generator. Holds all data (languages, positions, links, flags, inventors, organisations, health and outlook, famous software) and draws the SVG. |
| `source/desc.py` | The card paragraph for each language (origin, strengths, weaknesses, main uses). |
| `source/sw.py` | Famous software per language (name plus one-line description). Already merged into `build.py`; kept for reference. |
| `source/template.html` | Page layout, styles and all interactive behaviour (filters, depth controls, card panel, colours). |
| `source/artifact-page-body.html` | Exact output of `build.py` (the page without a document skeleton). |

## How to rebuild

Requirements: Python 3 with networkx (only for the graph-analysis numbers), Node.js/npm.

```bash
cd source
npm pack flag-icons@7 && tar xzf flag-icons-*.tgz            # creates ./package (country flags)
npm pack simple-icons && mkdir si && tar xzf simple-icons-*.tgz -C si   # creates ./si/package (logos)
python3 build.py        # writes language-lineage.html
```

`language-lineage.html` is the page body. Wrap it in `<!doctype html><html><head><meta charset="utf-8"></head><body>…</body></html>` to view it locally.

### Where to edit what

- **Add or move a language:** the `NODES` list in `build.py` (id, label, year, vertical position, family, short info). Then add entries in `FLAGS`, `STATUS`, `INVENTORS`, `ORG`, `DESC` (desc.py) and optionally `SOFTWARE` and `LOGO_SLUG`.
- **Add, remove or relabel a link:** the `EDGES` list in `build.py`: `(from_id, to_id, "label", "s" or "d")`, where `s` = solid and `d` = dotted.
- **Change a health or outlook rating:** `STATUS` in `build.py`: `(health, outlook or None, one-line reason)`.
- **Your languages (thick outline):** the `YOURS` set in `build.py`.

The build script prints `NODE OVERLAP`, `EDGE HITS NODE` and `LABEL CLASH` warnings to help with layout. Edge curves are chosen automatically to avoid nodes.

## Credits and licences

- Flags: flag-icons (MIT). Logos: Simple Icons (CC0 icon data; the marks belong to their owners). Fonts: IBM Plex (SIL Open Font License).
- Related work: Éric Lévénez's *Computer Languages History* chart; the O'Reilly *History of Programming Languages* poster (2004); Ramiro Gómez's *Programming Languages Influence Network*; Peter Gleeson's Wikipedia-based influence graph (freeCodeCamp, 2017); HOPL (hopl.info).
