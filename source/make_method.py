"""Generates the method note (../docs/method.md) from nodes.py, edges.py and sources.json,
so the text, the page and the data cannot drift apart."""
import os, json
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "nodes.py"), encoding="utf-8").read())
exec(open(os.path.join(HERE, "edges.py"), encoding="utf-8").read())
SRC = json.load(open(os.path.join(HERE, "sources.json"), encoding="utf-8"))

L = {n[0]: n[1] for n in NODES}; Y = {n[0]: n[2] for n in NODES}; FAM = dict(FAMILIES); NF = {n[0]: n[4] for n in NODES}
def esc(s): return str(s).replace("|", "\\|")
LINE = {"s": "solid", "d": "dotted"}
HL = {"thriving": "🔥 Thriving", "alive": "🌿 Alive", "fading": "🪫 Fading", "dead": "💀 Dead"}
OL = {"bull": "🐂 Bullish", "steady": "⚓ Steady", "bear": "🐻 Bearish", None: "—"}
st = Counter(s["st"] for s in STATUS.values()); ol = Counter(s["ol"] for s in STATUS.values() if s["ol"])
conf = Counter(s["conf"] for s in STATUS.values() if s["ol"]); ai = sum(1 for s in STATUS.values() if s["ai"])
ln = Counter(e[3] for e in EDGES); kd = Counter(e[4] for e in EDGES)
ver = Counter(SRC[f"{e[0]}>{e[1]}"]["verdict"] for e in EDGES); typ = Counter(SRC[f"{e[0]}>{e[1]}"]["type"] for e in EDGES)
late = [e for e in EDGES if e[5]]
_v2 = {}
exec(open(os.path.join(HERE, "edges_v2.py"), encoding="utf-8").read(), _v2)
V2E = _v2["EDGES"]
V2S = {(e[0], e[1]): e[3] for e in V2E}; V3S = {(e[0], e[1]): e[3] for e in EDGES}
KEPT = [k for k in V2S if k in V3S]; ADDED = [k for k in V3S if k not in V2S]; GONE = [k for k in V2S if k not in V3S]
REROUTED = [k for k in GONE if k in (("pascal", "delphi"), ("basic", "vb"))]
_YEAR = {n[0]: n[2] for n in NODES}
BACK = [(e[0], e[1]) for e in EDGES if _YEAR[e[0]] > _YEAR[e[1]]]

o = []
w = o.append
w("# Programming Language Lineage: method and link list\n")
w(f"*Version 3, November 2026 · {len(NODES)} languages · {len(EDGES)} links ({ln['s']} solid, {ln['d']} dotted) · every cited source re-read against a written inclusion rule*\n")
w("## How this version was made\n")
w("Version 1 (October 2026: 82 languages, 129 links) was built with Claude (Anthropic) from the author's prompts. It was then reviewed adversarially over three rounds by two other AI models, "
  "Gemini 3.1 Pro and ChatGPT 6.1 Sol, acting as reviewers. The author decided each point, conceding or arguing on the merits, and afterwards revised it further. "
  "The result was version 2 (88 languages, 147 links). The file `data/edges-v1-to-v2.csv` lists every link that was added, removed, re-weighted or relabeled between version 1 and version 2.\n")
w("An AI audit of version 2 then found that the cited sources named more influences than were recorded, because links had been collected one quote at a time. "
  "For version 3 every cited source was re-read in full with the written inclusion rule below, so that each influence a source names is either recorded or rejected for a stated reason. "
  "Wikidata's *influenced by* property was used as a checklist to find further candidates, which became links only with a primary source and a quote. "
  "The work was done with Claude; the author decided the disputed cases. This note describes version 3. "
  "The file `data/edges-v2-to-v3.csv` lists every link of either version with what changed and why.\n")
w("## What changed in version 3\n")
w(f"- **Links: {len(V2E)} to {len(EDGES)}.** {len(KEPT)} links were kept, {len(ADDED)} added, {len(GONE) - len(REROUTED)} removed and {len(REROUTED)} rerouted through a new language. "
  f"Of the kept links, {sum(V2S[k] != V3S[k] for k in KEPT)} changed strength ({sum(V2S[k] == 's' and V3S[k] == 'd' for k in KEPT)} to weak, {sum(V2S[k] == 'd' and V3S[k] == 's' for k in KEPT)} to strong).")
w("- **A written inclusion rule** (see *What a link is*). Links were removed where the quoted source showed only a rival product, a rejected candidate, a denial, or that one language was written in the other.")
w("- **Links by another route are always weak.** A link that is not about design, syntax or the type system (a platform, a library, an implementation, a shared designer) is drawn dotted, without exception.")
w("- **Strength and evidence are separate.** A solid link can now be partly supported, and a dotted link fully supported; version 2 had tied the two together.")
w("- **Every later-version link has a year** (`since_year` in the data), so that paths can respect time order.")
w("- **Two columns were added** to `data/edges.csv`: `source_names_it` (whether the quoted sentence itself names the influence) and `audit_note` (what changed from version 2).")
w("- **Two languages were added**, Turbo Pascal and QuickBASIC, under a rule for intermediates (see *Which languages are included*). The direct links Pascal → Delphi and Dartmouth BASIC → Visual Basic now run through them.")
w("- **New links are not added when an intermediary already explains them.** For example, C → Java is not drawn, because the source says the C heritage came by way of C++.\n")
w("## What changed after AI review (from version 1 to version 2)\n")
w("- **Every link has a type and a source.** Links are classified by kind: design, syntax or type-system influence, or an influence by another route (platform, implementation, library, product, organizational). "
  "Each link cites a source, mostly primary (designers' papers, HOPL histories, official FAQs and documentation). Many labels were rewritten to say what was passed on.")
w("- **Strength was reconsidered** in both directions; for example COBOL → ABAP and Ruby → Elixir became weak (dotted).")
w("- **Later features are tagged.** A link that entered a later version of the receiving language carries that version (for example *ES2015*, *Python 2.2*, *PHP 7.1*), so it can be told apart from the language's original design.")
w("- **Evidence has three parts.** Each link records evidence for the *relationship*, evidence for the *feature* named in the label, and its *strength* (the line style).")
w("- **Nodes follow an explicit rule**, with the exceptions listed. Ten languages were added (CPL, ALGOL 68, ISWIM, B, Common Lisp, Cyclone, Newsqueak, J, K/q, VBA) and four removed (CoffeeScript, KQL, LookML, Mojo).")
w("- **Health is judged on three dimensions** and the 2046 outlook carries a confidence level, an explicit flag when it rests mainly on the AI assumption, and a condition that would change it.\n")

w("## Goal\n")
w("This project maps how programming languages descend from one another, so the history of programming can be read as a family tree and analyzed as a network. "
  "Each language is a node placed at the year it first appeared; each influence is a directed link from an earlier language to a later one, labeled with what was passed on. "
  "It is written for data scientists, so it deliberately includes statistics, data-processing and BI languages that general histories often skip. "
  "It is a curated, educational map, not an exhaustive genealogy or a validated forecasting model.\n")

w("## What a node is\n")
w("Every node is one of three kinds:\n")
w("- **Historical language**: the language as first designed, no longer in use (for example LISP 1958, ALGOL 60, Dartmouth BASIC, CPL, B).")
w("- **Continuing language**: a language and its standard revisions and maintained implementations (for example Fortran from FORTRAN I to Fortran 2023, Python 1 to 3).")
w("- **Deliberately aggregated node**: two or more closely related languages shown as one, because separating them would add nodes without adding lineage information.\n")
w("Where a node covers more than its name suggests, or deliberately less, the exception is listed here and on the language's card:\n")
w("| Language | Kind | This node covers |"); w("|---|---|---|")
for k, (kind, text) in SCOPE.items():
    w(f"| {L[k]} | {kind} | {esc(text)} |")
w("")
w("**Years** are the first public announcement or release (Rust 2010, Go 2009, Kotlin 2011, Dart 2011, Newsqueak 1989, K 1992). "
  "Internal-only dates are mentioned in the cards where relevant. For a language dated by its announcement, the *initial design* runs up to its 1.0 release (Rust 2015, Go 2012, Kotlin 2016, Dart 2013); features added after 1.0 are later features.\n")

w("## What a link is\n")
w("A link records a documented influence of one language on another and names what was passed on.\n")
w("**Inclusion rule.** A link A → B is recorded when a source documents that B took something from A:\n")
w("- the source says B borrowed, adopted, was based on, was inspired by or derived from A, or its designers say they wanted B to match A in a named respect (a link);")
w("- the source names A in a list of B's influences without naming a feature (a link, weak);")
w("- the influence came by another route: a platform, a major library, or an implementation language that shaped the new language (a link, always weak);")
w("- the two languages share a lead designer and no documented link already joins them (a link, weak, marked partly supported).\n")
w("Not links: resemblance stated by a third party, compatibility or interoperability alone, a precedent cited without saying it was the source, a candidate that was considered and rejected, a rival product, and a language that the other was merely written in. "
  "A new link is also left out when a language already between the two explains it. "
  f"The sources come from the designers' side: {typ['primary']} of {len(EDGES)} links cite a primary source, {typ['secondary']} a secondary one.\n")
w("Every link is drawn solid (strong) or dotted (weak). Its *kind* records how the influence traveled:\n")
w("| Route | Kind | Meaning | Links |"); w("|---|---|---|---|")
w(f"| design | design | ideas, semantics or structure taken into the language's design | {kd['design']} |")
w(f"| design | syntax | surface syntax or keywords | {kd['syntax']} |")
w(f"| design | type | type-system features | {kd['type']} |")
w(f"| other route | platform | designed to run on the other language's platform or runtime | {kd['platform']} |")
w(f"| other route | implementation | written in, or built as a front-end to, the other language | {kd['implementation']} |")
w(f"| other route | library | the influence arrived through a library (pandas, dplyr, magrittr) | {kd['library']} |")
w(f"| other route | product | built as a rival product | {kd['product']} |")
w(f"| other route | organizational | same team or designer, without a documented design transfer | {kd['organizational']} |")
w("")
w(f"- **Solid** ({ln['s']}): a main parent, or a defining feature that was borrowed. **Dotted** ({ln['d']}): a secondary or single-feature influence, an influence named without a feature, and every link by another route.")
w(f"- **Later-feature links** ({len(late)}): " + "; ".join(f"{L[e[0]]} → {L[e[1]]} (*{e[5]}*)" for e in late) + ".")
w(f"- **Evidence:** each link has a source and a verdict, and records separately the evidence for the *relationship* and for the *feature* in its label. {ver['supported']} are *supported* (the source documents the influence and what the label says) and {ver['partly']} are *partly* supported (the source supports the influence only indirectly: it is secondary, describes a likeness in the owner's own words, or names a close relative of the language). "
  f"Strength and evidence are recorded separately: {sum(1 for e in EDGES if e[3] == 's' and SRC[f'{e[0]}>{e[1]}']['verdict'] == 'partly')} solid links are partly supported. In {sum(1 for e in EDGES if SRC[f'{e[0]}>{e[1]}']['names_it'] == 'yes')} links the quoted sentence itself names the influence (`source_names_it` in the data). "
  "The full table below gives the source for every link; `data/edges.csv` adds the supporting quote.")
w("- **Absence of a link** means the influence was not documented in the sources checked, not that there was none. Candidates that were examined and rejected are listed, with the reason, in `source/research/v3_reconcile.csv`.")
w("- **Intermediaries named only in labels** (ALGOL 58, ALGOL W, PL/0, PAL, SASL, KRC, Strongtalk, Alef, Limbo, and the libraries pandas, dplyr and magrittr) are not nodes. This contracts some paths; see *Limitations*.\n")

w("## Which languages are included, and what the scope choices change\n")
w("The map covers the major general-purpose languages and their key ancestors, plus the languages that matter for data work: S, R, SAS, SPSS, Stata, MATLAB, Julia, J, K/q, SQL and its procedural and analytical relatives (T-SQL, PL/SQL, MDX, Cypher), and the Microsoft data languages (Excel formulas, VBA, DAX, Power Query M). "
  "A few languages are included for their uniqueness rather than their descendants (Forth, TeX).\n")
w("**Intermediates.** A dialect or product that sits between two languages on the map becomes its own node only if it meets three conditions: it was widely used in its own right, a cited source names it as the route between the two, and it extended the language instead of only compiling it. "
  "Turbo Pascal (between Pascal and Delphi) and QuickBASIC (between Dartmouth BASIC and Visual Basic) meet all three and were added in version 3. ALGOL W, PL/0, SASL, Alef and Limbo do not meet the first, and stay in the labels.\n")
w("Four languages that were in version 1 were removed as **scope and display-budget choices**, not because their history is unimportant:\n")
w("- **CoffeeScript**: its arrow functions and classes entered JavaScript in ES2015; this is now told in JavaScript's card. Effect: JavaScript loses a later-feature parent; Python and Ruby lose a descendant.")
w("- **KQL** and **LookML**: two domain-specific data languages with SQL as their only documented parent (LookML's link was a compile target). Effect: SQL's direct design influence falls by two.")
w("- **Mojo**: too young (2023) for its lineage role or outlook to be judged. Effect: Python and Rust each lose a descendant.\n")

w("## Health today\n")
w("Health is judged on three dimensions, and the badge is derived from them by a written rule:\n")
w("| Dimension | Values |"); w("|---|---|")
w("| Maintenance | active · maintenance-only · dormant |")
w("| New projects | broad (many domains) · niche (steady within its niche) · rare · none |")
w("| Installed base | critical · substantial · niche · historical |")
w("")
w("| Badge | Rule | Count |"); w("|---|---|---|")
w(f"| 🔥 Thriving | active maintenance, broad new projects, critical or substantial installed base | {st['thriving']} |")
w(f"| 🌿 Alive | new projects within its niche (or broad, with a smaller base) | {st['alive']} |")
w(f"| 🪫 Fading | maintained, but new projects are rare | {st['fading']} |")
w(f"| 💀 Dead | no new projects, or no maintained implementation | {st['dead']} |")
w("")
w("These are AI judgments with a stated reason, not measurements: Claude proposed each rating, the two AI reviewers challenged them, and the author decided the disputed ones. Each language's card and `data/nodes.csv` give the reason in one line. They were made in October 2026, informed by TIOBE (July–September 2026), GitHub Octoverse 2025, Stack Overflow surveys, release activity and the strength of each language's platforms. Forth's Fading badge is marked low confidence.\n")

w("## Outlook to 2046\n")
w("The outlook is given only to Alive and Thriving languages. It is a judgment about **share of newly written source code by 2046**, including code written with or by AI tools; it is not about deployed runtime code (so JavaScript can be Bearish while TypeScript, which compiles to it, is Bullish).\n")
w("It is conditional on one **assumption**: that AI systems keep writing a growing share of the world's code. Five factors were weighed, and they too are assumptions rather than established predictors: "
  "(1) whether a strict type system or compiler can check AI-written code; (2) how much public code exists for AI models to learn from; (3) the health of the platforms the language depends on; (4) how entrenched it is in its power centers; (5) whether a successor is replacing it.\n")
w("| Category | Meaning | Count |"); w("|---|---|---|")
w(f"| 🐂 Bullish | expected to gain share of newly written code | {ol['bull']} |")
w(f"| ⚓ Steady | expected to keep its power centers, even if it gains little new ground | {ol['steady']} |")
w(f"| 🐻 Bearish | expected to lose share of newly written code, though it may still run widely | {ol['bear']} |")
w("")
w(f"Every outlook has a **confidence** level (high {conf['high']}, medium {conf['medium']}, low {conf['low']}) and a **would change if** condition. "
  f"The {ai} outlooks that rest mainly on the AI assumption are marked low confidence and flagged as such; for Bash, the note separates commands run by agents from scripts that persist as code. "
  "On the map only the badge is shown; the confidence and the condition appear on hover and in the card.\n")

w("## Limitations\n")
w("- **Curation.** The graph records the influences that were selected and could be documented; most languages have more ancestors than are drawn, and the selection shapes every measure.")
w("- **Age bias.** Older languages have had more time to gather descendants, which favors them on any count of descendants.")
w("- **Represented intermediaries.** Which intermediaries are drawn as nodes shapes any network measure. CPL and B are drawn, so the explicit C line (ALGOL 60 → CPL → BCPL → B → C) gives them many descendants; Strongtalk, Alef, Limbo, SASL and KRC are named only in labels, so the paths through them are contracted. This is a property of the drawing, not a claim that CPL or B were historically central.")
w("- **Absence of evidence.** A missing link means the influence was not documented in the sources checked (several sources, such as the Rust Reference's list of influences, are explicitly non-exhaustive).")
w("- **Judgments.** Health and outlook are AI judgments, each with a stated reason but without a per-rating citation; the outlook depends on an assumption about AI that cannot yet be tested.")
w("- **Single links.** One link can carry a headline result. Every descendant of ALGOL 60 becomes a descendant of Fortran through Fortran → ALGOL 60. Version 3 draws it solid and supported, on Perlis's account that ALGOL 58 'was based on a model strongly derived from FORTRAN and its contemporaries'; the same account says FORTRAN itself was unacceptable as the common language, and the sentence concerns ALGOL 58, the precursor of ALGOL 60. Any count of descendants should be read with and without this link.")
w(f"- **Cycles.** A language keeps changing after its first release, and a younger language can influence a later version of an older one ({len(BACK)} links: " + "; ".join(f"{L[a]} → {L[b]}" for a, b in BACK) + "). With these links the graph has cycles. The links whose source language is not younger than the target form an acyclic graph, which is the one to use for path-based measures.")
w("- **Mixed routes.** Implementation, platform, library, product and organizational links count as influences alongside design links, so a path can mix routes: for example Fortran → S → R counts S's implementation on Fortran routines as influence. The *kind* of every link is in the data, so readers can filter.\n")

w("## Languages\n")
w("Alphabetical. *Parents* lists links into the language (dotted marked *weak*, later features in italics with their version, and the route when it is not design).\n")
w("| Language | Year | Family | Health (maintenance · new projects · installed base) | Outlook 2046 (confidence) | Parents |")
w("|---|---|---|---|---|---|")
for nid in sorted(L, key=lambda k: L[k].lower()):
    s = STATUS[nid]
    ins = [e for e in EDGES if e[1] == nid]
    core = [f"{L[e[0]]}" + (" *weak*" if e[3] == "d" else "") + (f" *({e[5]})*" if e[5] else "") + (f" [{e[4]}]" if e[4] in CONTEXT_KINDS else "") for e in ins]
    olc = f"{OL[s['ol']]} ({s['conf']}{', AI assumption' if s['ai'] else ''})" if s["ol"] else "—"
    w(f"| **{esc(L[nid])}** | {Y[nid]} | {FAM[NF[nid]]} | {HL[s['st']]} ({s['maint']} · {s['newproj']} · {s['base']}) | {olc} | {esc(', '.join(core)) or '—'} |")
w("")

w("## Links and sources\n")
w("Ordered by the receiving language's year. *Verdict*: S = supported, P = partly supported; 1 = primary, 2 = secondary source. *Relationship* and *feature* give the evidence for the influence and for the feature in the label; the *line* gives its strength.\n")
w("| # | From | To | What was passed on | Line | Kind | Later feature | Relationship | Feature | Verdict | Source |")
w("|---|---|---|---|---|---|---|---|---|---|---|")
rows = sorted(EDGES, key=lambda e: (Y[e[1]], L[e[1]].lower(), Y[e[0]]))
for i, e in enumerate(rows, 1):
    r = SRC[f"{e[0]}>{e[1]}"]
    ev = ("S" if r["verdict"] == "supported" else "P") + ("1" if r["type"] == "primary" else "2")
    w(f"| {i} | {esc(L[e[0]])} | {esc(L[e[1]])} | {esc(e[2])} | {LINE[e[3]]} | {e[4]} | {e[5] or ''} | {esc(r['rel'])} | {esc(r['feat'])} | {ev} | [{esc(r['citation'])}]({r['url']}) |")
w("")
w("## Using the map\n")
w("| Do this | What happens |"); w("|---|---|")
w("| Hover a language | Its ancestors and successors are highlighted and the rest of the map fades (when nothing is selected). |")
w("| Click a language | It is selected: the highlighting stays and its card opens on the right. Click it again to deselect. |")
w("| Ctrl-click a language (⌘-click on a Mac) | It is added to the selection, or removed if it was already selected. |")
w("| Click **None / Direct / 2nd degree / All** for Ancestors or Successors | Sets how far the highlighting follows the chain in that direction. |")
w("| Untick **weaker or partial influence** in the key | Hides the dotted links, and the highlighting then follows solid links only. Tick it to show them again. |")
w("| Hover or select a language | The labels of its dotted links appear; they are hidden otherwise to keep the map readable. |")
w("| Click a family, health or outlook category | Picks out the languages in that category. Choices in one row add up; choices in different rows narrow down. |")
w("| Hover a flag | Shows the designers' names. |")
w("| Hover a health or outlook badge | Shows the reasoning and, for outlooks, the confidence. |")
w("| Click a language name inside a card | Selects that language. |")
w("| Click **source** in a card | Opens the cited source for that link in a new tab. |")
w("| Click **Hide panel** | Folds the card away and keeps the selection; a **Show panel** button brings it back. |")
w("| Click **Close**, press Esc, or click an empty part of the chart | Clears the selected languages and closes the card. |")
w("| Click **Reset selection** | Clears the category filters. |")
w("")
w("## Related work and credits\n")
w("Éric Lévénez's *Computer Languages History* chart; the O'Reilly *History of Programming Languages* poster (2004); Ramiro Gómez's *Programming Languages Influence Network*; Peter Gleeson's Wikipedia-based influence graph (freeCodeCamp, 2017); the ACM HOPL conference papers. "
  "Flags: flag-icons (MIT). Logos: Simple Icons (CC0 icon data; marks belong to their owners). The map, the sourcing and this note were built with Claude (Anthropic) and reviewed by Gemini 3.1 Pro and ChatGPT 6.1 Sol; the author directed the work and decided each disputed point.\n")
OUT = os.path.join(HERE, "..", "docs", "method.md")
open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(o))
print("method note:", sum(len(x) for x in o), "chars;", len(rows), "links")
