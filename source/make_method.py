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

o = []
w = o.append
w("# Programming Language Lineage: method and link list\n")
w(f"*Version 2, November 2026 · {len(NODES)} languages · {len(EDGES)} links ({ln['s']} solid, {ln['d']} dotted) · revised after three rounds of AI review*\n")
w("## How this version was made\n")
w("Version 1 (October 2026: 82 languages, 129 links) was built with Claude (Anthropic) from the author's prompts. It was then reviewed adversarially over three rounds by two other AI models, "
  "Gemini 3.1 Pro and ChatGPT 6.1 Sol, acting as reviewers. The author decided each point, conceding or arguing on the merits, and afterwards revised it further. "
  "This note describes the result, version 2. The file `data/edges-v1-to-v2.csv` lists every link that was added, removed, re-weighted or relabeled between version 1 and version 2.\n")
w("## What changed after AI review (from version 1)\n")
w("- **Every link has a type and a source.** Links are classified by kind: design, syntax or type-system influence, or an influence by another route (platform, implementation, library, product, organizational). "
  f"Each link cites a source: {typ['primary']} of {len(EDGES)} are primary (designers' papers, HOPL histories, official FAQs and documentation), {typ['secondary']} secondary. Many labels were rewritten to say what was passed on.")
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
w(f"- **Solid** ({ln['s']}): a substantial influence. **Dotted** ({ln['d']}): a weaker, partial or resemblance-level influence.")
w(f"- **Later-feature links** ({len(late)}): " + "; ".join(f"{L[e[0]]} → {L[e[1]]} (*{e[5]}*)" for e in late) + ".")
w(f"- **Evidence:** each link has a source and a verdict, and records separately the evidence for the *relationship* and for the *feature* in its label. {ver['supported']} are *supported* (the source documents the influence and what the label says) and {ver['partly']} are *partly* supported (the source is secondary, shows resemblance or precedent only, or names the influence without the feature). "
  "**Every solid line is supported**: the relationship is documented, and the feature is either documented in the cited source or widely described (marked as such in the record). Partly supported links are drawn dotted. "
  "The full table below gives the source for every link; `data/edges.csv` adds the supporting quote.")
w("- **Absence of a link** means the influence was not documented in the sources checked, not that there was none. Several acknowledged inspirations without an identifiable transfer are named in the cards instead (for example Swift ← CLU, C#, Ruby; Kotlin ← JavaScript, Groovy).")
w("- **Intermediaries named only in labels** (ALGOL 58, ALGOL W, PAL, SASL, KRC, Strongtalk, Alef, Limbo, and the libraries pandas, dplyr and magrittr) are not nodes. This contracts some paths; see *Limitations*.\n")

w("## Which languages are included, and what the scope choices change\n")
w("The map covers the major general-purpose languages and their key ancestors, plus the languages that matter for data work: S, R, SAS, SPSS, Stata, MATLAB, Julia, J, K/q, SQL and its procedural and analytical relatives (T-SQL, PL/SQL, MDX, Cypher), and the Microsoft data languages (Excel formulas, VBA, DAX, Power Query M). "
  "A few languages are included for their uniqueness rather than their descendants (Forth, TeX).\n")
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
w("- **Single links.** One link can carry a headline result. Fortran → ALGOL 60 is dotted and only partly supported: FORTRAN was the precedent for the algebraic languages rather than a design source (the 1958 report does not name it, and the American proposal was deliberately not based on it). Because every descendant of ALGOL 60 becomes a descendant of Fortran through this link, any count of descendants should be read with and without it.")
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
