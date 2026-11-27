# Programming Language Lineage: method and link list

*Version 3, November 2026 · 90 languages · 218 links (104 solid, 114 dotted) · every cited source re-read against a written inclusion rule*

## How this version was made

Version 1 (October 2026: 82 languages, 129 links) was built with Claude (Anthropic) from the author's prompts. It was then reviewed adversarially over three rounds by two other AI models, Gemini 3.1 Pro and ChatGPT 6.1 Sol, acting as reviewers. The author decided each point, conceding or arguing on the merits, and afterwards revised it further. The result was version 2 (88 languages, 147 links). The file `data/edges-v1-to-v2.csv` lists every link that was added, removed, re-weighted or relabeled between version 1 and version 2.

An AI audit of version 2 then found that the cited sources named more influences than were recorded, because links had been collected one quote at a time. For version 3 every cited source was re-read in full with the written inclusion rule below, so that each influence a source names is either recorded or rejected for a stated reason. Wikidata's *influenced by* property was used as a checklist to find further candidates, which became links only with a primary source and a quote. The work was done with Claude; the author decided the disputed cases. This note describes version 3. The file `data/edges-v2-to-v3.csv` lists every link of either version with what changed and why.

## What changed in version 3

- **Links: 147 to 218.** 139 links were kept, 79 added, 6 removed and 2 rerouted through a new language. Of the kept links, 14 changed strength (12 to weak, 2 to strong).
- **A written inclusion rule** (see *What a link is*). Links were removed where the quoted source showed only a rival product, a rejected candidate, a denial, or that one language was written in the other.
- **Links by another route are always weak.** A link that is not about design, syntax or the type system (a platform, a library, an implementation, a shared designer) is drawn dotted, without exception.
- **Strength and evidence are separate.** A solid link can now be partly supported, and a dotted link fully supported; version 2 had tied the two together.
- **Every later-version link has a year** (`since_year` in the data), so that paths can respect time order.
- **Two columns were added** to `data/edges.csv`: `source_names_it` (whether the quoted sentence itself names the influence) and `audit_note` (what changed from version 2).
- **Two languages were added**, Turbo Pascal and QuickBASIC, under a rule for intermediates (see *Which languages are included*). The direct links Pascal → Delphi and Dartmouth BASIC → Visual Basic now run through them.
- **New links are not added when an intermediary already explains them.** For example, C → Java is not drawn, because the source says the C heritage came by way of C++.

## What changed after AI review (from version 1 to version 2)

- **Every link has a type and a source.** Links are classified by kind: design, syntax or type-system influence, or an influence by another route (platform, implementation, library, product, organizational). Each link cites a source, mostly primary (designers' papers, HOPL histories, official FAQs and documentation). Many labels were rewritten to say what was passed on.
- **Strength was reconsidered** in both directions; for example COBOL → ABAP and Ruby → Elixir became weak (dotted).
- **Later features are tagged.** A link that entered a later version of the receiving language carries that version (for example *ES2015*, *Python 2.2*, *PHP 7.1*), so it can be told apart from the language's original design.
- **Evidence has three parts.** Each link records evidence for the *relationship*, evidence for the *feature* named in the label, and its *strength* (the line style).
- **Nodes follow an explicit rule**, with the exceptions listed. Ten languages were added (CPL, ALGOL 68, ISWIM, B, Common Lisp, Cyclone, Newsqueak, J, K/q, VBA) and four removed (CoffeeScript, KQL, LookML, Mojo).
- **Health is judged on three dimensions** and the 2046 outlook carries a confidence level, an explicit flag when it rests mainly on the AI assumption, and a condition that would change it.

## Goal

This project maps how programming languages descend from one another, so the history of programming can be read as a family tree and analyzed as a network. Each language is a node placed at the year it first appeared; each influence is a directed link from an earlier language to a later one, labeled with what was passed on. It is written for data scientists, so it deliberately includes statistics, data-processing and BI languages that general histories often skip. It is a curated, educational map, not an exhaustive genealogy or a validated forecasting model.

## What a node is

Every node is one of three kinds:

- **Historical language**: the language as first designed, no longer in use (for example LISP 1958, ALGOL 60, Dartmouth BASIC, CPL, B).
- **Continuing language**: a language and its standard revisions and maintained implementations (for example Fortran from FORTRAN I to Fortran 2023, Python 1 to 3).
- **Deliberately aggregated node**: two or more closely related languages shown as one, because separating them would add nodes without adding lineage information.

Where a node covers more than its name suggests, or deliberately less, the exception is listed here and on the language's card:

| Language | Kind | This node covers |
|---|---|---|
| Smalltalk | continuing | Smalltalk-80 and its descendants Squeak and Pharo (Pharo calls itself 'Smalltalk-inspired'). |
| Scheme | continuing | The Scheme standards (R5RS–R7RS) and implementations such as Chez, Guile, Gambit and Chicken. Racket, which renamed itself from PLT Scheme in 2010, is not included. |
| ML | aggregated | LCF ML (1973) and Standard ML (1983/1990). |
| K / q | aggregated | K (1992) and q (2003), Whitney's closely related pair; q is a query layer written in K. |
| Visual Basic | aggregated | Visual Basic 1–6 and VB.NET; VBA is drawn separately. |
| Excel formulas | continuing | The Excel formula language from 1985 to today, including LAMBDA (2020). |
| Delphi | continuing | Delphi's Object Pascal, from Borland to Embarcadero. |
| Bourne sh | continuing | The Bourne shell and the POSIX sh standard based on it; Bash is drawn separately. |
| T-SQL | aggregated | Transact-SQL in Sybase and Microsoft SQL Server. |
| Mathematica | continuing | Mathematica's language, now called the Wolfram Language. |
| TeX | continuing | TeX and the macro packages built on it, such as LaTeX. |
| LISP | historical | McCarthy's LISP (1958) and LISP 1.5 only; later dialects are drawn separately. |
| ALGOL 60 | historical | ALGOL 60 (with ALGOL 58 as its precursor); ALGOL 68 is drawn separately. |
| Dartmouth BASIC | historical | Dartmouth BASIC and the classic line-numbered BASICs; QuickBASIC, Visual Basic and VBA are drawn separately. |
| Pascal | continuing | Standard Pascal and Free Pascal; Turbo Pascal and Delphi are drawn separately. |
| Fortran | continuing | FORTRAN I to modern Fortran (2023 standard). |
| Turbo Pascal | aggregated | Turbo Pascal 1 to 7 (1983–1992) and Borland Pascal; Delphi is drawn separately. |
| QuickBASIC | aggregated | QuickBASIC 1 to 4.5 (1985–1988) and its interpreter-only subset QBasic (1991). |

**Years** are the first public announcement or release (Rust 2010, Go 2009, Kotlin 2011, Dart 2011, Newsqueak 1989, K 1992). Internal-only dates are mentioned in the cards where relevant. For a language dated by its announcement, the *initial design* runs up to its 1.0 release (Rust 2015, Go 2012, Kotlin 2016, Dart 2013); features added after 1.0 are later features.

## What a link is

A link records a documented influence of one language on another and names what was passed on.

**Inclusion rule.** A link A → B is recorded when a source documents that B took something from A:

- the source says B borrowed, adopted, was based on, was inspired by or derived from A, or its designers say they wanted B to match A in a named respect (a link);
- the source names A in a list of B's influences without naming a feature (a link, weak);
- the influence came by another route: a platform, a major library, or an implementation language that shaped the new language (a link, always weak);
- the two languages share a lead designer and no documented link already joins them (a link, weak, marked partly supported).

Not links: resemblance stated by a third party, compatibility or interoperability alone, a precedent cited without saying it was the source, a candidate that was considered and rejected, a rival product, and a language that the other was merely written in. A new link is also left out when a language already between the two explains it. The sources come from the designers' side: 210 of 218 links cite a primary source, 8 a secondary one.

Every link is drawn solid (strong) or dotted (weak). Its *kind* records how the influence traveled:

| Route | Kind | Meaning | Links |
|---|---|---|---|
| design | design | ideas, semantics or structure taken into the language's design | 149 |
| design | syntax | surface syntax or keywords | 45 |
| design | type | type-system features | 12 |
| other route | platform | designed to run on the other language's platform or runtime | 1 |
| other route | implementation | written in, or built as a front-end to, the other language | 2 |
| other route | library | the influence arrived through a library (pandas, dplyr, magrittr) | 7 |
| other route | product | built as a rival product | 0 |
| other route | organizational | same team or designer, without a documented design transfer | 2 |

- **Solid** (104): a main parent, or a defining feature that was borrowed. **Dotted** (114): a secondary or single-feature influence, an influence named without a feature, and every link by another route.
- **Later-feature links** (32): Scheme → Lua (*Lua 3.1*); C → Stata (*Stata 9*); Ada → C++ (*C++ after 1985*); CLU → C++ (*C++ after 1985*); Rust → Swift (*Swift 5.9*); Python → Scala (*Scala 3*); F# → R (*R 4.1*); Haskell → Excel formulas (*LAMBDA 2020*); Haskell → Python (*Python 2.0*); SQL → Python (*pandas 2008*); R → Python (*pandas 2008*); Python → JavaScript (*ES2015*); C# → Dart (*Dart 1.9*); SQL → R (*dplyr 2014*); ML → C++ (*C++ after 1985*); Haskell → F# (*F# 2007*); Python → F# (*F# 2006*); Bourne sh → R (*magrittr 2014*); Swift → Rust (*Rust 0.12*); Common Lisp → S (*S 1991*); C++ → S (*S 1991*); Bourne sh → S (*S on UNIX*); Smalltalk → S (*S 1991*); Perl → Swift (*Swift 4*); F# → C# (*C# 5.0*); Haskell → C# (*C# 3.0*); Icon → C# (*C# 2.0*); Python → C# (*C# 4.0*); Perl → JavaScript (*JavaScript 1.2*); Java → Ada (*Ada 2005*); Haskell → Clojure (*Clojure 1.2*); C++ → Turbo Pascal (*Turbo Pascal 5.5*).
- **Evidence:** each link has a source and a verdict, and records separately the evidence for the *relationship* and for the *feature* in its label. 200 are *supported* (the source documents the influence and what the label says) and 18 are *partly* supported (the source supports the influence only indirectly: it is secondary, describes a likeness in the owner's own words, or names a close relative of the language). Strength and evidence are recorded separately: 4 solid links are partly supported. In 206 links the quoted sentence itself names the influence (`source_names_it` in the data). The full table below gives the source for every link; `data/edges.csv` adds the supporting quote.
- **Absence of a link** means the influence was not documented in the sources checked, not that there was none. Candidates that were examined and rejected are listed, with the reason, in `source/research/v3_reconcile.csv`.
- **Intermediaries named only in labels** (ALGOL 58, ALGOL W, PL/0, PAL, SASL, KRC, Strongtalk, Alef, Limbo, and the libraries pandas, dplyr and magrittr) are not nodes. This contracts some paths; see *Limitations*.

## Which languages are included, and what the scope choices change

The map covers the major general-purpose languages and their key ancestors, plus the languages that matter for data work: S, R, SAS, SPSS, Stata, MATLAB, Julia, J, K/q, SQL and its procedural and analytical relatives (T-SQL, PL/SQL, MDX, Cypher), and the Microsoft data languages (Excel formulas, VBA, DAX, Power Query M). A few languages are included for their uniqueness rather than their descendants (Forth, TeX).

**Intermediates.** A dialect or product that sits between two languages on the map becomes its own node only if it meets three conditions: it was widely used in its own right, a cited source names it as the route between the two, and it extended the language instead of only compiling it. Turbo Pascal (between Pascal and Delphi) and QuickBASIC (between Dartmouth BASIC and Visual Basic) meet all three and were added in version 3. ALGOL W, PL/0, SASL, Alef and Limbo do not meet the first, and stay in the labels.

Four languages that were in version 1 were removed as **scope and display-budget choices**, not because their history is unimportant:

- **CoffeeScript**: its arrow functions and classes entered JavaScript in ES2015; this is now told in JavaScript's card. Effect: JavaScript loses a later-feature parent; Python and Ruby lose a descendant.
- **KQL** and **LookML**: two domain-specific data languages with SQL as their only documented parent (LookML's link was a compile target). Effect: SQL's direct design influence falls by two.
- **Mojo**: too young (2023) for its lineage role or outlook to be judged. Effect: Python and Rust each lose a descendant.

## Health today

Health is judged on three dimensions, and the badge is derived from them by a written rule:

| Dimension | Values |
|---|---|
| Maintenance | active · maintenance-only · dormant |
| New projects | broad (many domains) · niche (steady within its niche) · rare · none |
| Installed base | critical · substantial · niche · historical |

| Badge | Rule | Count |
|---|---|---|
| 🔥 Thriving | active maintenance, broad new projects, critical or substantial installed base | 12 |
| 🌿 Alive | new projects within its niche (or broad, with a smaller base) | 44 |
| 🪫 Fading | maintained, but new projects are rare | 11 |
| 💀 Dead | no new projects, or no maintained implementation | 23 |

These are AI judgments with a stated reason, not measurements: Claude proposed each rating, the two AI reviewers challenged them, and the author decided the disputed ones. Each language's card and `data/nodes.csv` give the reason in one line. They were made in October 2026, informed by TIOBE (July–September 2026), GitHub Octoverse 2025, Stack Overflow surveys, release activity and the strength of each language's platforms. Forth's Fading badge is marked low confidence.

## Outlook to 2046

The outlook is given only to Alive and Thriving languages. It is a judgment about **share of newly written source code by 2046**, including code written with or by AI tools; it is not about deployed runtime code (so JavaScript can be Bearish while TypeScript, which compiles to it, is Bullish).

It is conditional on one **assumption**: that AI systems keep writing a growing share of the world's code. Five factors were weighed, and they too are assumptions rather than established predictors: (1) whether a strict type system or compiler can check AI-written code; (2) how much public code exists for AI models to learn from; (3) the health of the platforms the language depends on; (4) how entrenched it is in its power centers; (5) whether a successor is replacing it.

| Category | Meaning | Count |
|---|---|---|
| 🐂 Bullish | expected to gain share of newly written code | 10 |
| ⚓ Steady | expected to keep its power centers, even if it gains little new ground | 26 |
| 🐻 Bearish | expected to lose share of newly written code, though it may still run widely | 20 |

Every outlook has a **confidence** level (high 11, medium 33, low 12) and a **would change if** condition. The 11 outlooks that rest mainly on the AI assumption are marked low confidence and flagged as such; for Bash, the note separates commands run by agents from scripts that persist as code. On the map only the badge is shown; the confidence and the condition appear on hover and in the card.

## Limitations

- **Curation.** The graph records the influences that were selected and could be documented; most languages have more ancestors than are drawn, and the selection shapes every measure.
- **Age bias.** Older languages have had more time to gather descendants, which favors them on any count of descendants.
- **Represented intermediaries.** Which intermediaries are drawn as nodes shapes any network measure. CPL and B are drawn, so the explicit C line (ALGOL 60 → CPL → BCPL → B → C) gives them many descendants; Strongtalk, Alef, Limbo, SASL and KRC are named only in labels, so the paths through them are contracted. This is a property of the drawing, not a claim that CPL or B were historically central.
- **Absence of evidence.** A missing link means the influence was not documented in the sources checked (several sources, such as the Rust Reference's list of influences, are explicitly non-exhaustive).
- **Judgments.** Health and outlook are AI judgments, each with a stated reason but without a per-rating citation; the outlook depends on an assumption about AI that cannot yet be tested.
- **Single links.** One link can carry a headline result. Every descendant of ALGOL 60 becomes a descendant of Fortran through Fortran → ALGOL 60. Version 3 draws it solid and supported, on Perlis's account that ALGOL 58 'was based on a model strongly derived from FORTRAN and its contemporaries'; the same account says FORTRAN itself was unacceptable as the common language, and the sentence concerns ALGOL 58, the precursor of ALGOL 60. Any count of descendants should be read with and without this link.
- **Cycles.** A language keeps changing after its first release, and a younger language can influence a later version of an older one (10 links: F# → R; Haskell → Excel formulas; R → Python; Swift → Rust; Common Lisp → S; C++ → S; Bourne sh → S; F# → C#; Java → Ada; C++ → Turbo Pascal). With these links the graph has cycles. The links whose source language is not younger than the target form an acyclic graph, which is the one to use for path-based measures.
- **Mixed routes.** Implementation, platform, library, product and organizational links count as influences alongside design links, so a path can mix routes: for example Fortran → S → R counts S's implementation on Fortran routines as influence. The *kind* of every link is in the data, so readers can filter.

## Languages

Alphabetical. *Parents* lists links into the language (dotted marked *weak*, later features in italics with their version, and the route when it is not design).

| Language | Year | Family | Health (maintenance · new projects · installed base) | Outlook 2046 (confidence) | Parents |
|---|---|---|---|---|---|
| **ABAP** | 1983 | Data & BI | 🌿 Alive (active · niche · critical) | ⚓ Steady (high) | COBOL *weak* |
| **ABC** | 1987 | Scripting & web | 💀 Dead (dormant · none · historical) | — | — |
| **Ada** | 1980 | C & systems | 🌿 Alive (active · niche · substantial) | ⚓ Steady (medium) | Pascal, ALGOL 68 *weak*, CLU *weak*, Simula *weak*, Java *weak* *(Ada 2005)* |
| **ALGOL 60** | 1960 | C & systems | 💀 Dead (dormant · none · historical) | — | Fortran |
| **ALGOL 68** | 1968 | C & systems | 💀 Dead (active · none · historical) | — | ALGOL 60 |
| **APL** | 1966 | Arrays & statistics | 🌿 Alive (active · niche · niche) | ⚓ Steady (medium) | — |
| **AWK** | 1977 | Scripting & web | 🌿 Alive (active · niche · substantial) | ⚓ Steady (high) | C, SNOBOL *weak* |
| **B** | 1969 | C & systems | 💀 Dead (dormant · none · historical) | — | BCPL, Fortran *weak* |
| **Bash** | 1989 | Scripting & web | 🔥 Thriving (active · broad · critical) | 🐂 Bullish (low, AI assumption) | Bourne sh |
| **BCPL** | 1967 | C & systems | 💀 Dead (active · none · historical) | — | CPL |
| **Bourne sh** | 1979 | Scripting & web | 🌿 Alive (active · niche · critical) | ⚓ Steady (high) | ALGOL 68 |
| **C** | 1972 | C & systems | 🔥 Thriving (active · broad · critical) | ⚓ Steady (high) | B, ALGOL 68 *weak*, PL/I *weak* |
| **C#** | 2000 | JVM & .NET | 🔥 Thriving (active · broad · critical) | 🐂 Bullish (medium) | Java, C++, Delphi, F# *weak* *(C# 5.0)*, Haskell *weak* *(C# 3.0)*, Icon *weak* *(C# 2.0)*, Python *weak* *(C# 4.0)* |
| **C++** | 1985 | C & systems | 🔥 Thriving (active · broad · critical) | ⚓ Steady (high) | ALGOL 68, C, Simula, Ada *weak* *(C++ after 1985)*, CLU *weak* *(C++ after 1985)*, BCPL *weak*, ML *weak* *(C++ after 1985)* |
| **Clojure** | 2007 | Lisp | 🌿 Alive (active · niche · niche) | 🐻 Bearish (low, AI assumption) | LISP, Java *weak* [platform], Common Lisp *weak*, ML *weak*, Haskell *weak* *(Clojure 1.2)* |
| **CLU** | 1974 | Other lineages | 💀 Dead (dormant · none · historical) | — | LISP, ALGOL 60 *weak* |
| **COBOL** | 1959 | Other lineages | 🪫 Fading (active · rare · critical) | — | — |
| **Common Lisp** | 1984 | Lisp | 🌿 Alive (active · niche · niche) | 🐻 Bearish (low, AI assumption) | LISP, Scheme |
| **CPL** | 1963 | C & systems | 💀 Dead (dormant · none · historical) | — | ALGOL 60 |
| **Cyclone** | 2002 | C & systems | 💀 Dead (dormant · none · historical) | — | C, ML *weak* |
| **Cypher** | 2011 | Data & BI | 🌿 Alive (active · niche · niche) | ⚓ Steady (medium) | SQL, Python *weak* |
| **Dart** | 2011 | Scripting & web | 🌿 Alive (active · niche · niche) | 🐻 Bearish (medium) | JavaScript *weak*, Java, Smalltalk, C# *weak* *(Dart 1.9)*, Erlang *weak* |
| **Dartmouth BASIC** | 1964 | Teaching & visual | 💀 Dead (dormant · none · historical) | — | Fortran, ALGOL 60 *weak* |
| **DAX** | 2009 | Data & BI | 🌿 Alive (active · niche · substantial) | ⚓ Steady (medium) | Excel formulas |
| **Delphi** | 1995 | Teaching & visual | 🌿 Alive (active · niche · substantial) | 🐻 Bearish (medium) | Turbo Pascal |
| **Eiffel** | 1986 | Other lineages | 🪫 Fading (active · rare · niche) | — | Simula |
| **Elixir** | 2012 | Other lineages | 🌿 Alive (active · niche · niche) | 🐻 Bearish (low, AI assumption) | F# *weak*, Ruby *weak*, Erlang, Clojure *weak* |
| **Erlang** | 1986 | Other lineages | 🌿 Alive (active · niche · substantial) | ⚓ Steady (medium) | Prolog |
| **Excel formulas** | 1985 | Data & BI | 🔥 Thriving (active · broad · critical) | 🐂 Bullish (low, AI assumption) | Haskell *weak* *(LAMBDA 2020)* |
| **F#** | 2005 | ML & Haskell | 🌿 Alive (active · niche · niche) | 🐻 Bearish (medium) | OCaml, C# *weak*, Haskell *weak* *(F# 2007)*, Python *weak* *(F# 2006)* |
| **Forth** | 1970 | Other lineages | 🪫 Fading (active · rare · niche) | — | — |
| **Fortran** | 1957 | Arrays & statistics | 🌿 Alive (active · niche · critical) | ⚓ Steady (high) | — |
| **Go** | 2009 | C & systems | 🔥 Thriving (active · broad · substantial) | 🐂 Bullish (medium) | C, Oberon, Newsqueak, APL *weak*, BCPL *weak*, Smalltalk *weak*, B *weak* [organizational] |
| **Hack** | 2014 | Scripting & web | 🌿 Alive (active · niche · substantial) | 🐻 Bearish (medium) | PHP |
| **Haskell** | 1990 | ML & Haskell | 🌿 Alive (active · niche · niche) | 🐻 Bearish (low, AI assumption) | ML, Miranda |
| **Icon** | 1977 | Other lineages | 💀 Dead (dormant · none · historical) | — | SNOBOL |
| **ISWIM** | 1966 | ML & Haskell | 💀 Dead (dormant · none · historical) | — | LISP |
| **J** | 1990 | Arrays & statistics | 🌿 Alive (active · niche · niche) | 🐻 Bearish (medium) | APL |
| **Java** | 1995 | JVM & .NET | 🔥 Thriving (active · broad · critical) | ⚓ Steady (high) | C++, Smalltalk *weak*, Eiffel *weak*, Objective-C |
| **JavaScript** | 1995 | Scripting & web | 🔥 Thriving (active · broad · critical) | 🐻 Bearish (medium) | Scheme, Self, Java *weak*, Python *weak* *(ES2015)*, AWK *weak*, Perl *weak* *(JavaScript 1.2)* |
| **Julia** | 2012 | Arrays & statistics | 🌿 Alive (active · niche · niche) | ⚓ Steady (low, AI assumption) | Common Lisp *weak*, MATLAB, Python *weak*, R *weak*, C *weak*, LISP, Perl *weak*, Lua *weak*, Ruby *weak*, Bourne sh *weak* |
| **K / q** | 1992 | Arrays & statistics | 🌿 Alive (active · niche · substantial) | ⚓ Steady (medium) | APL |
| **Kotlin** | 2011 | JVM & .NET | 🌿 Alive (active · niche · substantial) | 🐂 Bullish (medium) | Java, Scala *weak*, C# *weak*, JavaScript *weak* |
| **LISP** | 1958 | Lisp | 💀 Dead (dormant · none · historical) | — | — |
| **Logo** | 1967 | Teaching & visual | 💀 Dead (active · none · historical) | — | LISP |
| **Lua** | 1993 | Scripting & web | 🌿 Alive (active · niche · substantial) | ⚓ Steady (medium) | Scheme *(Lua 3.1)*, CLU *weak*, AWK, C++ *weak*, Modula-2 *weak* |
| **Mathematica** | 1988 | Arrays & statistics | 🌿 Alive (active · niche · substantial) | ⚓ Steady (medium) | LISP *weak*, APL *weak* |
| **MATLAB** | 1984 | Arrays & statistics | 🌿 Alive (active · niche · substantial) | 🐻 Bearish (medium) | Fortran *weak* [library], Pascal |
| **MDX** | 1997 | Data & BI | 🪫 Fading (maintenance-only · rare · substantial) | — | SQL |
| **Miranda** | 1985 | ML & Haskell | 💀 Dead (dormant · none · historical) | — | ISWIM, ML |
| **ML** | 1973 | ML & Haskell | 🪫 Fading (active · rare · niche) | — | LISP *weak*, ISWIM |
| **Modula-2** | 1978 | C & systems | 🪫 Fading (active · rare · niche) | — | Pascal |
| **Modula-3** | 1989 | C & systems | 💀 Dead (dormant · none · historical) | — | Modula-2 |
| **Newsqueak** | 1989 | Other lineages | 💀 Dead (dormant · none · historical) | — | — |
| **Oberon** | 1987 | C & systems | 💀 Dead (dormant · none · historical) | — | Modula-2 |
| **Objective-C** | 1984 | C & systems | 🪫 Fading (maintenance-only · rare · substantial) | — | C, Smalltalk |
| **OCaml** | 1996 | ML & Haskell | 🌿 Alive (active · niche · niche) | 🐻 Bearish (medium) | ML |
| **Pascal** | 1970 | C & systems | 🪫 Fading (active · rare · niche) | — | ALGOL 60, COBOL *weak* |
| **Perl** | 1987 | Scripting & web | 🪫 Fading (active · rare · substantial) | — | Bourne sh, AWK, C, Pascal *weak* |
| **PHP** | 1995 | Scripting & web | 🌿 Alive (active · niche · critical) | ⚓ Steady (medium) | C, Perl, Java *weak* |
| **PL/I** | 1964 | C & systems | 🪫 Fading (active · rare · substantial) | — | Fortran, COBOL, ALGOL 60 |
| **PL/SQL** | 1988 | Data & BI | 🌿 Alive (active · niche · critical) | ⚓ Steady (high) | Ada, SQL |
| **Power Query M** | 2013 | Data & BI | 🌿 Alive (active · niche · substantial) | ⚓ Steady (medium) | F# *weak* |
| **PowerShell** | 2006 | Scripting & web | 🌿 Alive (active · niche · substantial) | ⚓ Steady (high) | Bourne sh, C# *weak* |
| **Prolog** | 1972 | Other lineages | 🌿 Alive (active · niche · niche) | ⚓ Steady (low, AI assumption) | — |
| **Python** | 1991 | Scripting & web | 🔥 Thriving (active · broad · critical) | 🐂 Bullish (medium) | Icon *weak*, ABC, Modula-3, C++ *weak*, C, Haskell *weak* *(Python 2.0)*, SQL *weak* *(pandas 2008)* [library], R *weak* *(pandas 2008)* [library], ALGOL 68 *weak*, Bourne sh *weak* |
| **QuickBASIC** | 1985 | Teaching & visual | 💀 Dead (dormant · none · historical) | — | Dartmouth BASIC |
| **R** | 1993 | Arrays & statistics | 🌿 Alive (active · niche · substantial) | ⚓ Steady (medium) | Scheme, S, F# *weak* *(R 4.1)* [library], SQL *weak* *(dplyr 2014)* [library], Bourne sh *weak* *(magrittr 2014)* [library] |
| **Ruby** | 1995 | Scripting & web | 🌿 Alive (active · niche · substantial) | 🐻 Bearish (medium) | Smalltalk, CLU *weak*, Eiffel *weak*, Perl, LISP *weak* |
| **Rust** | 2010 | C & systems | 🔥 Thriving (active · broad · substantial) | 🐂 Bullish (medium) | Cyclone, C++, OCaml, Haskell, C# *weak*, Erlang *weak*, Newsqueak *weak*, Ruby *weak*, Scheme *weak*, Swift *weak* *(Rust 0.12)* |
| **S** | 1976 | Arrays & statistics | 💀 Dead (dormant · none · historical) | — | APL, Fortran *weak*, ALGOL 60 *weak*, C *weak*, Common Lisp *weak* *(S 1991)*, C++ *weak* *(S 1991)*, LISP, Bourne sh *weak* *(S on UNIX)*, Smalltalk *weak* *(S 1991)* |
| **SAS** | 1972 | Arrays & statistics | 🌿 Alive (active · niche · substantial) | 🐻 Bearish (medium) | — |
| **Scala** | 2004 | JVM & .NET | 🌿 Alive (active · niche · substantial) | 🐻 Bearish (medium) | Java, ML *weak*, Haskell, Python *weak* *(Scala 3)*, C# *weak*, Eiffel *weak*, Erlang *weak* [library], Smalltalk *weak* |
| **Scheme** | 1975 | Lisp | 🌿 Alive (active · niche · niche) | 🐻 Bearish (low, AI assumption) | LISP, ALGOL 60 |
| **Scratch** | 2007 | Teaching & visual | 🌿 Alive (active · niche · substantial) | ⚓ Steady (medium) | Logo |
| **Self** | 1987 | Other lineages | 💀 Dead (active · none · historical) | — | Smalltalk, APL *weak* |
| **Simula** | 1967 | Other lineages | 💀 Dead (dormant · none · historical) | — | ALGOL 60 |
| **Smalltalk** | 1972 | Other lineages | 🌿 Alive (active · niche · niche) | 🐻 Bearish (low, AI assumption) | LISP, Simula, Logo *weak* |
| **SNOBOL** | 1962 | Other lineages | 💀 Dead (active · none · historical) | — | — |
| **SPSS** | 1968 | Arrays & statistics | 🌿 Alive (active · niche · substantial) | 🐻 Bearish (medium) | Fortran *weak* [implementation] |
| **SQL** | 1974 | Data & BI | 🔥 Thriving (active · broad · critical) | 🐂 Bullish (low, AI assumption) | — |
| **Stata** | 1985 | Arrays & statistics | 🌿 Alive (active · niche · substantial) | 🐻 Bearish (medium) | C *weak* *(Stata 9)* |
| **Swift** | 2014 | C & systems | 🌿 Alive (active · niche · substantial) | ⚓ Steady (medium) | Objective-C, Rust *weak* *(Swift 5.9)*, Python *weak*, Haskell *weak*, Perl *weak* *(Swift 4)*, Ruby *weak*, C# *weak*, CLU *weak* |
| **T-SQL** | 1987 | Data & BI | 🌿 Alive (active · niche · critical) | ⚓ Steady (high) | SQL |
| **TeX** | 1978 | Other lineages | 🌿 Alive (active · niche · critical) | ⚓ Steady (high) | Pascal *weak* [implementation] |
| **Turbo Pascal** | 1983 | C & systems | 💀 Dead (dormant · none · historical) | — | Pascal, C++ *weak* *(Turbo Pascal 5.5)* |
| **TypeScript** | 2012 | Scripting & web | 🔥 Thriving (active · broad · critical) | 🐂 Bullish (medium) | JavaScript, C# *weak* [organizational] |
| **VBA** | 1993 | Teaching & visual | 🌿 Alive (maintenance-only · niche · critical) | 🐻 Bearish (medium) | Visual Basic |
| **Visual Basic** | 1991 | Teaching & visual | 🪫 Fading (maintenance-only · rare · substantial) | — | QuickBASIC |
| **Zig** | 2016 | C & systems | 🌿 Alive (active · niche · niche) | 🐂 Bullish (low) | C |

## Links and sources

Ordered by the receiving language's year. *Verdict*: S = supported, P = partly supported; 1 = primary, 2 = secondary source. *Relationship* and *feature* give the evidence for the influence and for the feature in the label; the *line* gives its strength.

| # | From | To | What was passed on | Line | Kind | Later feature | Relationship | Feature | Verdict | Source |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fortran | ALGOL 60 | ALGOL 58 was based on a model derived from FORTRAN | solid | design |  | documented | documented | S1 | [Perlis, A. J. (1978/1981). The American Side of the Development of ALGOL. History of Programming Languages (HOPL I), ACM, pp. 75-91.](https://dl.acm.org/doi/10.1145/800025.1198352) |
| 2 | ALGOL 60 | CPL | ALGOL 60 as its base | solid | design |  | documented | documented | S1 | [Richards, M. (2013). How BCPL evolved from CPL. The Computer Journal (author's PDF).](https://www.cl.cam.ac.uk/~mr10/cpl2bcpl.pdf) |
| 3 | Fortran | Dartmouth BASIC | keywords, operators from FORTRAN II | solid | design |  | documented | documented | S2 | [Wikipedia (2026). Dartmouth BASIC (citing Kurtz, T. E. (1981). BASIC. In History of Programming Languages, Academic Press, p. 523).](https://en.wikipedia.org/wiki/Dartmouth_BASIC) |
| 4 | ALGOL 60 | Dartmouth BASIC | FOR…TO…STEP loops | dotted | syntax |  | documented | documented | S2 | [Wikipedia (2026). Dartmouth BASIC (citing Kurtz, T. E. (1981). BASIC. In History of Programming Languages, Academic Press, p. 523).](https://en.wikipedia.org/wiki/Dartmouth_BASIC) |
| 5 | Fortran | PL/I | the scientific half | solid | design |  | documented | documented | S2 | [Meil, D. (2023). Lessons from PL/I: A Most Ambitious Programming Language. BLOG@CACM, Communications of the ACM.](https://cacm.acm.org/blogcacm/lessons-from-pl-i-a-most-ambitious-programming-language/) |
| 6 | COBOL | PL/I | the business half | solid | design |  | documented | documented | S2 | [Meil, D. (2023). Lessons from PL/I: A Most Ambitious Programming Language. BLOG@CACM, Communications of the ACM.](https://cacm.acm.org/blogcacm/lessons-from-pl-i-a-most-ambitious-programming-language/) |
| 7 | ALGOL 60 | PL/I | one of the three languages PL/I set out to combine | solid | design |  | documented | documented | S2 | [Meil, D. (2023). Lessons from PL/I: A Most Ambitious Programming Language. BLOG@CACM, Communications of the ACM.](https://cacm.acm.org/blogcacm/lessons-from-pl-i-a-most-ambitious-programming-language/) |
| 8 | LISP | ISWIM | functional core, without lists and brackets | solid | design |  | documented | documented | S1 | [Landin, P. J. (1966). The Next 700 Programming Languages. Communications of the ACM 9(3), 157-165.](https://www.cs.cmu.edu/~crary/819-f09/Landin66.pdf) |
| 9 | CPL | BCPL | CPL minus the hard parts | solid | design |  | documented | documented | S1 | [Richards, M. (c. 2012). How BCPL evolved from CPL. Author's version, University of Cambridge Computer Laboratory.](https://www.cl.cam.ac.uk/~mr10/cpl2bcpl.pdf) |
| 10 | LISP | Logo | Lisp without parentheses | solid | design |  | documented | documented | S1 | [Solomon, C., Harvey, B., Kahn, K., Lieberman, H., Miller, M. L., Minsky, M., Papert, A. & Silverman, B. (2020). History of Logo. Proceedings of the ACM on Programming Languages 4(HOPL), Article 79.](https://people.eecs.berkeley.edu/~bh/HOPL.pdf) |
| 11 | ALGOL 60 | Simula | extension of ALGOL 60 | solid | design |  | documented | documented | S1 | [Nygaard, K. & Dahl, O.-J. (1978). The Development of the SIMULA Languages. History of Programming Languages (HOPL-I), ACM SIGPLAN Notices 13(8).](https://hannemyr.com/cache/knojd_acm78.pdf) |
| 12 | ALGOL 60 | ALGOL 68 | successor, an orthogonal redesign | solid | design |  | documented | documented | S1 | [Lindsey, C. H. (1996). A History of ALGOL 68. In History of Programming Languages II (HOPL-II), ACM Press / Addison-Wesley.](https://algol68-lang.org/docs/lindsey-history-of-algol68.pdf) |
| 13 | Fortran | SPSS | first written in Fortran | dotted | implementation |  | documented | n/a (implementation route) | S2 | [Uprichard, E., Burrows, R. & Byrne, D. (2008). SPSS as an 'inscription device': from causality to description? The Sociological Review (Goldsmiths Research Online preprint).](https://eprints-gro.gold.ac.uk/5823/2/SPSS_as_an_insciption_device_final_word_version_-_unproofe%E2%80%A6.pdf) |
| 14 | Fortran | B | declaration syntax: a specifier, then a list of names | dotted | syntax |  | documented | documented | S1 | [Ritchie, D. M. (1993). The Development of the C Language. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.cs.tufts.edu/~nr/cs257/archive/dennis-ritchie/chist.pdf) |
| 15 | BCPL | B | cut-down BCPL (Thompson) | solid | design |  | documented | documented | S1 | [Richards, M. (c. 2012). How BCPL evolved from CPL. Author's version, University of Cambridge Computer Laboratory.](https://www.cl.cam.ac.uk/~mr10/cpl2bcpl.pdf) |
| 16 | COBOL | Pascal | record types (via Hoare, ALGOL W) | dotted | type |  | documented | documented | S1 | [Wirth, N. (1993). Recollections about the Development of Pascal. HOPL II, ACM SIGPLAN Notices 28(3), 333-342.](http://pascal.hansotten.com/niklaus-wirth/recollections-about-the-development-of-pascal/) |
| 17 | ALGOL 60 | Pascal | precursor, via ALGOL W | solid | design |  | documented | documented | S1 | [Wirth, N. (2021). 50 Years of Pascal. Communications of the ACM 64(3).](https://informatika-21.ru/wirth/Pascal50E.pdf) |
| 18 | PL/I | C | loose structure pointers in early C; file inclusion | dotted | design |  | documented | documented | S1 | [Ritchie, D. M. (1993). The Development of the C Language. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.cs.tufts.edu/~nr/cs257/archive/dennis-ritchie/chist.pdf) |
| 19 | ALGOL 68 | C | type composition (Ritchie) | dotted | type |  | documented | documented | S1 | [Ritchie, D. M. (1993). The Development of the C Language. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.cs.tufts.edu/~nr/cs257/archive/dennis-ritchie/chist.pdf) |
| 20 | B | C | B plus types | solid | design |  | documented | documented | S1 | [Ritchie, D. M. (1993). The Development of the C Language. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.cs.tufts.edu/~nr/cs257/archive/dennis-ritchie/chist.pdf) |
| 21 | LISP | Smalltalk | language defined in itself (Lisp's eval) | solid | design |  | documented | documented | S1 | [Kay, A. C. (1993). The Early History of Smalltalk. HOPL-II, ACM SIGPLAN Notices 28(3).](https://worrydream.com/EarlyHistoryOfSmalltalk/) |
| 22 | Simula | Smalltalk | classes & objects | solid | design |  | documented | documented | S1 | [Kay, A. C. (1993). The Early History of Smalltalk. ACM SIGPLAN Notices 28(3) (HOPL-II).](https://worrydream.com/EarlyHistoryOfSmalltalk/) |
| 23 | Logo | Smalltalk | learning by programming | dotted | design |  | documented | documented | S1 | [Kay, A. C. (1993). The Early History of Smalltalk. ACM SIGPLAN Notices 28(3) (HOPL-II).](https://worrydream.com/EarlyHistoryOfSmalltalk/) |
| 24 | LISP | ML | a design influence on LCF/ML, and its implementation language | dotted | design |  | documented | n/a (implementation route) | S1 | [MacQueen, D., Harper, R. & Reppy, J. (2020). The History of Standard ML. Proceedings of the ACM on Programming Languages 4(HOPL), Article 86.](https://smlfamily.github.io/history/SML-history.pdf) |
| 25 | ISWIM | ML | let/where, expression language | solid | design |  | documented | documented | S1 | [MacQueen, D., Harper, R. & Reppy, J. (2020). The History of Standard ML. Proceedings of the ACM on Programming Languages 4(HOPL), Article 86.](https://smlfamily.github.io/history/SML-history.pdf) |
| 26 | LISP | CLU | object semantics: heap objects, references | solid | design |  | documented | documented | S1 | [Liskov, B. (1993). A History of CLU. HOPL II, ACM SIGPLAN Notices 28(3), 133-147 (MIT LCS report version, April 1992).](https://www.cs.tufts.edu/~nr/cs257/archive/barbara-liskov/clu-history.pdf) |
| 27 | ALGOL 60 | CLU | ALGOL-like syntax | dotted | syntax |  | documented | documented | S1 | [Liskov, B. (1993). A History of CLU. HOPL II, ACM SIGPLAN Notices 28(3), 133-147 (MIT LCS report version, April 1992).](https://www.cs.tufts.edu/~nr/cs257/archive/barbara-liskov/clu-history.pdf) |
| 28 | LISP | Scheme | minimal dialect | solid | design |  | documented | documented | S1 | [Steele, G. L., Jr. & Gabriel, R. P. (1993). The Evolution of Lisp. HOPL-II, ACM SIGPLAN Notices 28(3).](https://www.dreamsongs.com/Files/Hopl2.pdf) |
| 29 | ALGOL 60 | Scheme | lexical scoping | solid | design |  | documented | documented | S1 | [Steele, G. L., Jr. & Gabriel, R. P. (1993). The Evolution of Lisp. HOPL-II, ACM SIGPLAN Notices 28(3).](https://www.dreamsongs.com/Files/Hopl2.pdf) |
| 30 | Fortran | S | arithmetic expression syntax; first written in Fortran | dotted | syntax |  | documented | documented | S1 | [Becker, R. A. (1994). A Brief History of S. AT&T Bell Laboratories.](https://sas.uwaterloo.ca/~rwoldfor/software/R-code/historyOfS.pdf) |
| 31 | LISP | S | functions as first-class objects; attributes | solid | design |  | documented | documented | S1 | [Becker, R. A. (1994). A Brief History of S. AT&T Bell Laboratories.](https://sas.uwaterloo.ca/~rwoldfor/software/R-code/historyOfS.pdf) |
| 32 | ALGOL 60 | S | a separate assignment operator | dotted | syntax |  | documented | documented | S1 | [Becker, R. A. (1994). A Brief History of S. AT&T Bell Laboratories.](https://sas.uwaterloo.ca/~rwoldfor/software/R-code/historyOfS.pdf) |
| 33 | APL | S | multi-way arrays, consistent operations | solid | design |  | documented | documented | S1 | [Becker, R. A. (1994). A Brief History of S. AT&T Bell Laboratories.](https://sas.uwaterloo.ca/~rwoldfor/software/R-code/historyOfS.pdf) |
| 34 | C | S | braced expressions; arithmetic syntax | dotted | syntax |  | documented | documented | S1 | [Becker, R. A. (1994). A Brief History of S. AT&T Bell Laboratories.](https://sas.uwaterloo.ca/~rwoldfor/software/R-code/historyOfS.pdf) |
| 35 | Smalltalk | S | classes and inheritance | dotted | design | S 1991 | documented | documented | S1 | [Becker, R. A. (1994). A Brief History of S. AT&T Bell Laboratories.](https://sas.uwaterloo.ca/~rwoldfor/software/R-code/historyOfS.pdf) |
| 36 | Bourne sh | S | continuation lines | dotted | syntax | S on UNIX | indirect support only | documented | P1 | [Becker, R. A. (1994). A Brief History of S. AT&T Bell Laboratories.](https://sas.uwaterloo.ca/~rwoldfor/software/R-code/historyOfS.pdf) |
| 37 | Common Lisp | S | classes and inheritance (from CLOS) | dotted | design | S 1991 | documented | documented | S1 | [Becker, R. A. (1994). A Brief History of S. AT&T Bell Laboratories.](https://sas.uwaterloo.ca/~rwoldfor/software/R-code/historyOfS.pdf) |
| 38 | C++ | S | classes and inheritance | dotted | design | S 1991 | documented | documented | S1 | [Becker, R. A. (1994). A Brief History of S. AT&T Bell Laboratories.](https://sas.uwaterloo.ca/~rwoldfor/software/R-code/historyOfS.pdf) |
| 39 | SNOBOL | AWK | associative arrays (likened to SNOBOL4 tables) | dotted | design |  | documented | documented | S1 | [Aho, A. V., Kernighan, B. W., & Weinberger, P. J. (1988). The AWK Programming Language. Addison-Wesley. Chapter 8 (Epilog), section 8.1 'AWK as a Language'.](https://archive.org/stream/pdfy-MgN0H1joIoDVoIC7/The_AWK_Programming_Language_djvu.txt) |
| 40 | C | AWK | C-like syntax | solid | syntax |  | documented | documented | S1 | [Aho, A. V., Kernighan, B. W. & Weinberger, P. J. (1979). Awk — A Pattern Scanning and Processing Language. Software: Practice and Experience 9(4) (copy hosted at awk.dev).](https://www.awk.dev/awk.spe.pdf) |
| 41 | SNOBOL | Icon | SNOBOL4 patterns recast as string scanning | solid | design |  | documented | documented | S1 | [Griswold, R. E. (1994). Icon in the Humanities. TEXT Technology 4(1), 13-19 (online version updated 1996, University of Arizona).](https://raptor.cs.arizona.edu/icon/docs/humanit.htm) |
| 42 | Pascal | Modula-2 | Pascal's successor (Modula-2 adds modules) | solid | design |  | documented | documented | S1 | [Wirth, N. (2021). 50 Years of Pascal. Communications of the ACM 64(3).](https://informatika-21.ru/wirth/Pascal50E.pdf) |
| 43 | Pascal | TeX | written in WEB, Knuth's Pascal-based system | dotted | implementation |  | documented | n/a (implementation route) | S1 | [Knuth, D. E. (1982). TeX82 (tex.web), §1 Introduction. Copy in Xerox PARC Cedar archive, Computer History Museum.](https://xeroxparcarchive.computerhistory.org/cyan/cedarchest6.0/tex/.TeX.web!1.html) |
| 44 | ALGOL 68 | Bourne sh | if…fi, case…esac | solid | syntax |  | documented | documented | S1 | [Computerworld (2009). The A-Z of Programming Languages: Bourne shell, or sh (interview with Steve Bourne). Computerworld Australia / Computerwoche.](https://www.computerwoche.de/article/2720775/the-a-z-of-programming-languages-bourne-shell.html) |
| 45 | Simula | Ada | named among Ada's sources (no feature given) | dotted | design |  | documented | documented | S1 | [US Department of Defense (1983). Reference Manual for the Ada Programming Language (ANSI/MIL-STD-1815A), §1.3 Design Goals and Sources.](https://psc.informatik.uni-jena.de/languages/ada83/LRM-01.txt) |
| 46 | ALGOL 68 | Ada | named among Ada's sources (no feature given) | dotted | design |  | documented | documented | S1 | [US Department of Defense (1983). Reference Manual for the Ada Programming Language (ANSI/MIL-STD-1815A), §1.3 Design Goals and Sources.](https://psc.informatik.uni-jena.de/languages/ada83/LRM-01.txt) |
| 47 | Pascal | Ada | Pascal-family base | solid | design |  | documented | documented | S1 | [US Department of Defense (1983). Reference Manual for the Ada Programming Language (ANSI/MIL-STD-1815A), §1.3 Design Goals and Sources.](https://psc.informatik.uni-jena.de/languages/ada83/LRM-01.txt) |
| 48 | CLU | Ada | named among Ada's sources (no feature given) | dotted | design |  | documented | documented | S1 | [US Department of Defense (1983). Reference Manual for the Ada Programming Language (ANSI/MIL-STD-1815A), §1.3 Design Goals and Sources.](https://psc.informatik.uni-jena.de/languages/ada83/LRM-01.txt) |
| 49 | Java | Ada | interfaces | dotted | type | Ada 2005 | documented | documented | S1 | [Barnes, J. (2006). Rationale for Ada 2005, section 1.3.1 (Overview: the object oriented model).](https://www.adaic.org/resources/add_content/standards/05rat/html/Rat-1-3-1.html) |
| 50 | COBOL | ABAP | COBOL-like keyword statements | dotted | syntax |  | secondary source only | resemblance | P2 | [SAP Community blog (2021). ABAP: Past, Present, Future. blogs.sap.com (author not shown).](https://blogs.sap.com/2021/07/29/abap-past-present-future/) |
| 51 | Pascal | Turbo Pascal | standard Pascal, extended | solid | design |  | documented | documented | S1 | [Borland International (1985). TURBO Pascal Reference Manual, Version 3.0. Introduction, section "TURBO Pascal".](https://archive.decromancer.ca/bitsavers.org/pdf/borland/turbo_pascal/TURBO_Pascal_Reference_Manual_CPM_Version_3_Dec88.pdf) |
| 52 | C++ | Turbo Pascal | object-oriented extensions | dotted | design | Turbo Pascal 5.5 | documented | documented | S1 | [Borland International (1989). Turbo Pascal 5.5 Object-Oriented Programming Guide. Introduction, p. 1.](https://archive.decromancer.ca/bitsavers.org/pdf/borland/turbo_pascal/Turbo_Pascal_Version_5.5_Object-Oriented_Programming_Guide_1989.pdf) |
| 53 | LISP | Common Lisp | unified Maclisp line | solid | design |  | documented | documented | S1 | [Steele, G. L., Jr. & Gabriel, R. P. (1993). The Evolution of Lisp. HOPL-II, ACM SIGPLAN Notices 28(3).](https://www.dreamsongs.com/Files/Hopl2.pdf) |
| 54 | Scheme | Common Lisp | lexical scoping and closures | solid | design |  | documented | documented | S1 | [ANSI X3.226-1994, Programming Language Common Lisp, section 1.1.2 History (as in the Common Lisp HyperSpec, K. Pitman ed., 1996).](https://www.lispworks.com/documentation/HyperSpec/Body/01_ab.htm) |
| 55 | Fortran | MATLAB | built to call Fortran's LINPACK/EISPACK routines | dotted | library |  | documented | documented | S1 | [Moler, C. (2015, 15 June). Algol 60, PL/0 and MATLAB. Cleve's Corner, MathWorks blog.](https://blogs.mathworks.com/cleve/2015/06/15/algol-60-pl0-and-matlab/) |
| 56 | Pascal | MATLAB | syntax via Wirth's PL/0 | solid | syntax |  | indirect support only | not stated in the quoted sentence | P1 | [Moler, C. (2015, 15 June). Algol 60, PL/0 and MATLAB. Cleve's Corner, MathWorks blog.](https://blogs.mathworks.com/cleve/2015/06/15/algol-60-pl0-and-matlab/) |
| 57 | C | Objective-C | C plus messages | solid | design |  | documented | documented | S1 | [Apple Inc. (2014). Programming with Objective-C. Apple Developer Documentation Archive.](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html) |
| 58 | Smalltalk | Objective-C | Smalltalk-like messaging syntax | solid | design |  | indirect support only | documented | P1 | [Cox, B. J., Naroff, S. & Hsu, H. (2020). The Origins of Objective-C at PPI/Stepstone and Its Evolution at NeXT. Proc. ACM Program. Lang. 4 (HOPL IV).](https://hopl4.sigplan.org/details/hopl-4-papers/18/The-Origins-of-Objective-C-at-PPI-Stepstone-and-its-Evolution-at-NeXT) |
| 59 | Simula | C++ | classes, virtual functions | solid | design |  | documented | documented | S1 | [Stroustrup, B. (1993). A History of C++: 1979–1991. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.stroustrup.com/hopl2.pdf) |
| 60 | BCPL | C++ | // comments | dotted | syntax |  | documented | documented | S1 | [Stroustrup, B. (1993). A History of C++: 1979–1991. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.stroustrup.com/hopl2.pdf) |
| 61 | ALGOL 68 | C++ | operator overloading, declarations anywhere | solid | design |  | documented | documented | S1 | [Stroustrup, B. (1993). A History of C++: 1979–1991. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.stroustrup.com/hopl2.pdf) |
| 62 | C | C++ | C plus classes | solid | design |  | documented | documented | S1 | [Stroustrup, B. (1993). A History of C++: 1979–1991. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.stroustrup.com/hopl2.pdf) |
| 63 | ML | C++ | exception handling: throw an object, catch it by type | dotted | design | C++ after 1985 | documented | documented | S1 | [Stroustrup, B. (1993). A History of C++: 1979–1991. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.stroustrup.com/hopl2.pdf) |
| 64 | CLU | C++ | parameterized types, exceptions | dotted | design | C++ after 1985 | documented (Stroustrup) | widely described, not in the cited source | S1 | [Stroustrup, B. (1993). A History of C++: 1979–1991. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.stroustrup.com/hopl2.pdf) |
| 65 | Ada | C++ | named source of later ideas (no feature given) | dotted | design | C++ after 1985 | documented (Stroustrup) | widely described (Stroustrup's Design and Evolution of C++), not in the cited source | S1 | [Stroustrup, B. (1993). A History of C++: 1979–1991. ACM SIGPLAN Notices 28(3), HOPL-II.](https://www.stroustrup.com/hopl2.pdf) |
| 66 | Haskell | Excel formulas | LAMBDA (MSR functional-programming research) | dotted | design | LAMBDA 2020 | functional-programming research; Haskell not named | LAMBDA documented | P1 | [Microsoft Research Podcast (2021). Advancing Excel as a programming language with Andy Gordon and Simon Peyton Jones.](https://www.microsoft.com/en-us/research/?p=743248) |
| 67 | ISWIM | Miranda | ISWIM's applicative core, via PAL, SASL and KRC | solid | design |  | documented | documented | S1 | [Turner, D. A. (2012). Some History of Functional Programming Languages. Invited lecture, Trends in Functional Programming (TFP 2012), St Andrews.](https://www.cs.kent.ac.uk/people/staff/dat/tfp12/tfp12.pdf) |
| 68 | ML | Miranda | Milner's polymorphic types; type-variable notation | solid | type |  | documented | documented | S1 | [Turner, D. A. (2012). Some History of Functional Programming Languages. Invited lecture, Trends in Functional Programming (TFP 2012), St Andrews.](https://www.cs.kent.ac.uk/people/staff/dat/tfp12/tfp12.pdf) |
| 69 | Dartmouth BASIC | QuickBASIC | Microsoft's BASIC, compiled and structured | solid | design |  | documented | documented | S1 | [Winer, E. (1987). Interview with Greg Whitten. QuickTALK, vol. 1, no. 1.](https://qbmikehawk.neocities.org/interviews/GregWhitten) |
| 70 | C | Stata | Mata's C-like syntax | dotted | syntax | Stata 9 | indirect support only | not stated in the quoted sentence | P1 | [StataCorp (current release). Stata Mata Reference Manual, [M-2] syntax: Mata language grammar and syntax.](https://www.stata.com/manuals/m-2syntax.pdf) |
| 71 | Simula | Eiffel | classes, inheritance | solid | design |  | documented | documented | S1 | [Meyer, B. (n.d.). Bio. bertrandmeyer.com (designer's own website).](https://bertrandmeyer.com/bio/) |
| 72 | Prolog | Erlang | syntax, pattern matching; began as Prolog with processes | solid | design |  | documented | documented | S1 | [Armstrong, J. (2010). Talk slides, Erlang Factory SF Bay Area 2010.](https://www.erlang-factory.com/upload/presentations/222/ErlangFactorySFBay2010-JoeArmstrong.pdf) |
| 73 | Modula-2 | Oberon | simplified successor | solid | design |  | documented | documented | S1 | [Wirth, N. (1988). From Modula to Oberon. Software: Practice and Experience 18(7).](https://kronos.ru/node/39) |
| 74 | Pascal | Perl | 'vestiges' of Pascal (no feature given) | dotted | syntax |  | documented | documented | S1 | [Wall, L. (1987). perl(1) manual page, Perl 1.0 (header dated 87/12/18). Distributed with Perl 1.0 (2.11BSD source archive).](https://www.retro11.de/ouxr/211bsd/usr/src/new/PORT/perl.1.0.0/perl.man.1) |
| 75 | C | Perl | C-like syntax | solid | syntax |  | documented | documented | S1 | [Wall, L. (1987). perl(1) manual page, Perl 1.0 (header dated 87/12/18). Distributed with Perl 1.0 (2.11BSD source archive).](https://www.retro11.de/ouxr/211bsd/usr/src/new/PORT/perl.1.0.0/perl.man.1) |
| 76 | AWK | Perl | awk-style text scanning, reports | solid | design |  | documented | documented | S1 | [Wall, L. (1987). perl(1) manual page, Perl 1.0 (header dated 87/12/18). Distributed with Perl 1.0 (2.11BSD source archive).](https://www.retro11.de/ouxr/211bsd/usr/src/new/PORT/perl.1.0.0/perl.man.1) |
| 77 | Bourne sh | Perl | shell features (Wall names sh) | solid | syntax |  | documented | documented | S1 | [Wall, L. (1987). perl(1) manual page, Perl 1.0 (header dated 87/12/18). Distributed with Perl 1.0 (2.11BSD source archive).](https://www.retro11.de/ouxr/211bsd/usr/src/new/PORT/perl.1.0.0/perl.man.1) |
| 78 | APL | Self | no classes: objects made by copying; live workspace | dotted | design |  | documented | documented | S1 | [Ungar, D. & Smith, R. B. (2007). Self. Proc. HOPL III (ACM SIGPLAN History of Programming Languages).](https://worrydream.com/refs/Ungar_2007_-_Self_(HOPL).pdf) |
| 79 | Smalltalk | Self | simpler Smalltalk: prototypes, no classes | solid | design |  | documented | documented | S1 | [Ungar, D. & Smith, R. B. (2007). Self. Proc. HOPL III (ACM SIGPLAN History of Programming Languages).](https://worrydream.com/refs/Ungar_2007_-_Self_(HOPL).pdf) |
| 80 | SQL | T-SQL | SQL plus procedural code | solid | design |  | documented | documented | S1 | [Microsoft (n.d.). Describe T-SQL for programming. Microsoft Learn training module 'Get started with Transact-SQL programming'.](https://learn.microsoft.com/en-us/training/modules/get-started-transact-sql-programming/2-describe-transact-sql-for-programming) |
| 81 | LISP | Mathematica | early SMP sketches (with APL) | dotted | design |  | documented | documented | S1 | [Wolfram Research (n.d.). Wolfram Language FAQ: 'What languages were influences?'. wolfram.com.](https://www.wolfram.com/language/faq) |
| 82 | APL | Mathematica | some APL ideas (Wolfram) | dotted | design |  | documented | documented | S1 | [Wolfram, S. (2012). Answer to a reader question on APL, J and K/q. Stephen Wolfram Q&A, stephenwolfram.com, 14 May 2012.](https://stephenwolfram.com/questions/2012/05/14/have-you-ever-worked-with-apl-or-j-or-the-kq-programming-languages-and-what-is-your-opinion-of-j-especially-its-usefulness-in-research-mathematics-and-industry-and-perhaps-how-it-compares-w) |
| 83 | SQL | PL/SQL | SQL plus procedural code | solid | design |  | documented | documented | S1 | [Oracle (2019). Overview of PL/SQL. Oracle Database PL/SQL Language Reference, 19c.](https://docs.oracle.com/en/database/oracle/oracle-database/19/lnpls/overview.html) |
| 84 | Ada | PL/SQL | based on Ada | solid | design |  | documented | documented | S1 | [Oracle (2005). Oracle Database PL/SQL User's Guide and Reference 10g Release 2 (10.2), Appendix C: PL/SQL Program Limits.](https://docs.oracle.com/cd/B19306_01/appdev.102/b14261/limits.htm) |
| 85 | Bourne sh | Bash | Bourne Again | solid | design |  | documented | documented | S1 | [Ramey, C. & Fox, B. (current ed.). Bash Reference Manual, §1.1 "What is Bash?". Free Software Foundation (copy hosted by Chet Ramey, Case Western Reserve University).](https://tiswww.case.edu/php/chet/bash/bashref.html) |
| 86 | Modula-2 | Modula-3 | safety, objects | solid | design |  | documented | documented | S1 | [Cardelli, L., Donahue, J., Glassman, L., Jordan, M., Kalsow, B. & Nelson, G. (1989). Modula-3 Report (revised). DEC Systems Research Center, Research Report 52.](https://softwarepreservation.computerhistory.org/modula3/doc/SRC-RR-52.pdf) |
| 87 | ML | Haskell | Hindley-Milner types | solid | type |  | documented | documented | S1 | [Hudak, P., Hughes, J., Peyton Jones, S. & Wadler, P. (2007). A History of Haskell: Being Lazy with Class. HOPL III, ACM.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/07/history.pdf) |
| 88 | Miranda | Haskell | lazy, pure (open rewrite) | solid | design |  | documented | documented | S1 | [Hudak, P., Hughes, J., Peyton Jones, S. & Wadler, P. (2007). A History of Haskell: Being Lazy with Class. HOPL III, ACM.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/07/history.pdf) |
| 89 | APL | J | Iverson's ASCII successor | solid | design |  | documented | documented | S1 | [Iverson, K. E. (1991). A Personal View of APL. IBM Systems Journal 30(4).](https://www.jsoftware.com/papers/APLPersonalView1.htm) |
| 90 | ALGOL 68 | Python | string slicing | dotted | design |  | documented | documented | S1 | [Kuchling, A. M. (1998). LJ Interviews Guido van Rossum. Linux Journal.](https://www.linuxjournal.com/node/2959) |
| 91 | C | Python | keywords, operator precedence | solid | syntax |  | documented | documented | S1 | [Kuchling, A. M. (1998). LJ Interviews Guido van Rossum. Linux Journal.](https://www.linuxjournal.com/node/2959) |
| 92 | SQL | Python | SQL-style joins and group-by in pandas | dotted | library | pandas 2008 | indirect support only | n/a (library route) | P1 | [McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference (SciPy 2010).](https://proceedings.scipy.org/articles/Majora-92bf1922-00a.pdf) |
| 93 | Icon | Python | string slicing; later generators (Python 2.2) | dotted | design |  | documented | documented | S1 | [Kuchling, A. M. (1998). LJ Interviews Guido van Rossum. Linux Journal.](https://www.linuxjournal.com/node/2959) |
| 94 | Bourne sh | Python | script runner and interactive prompt | dotted | design |  | documented | documented | S1 | [Kuchling, A. M. (1998). LJ Interviews Guido van Rossum. Linux Journal.](https://www.linuxjournal.com/node/2959) |
| 95 | C++ | Python | class mechanism (with Modula-3) | dotted | design |  | documented | documented | S1 | [Python Software Foundation (current ed.). The Python Tutorial, §9 Classes. docs.python.org.](https://docs.python.org/3/tutorial/classes.html) |
| 96 | ABC | Python | indentation, built-in types | solid | design |  | documented | documented | S1 | [van Rossum, G. (2009). Early Language Design and Development. The History of Python (blog).](https://python-history.blogspot.com/2009/02/early-language-design-and-development.html) |
| 97 | Modula-3 | Python | modules, exceptions, explicit self | solid | design |  | documented | documented | S1 | [Kuchling, A. M. (1998). LJ Interviews Guido van Rossum. Linux Journal.](https://www.linuxjournal.com/node/2959) |
| 98 | Haskell | Python | list comprehensions | dotted | syntax | Python 2.0 | documented | documented | S1 | [Kuchling, A. M. & Zadka, M. (2000). What's New in Python 2.0, §List Comprehensions. Python documentation.](https://docs.python.org/3/whatsnew/2.0.html) |
| 99 | R | Python | data frames, via pandas | dotted | library | pandas 2008 | documented | documented | S1 | [McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference (SciPy 2010).](https://proceedings.scipy.org/articles/Majora-92bf1922-00a.pdf) |
| 100 | QuickBASIC | Visual Basic | the BASIC language behind the forms | solid | design |  | documented | documented | S1 | [Microsoft Corporation (1991). Microsoft Visual Basic. Microsoft News Releases, document Q72316 PR, May 1991 (updated 23 May 1991).](https://discmaster.textfiles.com/view/16184/MAX_PROGRAMMERS.iso/VISUAL_B/ARQS_ZIP/VBFACTS.ZIP/VBFACTS.TXT) |
| 101 | APL | K / q | Whitney's APL line, in ASCII | solid | design |  | documented | documented | S1 | [Cantrill, B. (2009). A Conversation with Arthur Whitney. ACM Queue 7(2).](https://queue.acm.org/detail.cfm?id=1531242) |
| 102 | CLU | Lua | multiple assignment and returns | dotted | design |  | documented | documented | S1 | [Ierusalimschy, R., de Figueiredo, L. H. & Celes, W. (2007). The Evolution of Lua. HOPL III, ACM.](https://www.lua.org/doc/hopl.pdf) |
| 103 | Scheme | Lua | closures, first-class functions | solid | design | Lua 3.1 | documented | documented | S1 | [Ierusalimschy, R., de Figueiredo, L. H. & Celes, W. (2007). The Evolution of Lua. HOPL III, ACM.](https://www.lua.org/doc/hopl.pdf) |
| 104 | AWK | Lua | associative arrays (tables) | solid | design |  | documented | documented | S1 | [Ierusalimschy, R., de Figueiredo, L. H. & Celes, W. (2007). The Evolution of Lua. HOPL III, ACM.](https://www.lua.org/doc/hopl.pdf) |
| 105 | Modula-2 | Lua | control-structure syntax (while, if, repeat…until) | dotted | syntax |  | documented | documented | S1 | [Ierusalimschy, R., de Figueiredo, L. H. & Celes, W. (2007). The Evolution of Lua. HOPL III, ACM.](https://www.lua.org/doc/hopl.pdf) |
| 106 | C++ | Lua | local variables declared where needed | dotted | design |  | documented | documented | S1 | [Ierusalimschy, R., de Figueiredo, L. H. & Celes, W. (2007). The Evolution of Lua. HOPL III, ACM.](https://www.lua.org/doc/hopl.pdf) |
| 107 | SQL | R | SQL-inspired verbs, via dplyr | dotted | library | dplyr 2014 | documented | n/a (library route) | S1 | [Wickham, H., Çetinkaya-Rundel, M., & Grolemund, G. (2023). R for Data Science (2nd ed.), ch. 'Databases'. O'Reilly.](https://r4ds.hadley.nz/databases.html) |
| 108 | Scheme | R | closures, lexical scope | solid | design |  | documented | documented | S1 | [Ihaka, R. (1998). R: Past and Future History. Interface '98 (Computing Science and Statistics).](https://www.stat.auckland.ac.nz/~ihaka/downloads/Interface98.pdf) |
| 109 | S | R | S-like syntax and features | solid | design |  | documented | documented | S1 | [Ihaka, R. (1998). R: Past and Future History. Interface '98 (Computing Science and Statistics).](https://www.stat.auckland.ac.nz/~ihaka/downloads/Interface98.pdf) |
| 110 | Bourne sh | R | Unix pipes, a motivation for the magrittr pipe | dotted | library | magrittr 2014 | documented | n/a (library route) | S1 | [Bache, S. M. & Wickham, H. (n.d.). Introducing magrittr (package vignette), CRAN; and Tierney, L. (n.d.). Native pipe design note (PIPE.md), R Project SVN.](https://archive.linux.duke.edu/cran/web/packages/magrittr/vignettes/magrittr.html) |
| 111 | F# | R | pipe \|>, via magrittr; native in R 4.1 | dotted | library | R 4.1 | documented | n/a (library route) | S1 | [Bache, S. M. & Wickham, H. (n.d.). Introducing magrittr (package vignette), CRAN; and Tierney, L. (n.d.). Native pipe design note (PIPE.md), R Project SVN.](https://archive.linux.duke.edu/cran/web/packages/magrittr/vignettes/magrittr.html) |
| 112 | Visual Basic | VBA | VB inside Office | solid | design |  | documented | documented | S1 | [Microsoft (n.d.). Visual Basic for Applications Frequently Asked Questions. MSDN (Previous Versions).](https://learn.microsoft.com/en-us/previous-versions/msdn10/bb190540(v=msdn.10)) |
| 113 | Turbo Pascal | Delphi | Object Pascal; the same compiler line | solid | design |  | documented | documented | S1 | [Civeyrac, A.-L. (2019). The One Who Created Languages (interview with Anders Hejlsberg). Welcome to the Jungle, 11 February 2019.](https://www.welcometothejungle.com/en-GB/articles/video/anders-hejlsberg-microsoft-career) |
| 114 | Smalltalk | Java | object-oriented concepts (no feature given) | dotted | design |  | documented | documented | S1 | [Gosling, J. & McGilton, H. (1996). The Java Language Environment: A White Paper. Sun Microsystems.](https://www.oracle.com/java/technologies/introduction-to-Java.html) |
| 115 | Objective-C | Java | interfaces, from Objective-C protocols | solid | type |  | documented | documented | S1 | [Gosling, J. & McGilton, H. (1996). The Java Language Environment: A White Paper. Sun Microsystems.](https://www.oracle.com/java/technologies/object-oriented.html) |
| 116 | C++ | Java | syntax, minus pointers | solid | syntax |  | documented | documented | S1 | [Gosling, J. & McGilton, H. (1996). The Java Language Environment: A White Paper. Sun Microsystems.](https://www.oracle.com/java/technologies/introduction-to-Java.html) |
| 117 | Eiffel | Java | object-oriented concepts (no feature given) | dotted | design |  | documented | documented | S1 | [Gosling, J. & McGilton, H. (1996). The Java Language Environment: A White Paper. Sun Microsystems.](https://www.oracle.com/java/technologies/introduction-to-Java.html) |
| 118 | Scheme | JavaScript | first-class functions | solid | design |  | documented | documented | S1 | [Eich, B. (2008, April 3). Popularity. brendaneich.com.](https://brendaneich.com/2008/04/popularity/) |
| 119 | AWK | JavaScript | the function keyword; for…in | dotted | syntax |  | documented | documented | S1 | [Wirfs-Brock, A. and Eich, B. (2020). JavaScript: The First 20 Years. Proceedings of the ACM on Programming Languages 4 (HOPL), Article 77 (authors' corrections, March 2021).](https://www.wirfs-brock.com/allen/jshopl.pdf) |
| 120 | Self | JavaScript | prototypes | solid | design |  | documented | documented | S1 | [Eich, B. (2008). Popularity. brendaneich.com (blog).](https://brendaneich.com/2008/04/popularity/) |
| 121 | Perl | JavaScript | regular expressions; array and string methods | dotted | syntax | JavaScript 1.2 | documented | documented | S1 | [Wirfs-Brock, A. and Eich, B. (2020). JavaScript: The First 20 Years. Proceedings of the ACM on Programming Languages 4 (HOPL), Article 77 (authors' corrections, March 2021).](https://www.wirfs-brock.com/allen/jshopl.pdf) |
| 122 | Python | JavaScript | generators and iterators | dotted | design | ES2015 | documented | documented | S1 | [Eich, B. (2006). Python and JavaScript. brendaneich.com (blog), 19 Feb 2006.](https://brendaneich.com/?p=49) |
| 123 | Java | JavaScript | syntax, by marketing mandate | dotted | syntax |  | documented | documented | S1 | [Eich, B. (2008). Popularity. brendaneich.com (blog).](https://brendaneich.com/2008/04/popularity/) |
| 124 | C | PHP | C-like syntax, function names | solid | syntax |  | documented | documented | S1 | [The PHP Group (current ed.). History of PHP. PHP Manual.](https://www.php.net/manual/en/history.php.php) |
| 125 | Perl | PHP | syntax, $ variables | solid | syntax |  | documented | documented | S1 | [PHP Documentation Group (c. 1999-2000). PHP Manual, Preface (PHP 3.0.18 edition, copy shipped in the Debian php3 package).](https://sources.debian.org/data/main/p/php3/3:3.0.18-31/doc/preface.html) |
| 126 | Java | PHP | syntax (with C and Perl) | dotted | syntax |  | documented | documented | S1 | [PHP Documentation Group (c. 1999-2000). PHP Manual, Preface (PHP 3.0.18 edition, copy shipped in the Debian php3 package).](https://sources.debian.org/data/main/p/php3/3:3.0.18-31/doc/preface.html) |
| 127 | LISP | Ruby | closures and blocks; truth values | dotted | design |  | documented | documented | S1 | [Ruby community (current ed.). About Ruby. ruby-lang.org (official site).](https://www.ruby-lang.org/en/about/) |
| 128 | Smalltalk | Ruby | everything is an object | solid | design |  | documented | documented | S1 | [Ruby community (current ed.). About Ruby. ruby-lang.org (official site).](https://www.ruby-lang.org/en/about/) |
| 129 | CLU | Ruby | iterators, yield | dotted | design |  | secondary source only | iterators (secondary) | P2 | [AppFolio Engineering Blog (2019, July 3). Ruby's Roots and Matz's Leadership (recap of a Matz talk at Cookpad, Bristol).](https://engineering.appfolio.com/appfolio-engineering/2019/7/3/rubys-roots-and-matzs-leadership) |
| 130 | Eiffel | Ruby | end-delimited syntax, rescue/ensure | dotted | syntax |  | documented (Eiffel named) | secondary source only | P1 | [Ruby community (current ed.). About Ruby. ruby-lang.org (official site).](https://www.ruby-lang.org/en/about/) |
| 131 | Perl | Ruby | regex, scripting | solid | design |  | documented | documented | S1 | [Matsumoto, Y. (1999, June 4). Post on Ruby's history. ruby-talk mailing list, message 382.](https://blade.ruby-lang.org/ruby-talk/382) |
| 132 | ML | OCaml | dialect + objects | solid | design |  | documented | documented | S1 | [OCaml.org (n.d.). About OCaml / history. Official OCaml website.](https://ocaml.org/about) |
| 133 | SQL | MDX | SELECT syntax for cubes | solid | design |  | indirect support only | documented | P1 | [Microsoft (n.d., archived 2016). Multidimensional Expressions (OLE DB). OLE DB for OLAP Programmer's Reference, Microsoft Learn (previous versions).](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ms714949(v=vs.85)) |
| 134 | Icon | C# | iterators (yield) | dotted | design | C# 2.0 | documented | documented | S1 | [Syme, D. (2020). The Early History of F#. Proceedings of the ACM on Programming Languages 4 (HOPL), Article 75.](https://fsharp.org/history/hopl-final/hopl-fsharp.pdf) |
| 135 | C++ | C# | C-family syntax | solid | design |  | documented | documented | S1 | [Morris, R. (2009). Anders Hejlsberg: Geek of the Week (interview). Simple Talk, Redgate.](https://www.red-gate.com/simple-talk/opinion/geek-of-the-week/anders-hejlsberg-geek-of-the-week/) |
| 136 | Haskell | C# | LINQ query comprehensions | dotted | design | C# 3.0 | documented | documented | S1 | [Meijer, E. (2007). Confessions of a Used Programming Language Salesman: Getting the Masses Hooked on Haskell. OOPSLA 2007.](https://people.willamette.edu/~fruehr/talks/webcs/MeijerICFP06.pdf) |
| 137 | Python | C# | dynamic typing (the dynamic type) | dotted | type | C# 4.0 | documented | documented | S1 | [Syme, D. (2020). The Early History of F#. Proceedings of the ACM on Programming Languages 4 (HOPL), Article 75.](https://fsharp.org/history/hopl-final/hopl-fsharp.pdf) |
| 138 | Java | C# | type safety, exceptions, GC | solid | design |  | documented | documented | S1 | [Morris, R. (2009). Anders Hejlsberg: Geek of the Week (interview). Simple Talk, Redgate.](https://www.red-gate.com/simple-talk/opinion/geek-of-the-week/anders-hejlsberg-geek-of-the-week/) |
| 139 | Delphi | C# | properties, events, is/as (same designer, Hejlsberg) | solid | design |  | documented (Hejlsberg names Delphi; same designer) | widely described, not in the cited source | S1 | [Morris, R. (2009). Anders Hejlsberg: Geek of the Week (interview). Simple Talk, Redgate.](https://www.red-gate.com/simple-talk/opinion/geek-of-the-week/anders-hejlsberg-geek-of-the-week/) |
| 140 | F# | C# | async/await, from F# async workflows | dotted | design | C# 5.0 | documented | documented | S1 | [Syme, D. (2020). The Early History of F#. Proceedings of the ACM on Programming Languages 4 (HOPL), Article 75.](https://fsharp.org/history/hopl-final/hopl-fsharp.pdf) |
| 141 | C | Cyclone | safe C dialect | solid | design |  | documented | documented | S1 | [Jim, T., Morrisett, G., Grossman, D., Hicks, M., Cheney, J. & Wang, Y. (2002). Cyclone: A safe dialect of C. USENIX Annual Technical Conference.](https://www.usenix.org/legacy/publications/library/proceedings/usenix02/full_papers/jim/jim.pdf) |
| 142 | ML | Cyclone | early design choices carried over from ML | dotted | design |  | documented | documented | S1 | [Jim, T., Morrisett, G., Grossman, D., Hicks, M., Cheney, J. & Wang, Y. (2002). Cyclone: A safe dialect of C. USENIX Annual Technical Conference.](https://www.usenix.org/legacy/publications/library/proceedings/usenix02/full_papers/jim/jim.pdf) |
| 143 | Smalltalk | Scala | uniform object model: every value an object | dotted | design |  | documented | documented | S1 | [Odersky, M. et al. (2006). An Overview of the Scala Programming Language, Second Edition. EPFL Technical Report LAMP-REPORT-2006-001, section 10.](https://www.scala-lang.org/docu/files/ScalaOverview.pdf) |
| 144 | ML | Scala | abstract types, after ML's module systems | dotted | type |  | indirect support only | documented | P1 | [Odersky, M. et al. (2006). An Overview of the Scala Programming Language, Second Edition. EPFL Technical Report LAMP-REPORT-2006-001, section 10 (Related Work).](https://www.scala-lang.org/docu/files/ScalaOverview.pdf) |
| 145 | Eiffel | Scala | uniform access principle | dotted | design |  | documented | documented | S1 | [Odersky, M., Spoon, L. & Venners, B. (2008). Programming in Scala, 1st ed., ch. 1 'Scala's roots'. Artima.](https://www.artima.com/pins1ed/a-scalable-language.html) |
| 146 | Erlang | Scala | actor-based concurrency library | dotted | library |  | documented | n/a (library route) | S1 | [Odersky, M., Spoon, L. & Venners, B. (2008). Programming in Scala, 1st ed., ch. 1 'Scala's roots'. Artima.](https://www.artima.com/pins1ed/a-scalable-language.html) |
| 147 | Haskell | Scala | type classes | solid | type |  | documented | documented | S1 | [Odersky, M., Spoon, L. & Venners, B. (2008). Programming in Scala, 1st ed., ch. 1 'Scala's roots'. Artima.](https://www.artima.com/pins1ed/a-scalable-language.html) |
| 148 | Python | Scala | indentation syntax | dotted | syntax | Scala 3 | indirect support only | not stated in the quoted sentence | P1 | [Odersky, M. (2019). Allow significant indentation syntax (pull request #7083). scala/scala3 (Dotty) repository, GitHub.](https://github.com/scala/scala3/pull/7083) |
| 149 | Java | Scala | classes, JVM interop | solid | syntax |  | documented | documented | S1 | [Odersky, M. (2006). A Brief History of Scala. Artima Weblogs.](https://www.artima.com/weblogs/viewpost.jsp?thread=163733) |
| 150 | C# | Scala | surface syntax (with Java) | dotted | syntax |  | documented | documented | S1 | [Odersky, M., Spoon, L. & Venners, B. (2008). Programming in Scala, 1st ed., ch. 1 'Scala's roots'. Artima.](https://www.artima.com/pins1ed/a-scalable-language.html) |
| 151 | Haskell | F# | background for computation expressions (do notation, comprehensions) | dotted | design | F# 2007 | indirect support only | documented | P1 | [Syme, D. (2020). The Early History of F#. Proceedings of the ACM on Programming Languages 4(HOPL), Article 75.](https://fsharp.org/history/hopl-final/hopl-fsharp.pdf) |
| 152 | Python | F# | indentation-aware syntax | dotted | syntax | F# 2006 | documented | documented | S1 | [Syme, D. (2020). The Early History of F#. Proceedings of the ACM on Programming Languages 4(HOPL), Article 75.](https://fsharp.org/history/hopl-final/hopl-fsharp.pdf) |
| 153 | OCaml | F# | OCaml for .NET | solid | design |  | documented | documented | S1 | [Syme, D. (2020). The Early History of F#. Proceedings of the ACM on Programming Languages 4(HOPL), Article 75.](https://fsharp.org/history/hopl-final/hopl-fsharp.pdf) |
| 154 | C# | F# | objects, properties, events; later LINQ | dotted | design |  | documented | documented | S1 | [Syme, D. (2020). The Early History of F#. Proceedings of the ACM on Programming Languages 4(HOPL), Article 75.](https://fsharp.org/history/hopl-final/hopl-fsharp.pdf) |
| 155 | Bourne sh | PowerShell | pipelines, but of objects | solid | design |  | documented | documented | S1 | [Snover, J. (2002). Monad Manifesto. Microsoft (republished at jsnover.com).](https://www.jsnover.com/Docs/MonadManifesto.pdf) |
| 156 | C# | PowerShell | C#-like syntax (glide path to C#) | dotted | syntax |  | documented | documented | S1 | [Snover, J. (2002). Monad Manifesto. Microsoft (republished at jsnover.com).](https://www.jsnover.com/Docs/MonadManifesto.pdf) |
| 157 | LISP | Clojure | Lisp dialect: code as data, macros | solid | design |  | documented | documented | S1 | [Hickey, R. (2020). A History of Clojure. Proceedings of the ACM on Programming Languages 4(HOPL), 1-46.](https://hopl4.sigplan.org/details/hopl-4-papers/9/A-History-of-Clojure) |
| 158 | ML | Clojure | references as the model for state | dotted | design |  | documented | documented | S1 | [Hickey, R. (2020). A History of Clojure. Proceedings of the ACM on Programming Languages 4(HOPL), Article 71.](https://dl.acm.org/doi/10.1145/3386321) |
| 159 | Common Lisp | Clojure | multimethods, from generic functions | dotted | design |  | documented | documented | S1 | [Hickey, R. (2020). A History of Clojure. Proceedings of the ACM on Programming Languages 4(HOPL), Article 71.](https://dl.acm.org/doi/10.1145/3386321) |
| 160 | Haskell | Clojure | protocols as an open system, like type classes | dotted | type | Clojure 1.2 | documented | documented | S1 | [Hickey, R. (2020). A History of Clojure. Proceedings of the ACM on Programming Languages 4(HOPL), Article 71.](https://dl.acm.org/doi/10.1145/3386321) |
| 161 | Java | Clojure | designed to be hosted on the JVM | dotted | platform |  | documented | documented | S1 | [Hickey, R. (2020). A History of Clojure. Proceedings of the ACM on Programming Languages 4(HOPL), 1-46.](https://hopl4.sigplan.org/details/hopl-4-papers/9/A-History-of-Clojure) |
| 162 | Logo | Scratch | Papert's Logo: turtle, low floor | solid | design |  | documented | documented | S1 | [Resnick, M. (2022). 10 sparks that lit the flame of Scratch. Medium.](https://mres.medium.com/10-sparks-that-lit-the-flame-of-scratch-595a27d44334) |
| 163 | Excel formulas | DAX | formula syntax | solid | syntax |  | documented | documented | S1 | [Microsoft (2010). Data Analysis Expressions (DAX) and MDX. SQL Server 2008 R2 documentation.](https://learn.microsoft.com/en-us/previous-versions/sql/sql-server-2008-r2/ff487170(v=sql.105)) |
| 164 | APL | Go | iota, the constant counter | dotted | syntax |  | documented | documented | S1 | [Pike, R. (2014). Hello, Gophers! GopherCon opening keynote, 24 April 2014, slide 'Not just C'.](https://go.googlesource.com/website/+/33b532a2f57ccceaeaf826d86ca10b069ce5cd9e/_content/talks/2014/hellogophers.slide) |
| 165 | BCPL | Go | automatic semicolon rule | dotted | syntax |  | documented | documented | S1 | [Pike, R. (2014). Hello, Gophers! GopherCon opening keynote, 24 April 2014, slide 'Not just C'.](https://go.googlesource.com/website/+/33b532a2f57ccceaeaf826d86ca10b069ce5cd9e/_content/talks/2014/hellogophers.slide) |
| 166 | B | Go | same designer (Ken Thompson) | dotted | organizational |  | indirect support only | n/a (organizational route) | P1 | [The Go Authors (n.d.). Frequently Asked Questions: 'What is the history of the project?'. go.dev.](https://go.dev/doc/faq) |
| 167 | C | Go | C-style expression syntax | solid | syntax |  | documented | documented | S1 | [The Go Authors (n.d.). Frequently Asked Questions: 'What are Go's ancestors?'. go.dev.](https://go.dev/doc/faq) |
| 168 | Smalltalk | Go | methods | dotted | design |  | documented | documented | S1 | [Pike, R. (2014). Hello, Gophers! GopherCon opening keynote, 24 April 2014, slide 'Not just C'.](https://go.googlesource.com/website/+/33b532a2f57ccceaeaf826d86ca10b069ce5cd9e/_content/talks/2014/hellogophers.slide) |
| 169 | Oberon | Go | declarations, packages | solid | design |  | documented | documented | S1 | [The Go Authors (n.d.). Frequently Asked Questions: 'What are Go's ancestors?'. go.dev.](https://go.dev/doc/faq) |
| 170 | Newsqueak | Go | channels, goroutines (via Alef, Limbo) | solid | design |  | documented | documented | S1 | [The Go Authors (n.d.). Frequently Asked Questions: 'What are Go's ancestors?'. go.dev.](https://go.dev/doc/faq) |
| 171 | Scheme | Rust | hygienic macros | dotted | design |  | documented | documented | S1 | [The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.](https://doc.rust-lang.org/reference/influences.html) |
| 172 | C++ | Rust | RAII, move semantics, monomorphization | solid | design |  | documented | documented | S1 | [The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.](https://doc.rust-lang.org/reference/influences.html) |
| 173 | Erlang | Rust | message passing, lightweight concurrency | dotted | design |  | documented | documented | S1 | [The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.](https://doc.rust-lang.org/reference/influences.html) |
| 174 | Newsqueak | Rust | channels, concurrency | dotted | design |  | documented | documented | S1 | [The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.](https://doc.rust-lang.org/reference/influences.html) |
| 175 | Haskell | Rust | traits from type classes | solid | type |  | documented | documented | S1 | [The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.](https://doc.rust-lang.org/reference/influences.html) |
| 176 | Ruby | Rust | closure and block syntax | dotted | syntax |  | documented | documented | S1 | [The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.](https://doc.rust-lang.org/reference/influences.html) |
| 177 | OCaml | Rust | algebraic data types, pattern matching | solid | design |  | documented | documented | S1 | [The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.](https://doc.rust-lang.org/reference/influences.html) |
| 178 | C# | Rust | attributes | dotted | syntax |  | documented | documented | S1 | [The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.](https://doc.rust-lang.org/reference/influences.html) |
| 179 | Cyclone | Rust | region-based memory (lifetimes) | solid | design |  | documented | documented | S1 | [The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.](https://doc.rust-lang.org/reference/influences.html) |
| 180 | Swift | Rust | optional bindings (if let) | dotted | syntax | Rust 0.12 | documented | documented | S1 | [The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.](https://doc.rust-lang.org/reference/influences.html) |
| 181 | SQL | Cypher | SQL-like clauses for graphs (MATCH … WHERE … RETURN) | solid | syntax |  | documented | documented | S1 | [Francis, N., Green, A., Guagliardo, P., Libkin, L., Lindaaker, T., Marsault, V., Plantikow, S., Rydberg, M., Selmer, P., & Taylor, A. (2018). Cypher: An Evolving Query Language for Property Graphs. SIGMOD '18, pp. 1433-1445.](https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf) |
| 182 | Python | Cypher | named inspiration (no feature given) | dotted | design |  | documented | documented | S1 | [Francis, N., Green, A., Guagliardo, P., Libkin, L., Lindaaker, T., Marsault, V., Plantikow, S., Rydberg, M., Selmer, P., & Taylor, A. (2018). Cypher: An Evolving Query Language for Property Graphs. SIGMOD '18, pp. 1433-1445.](https://www.pure.ed.ac.uk/ws/files/56321692/cypher_sigmod18_crc_1.pdf) |
| 183 | Smalltalk | Dart | pure objects, mixins, optional types (via Strongtalk) | solid | design |  | documented | documented | S1 | [Bracha, G. (2015). The Dart Programming Language, §1.6. Addison-Wesley (sample pages).](https://ptgmedia.pearsoncmg.com/images/9780321927705/samplepages/9780321927705.pdf) |
| 184 | Erlang | Dart | actor-style concurrency (isolates) | dotted | design |  | documented | documented | S1 | [Bracha, G. (2015). The Dart Programming Language, §1.6. Addison-Wesley (sample pages).](https://ptgmedia.pearsoncmg.com/images/9780321927705/samplepages/9780321927705.pdf) |
| 185 | JavaScript | Dart | single-threaded event loop, closures | dotted | syntax |  | documented (Bracha) | widely described, not in the cited source | S1 | [Bracha, G. (2015). The Dart Programming Language, §1.6. Addison-Wesley (sample pages).](https://ptgmedia.pearsoncmg.com/images/9780321927705/samplepages/9780321927705.pdf) |
| 186 | Java | Dart | class-based, single inheritance | solid | syntax |  | documented | documented | S1 | [Bracha, G. (2015). The Dart Programming Language, §1.6. Addison-Wesley (sample pages).](https://ptgmedia.pearsoncmg.com/images/9780321927705/samplepages/9780321927705.pdf) |
| 187 | C# | Dart | async/await | dotted | design | Dart 1.9 | documented | documented | S1 | [Bracha, G. (2015). The Dart Programming Language, §1.6. Addison-Wesley (sample pages).](https://ptgmedia.pearsoncmg.com/images/9780321927705/samplepages/9780321927705.pdf) |
| 188 | Java | Kotlin | classes, 100% JVM interop | solid | design |  | documented | documented | S1 | [JetBrains (n.d.). FAQ. Kotlin Documentation, kotlinlang.org.](https://kotlinlang.org/docs/faq.html) |
| 189 | JavaScript | Kotlin | named inspiration (no feature given) | dotted | design |  | documented | documented | S1 | [JetBrains (n.d.). FAQ. Kotlin Documentation, kotlinlang.org.](https://kotlinlang.org/docs/faq.html) |
| 190 | C# | Kotlin | extension functions (Breslav talk) | dotted | design |  | documented | documented | S1 | [JetBrains (n.d.). FAQ. Kotlin Documentation, kotlinlang.org.](https://kotlinlang.org/docs/faq.html) |
| 191 | Scala | Kotlin | val/var, name: Type, primary constructors, object singletons | dotted | design |  | documented (Kotlin FAQ) | widely described, not in the cited source | S1 | [JetBrains (n.d.). FAQ. Kotlin Documentation, kotlinlang.org.](https://kotlinlang.org/docs/faq.html) |
| 192 | Erlang | Elixir | processes, OTP, the BEAM | solid | design |  | documented | documented | S1 | [Valim, J. (2013). Elixir Design Goals. elixir-lang.org blog, 8 August 2013.](https://elixir-lang.org/blog/2013/08/08/elixir-design-goals/) |
| 193 | Ruby | Elixir | Ruby-like surface syntax | dotted | syntax |  | documented | documented | S1 | [Valim, J. (2013). Elixir Design Goals. elixir-lang.org blog, 8 August 2013.](https://elixir-lang.org/blog/2013/08/08/elixir-design-goals/) |
| 194 | F# | Elixir | pipe operator \|> | dotted | syntax |  | documented | documented | S1 | [Valim, J. (2018). Post in 'Which language first introduced the pipe operator?'. Elixir Forum.](https://elixirforum.com/t/which-language-first-introduced-the-pipe-operator/16791) |
| 195 | Clojure | Elixir | protocols | dotted | design |  | documented | documented | S1 | [Valim, J. (2013). Elixir Design Goals. elixir-lang.org blog, 8 August 2013.](https://elixir-lang.org/blog/2013/08/08/elixir-design-goals/) |
| 196 | LISP | Julia | homoiconicity and true macros | solid | design |  | documented | documented | S1 | [Bezanson, J., Karpinski, S., Shah, V. B. & Edelman, A. (2012, 14 February). Why We Created Julia. julialang.org blog.](https://julialang.org/blog/2012/02/why-we-created-julia/) |
| 197 | C | Julia | the speed of C as a design aim | dotted | design |  | documented | documented | S1 | [Bezanson, J., Karpinski, S., Shah, V. B. & Edelman, A. (2012, 14 February). Why We Created Julia. julialang.org blog.](https://julialang.org/blog/2012/02/why-we-created-julia/) |
| 198 | Bourne sh | Julia | gluing programs together as a design aim | dotted | design |  | documented | documented | S1 | [Bezanson, J., Karpinski, S., Shah, V. B. & Edelman, A. (2012, 14 February). Why We Created Julia. julialang.org blog.](https://julialang.org/blog/2012/02/why-we-created-julia/) |
| 199 | Common Lisp | Julia | generic functions (CLOS as an earlier system) | dotted | design |  | indirect support only | not stated in the quoted sentence | P1 | [Bezanson, J., Karpinski, S., Shah, V. B. & Edelman, A. (2012). Julia: A Fast Dynamic Language for Technical Computing. arXiv:1209.5145.](https://arxiv.org/pdf/1209.5145) |
| 200 | MATLAB | Julia | familiar mathematical notation | solid | syntax |  | documented | documented | S1 | [Bezanson, J., Karpinski, S., Shah, V. B. & Edelman, A. (2012, 14 February). Why We Created Julia. julialang.org blog.](https://julialang.org/blog/2012/02/why-we-created-julia/) |
| 201 | Perl | Julia | string processing as a design aim | dotted | design |  | documented | documented | S1 | [Bezanson, J., Karpinski, S., Shah, V. B. & Edelman, A. (2012, 14 February). Why We Created Julia. julialang.org blog.](https://julialang.org/blog/2012/02/why-we-created-julia/) |
| 202 | Python | Julia | general-purpose usability as a design aim | dotted | design |  | documented | documented | S1 | [Bezanson, J., Karpinski, S., Shah, V. B. & Edelman, A. (2012, 14 February). Why We Created Julia. julialang.org blog.](https://julialang.org/blog/2012/02/why-we-created-julia/) |
| 203 | R | Julia | ease for statistics as a design aim | dotted | design |  | documented | documented | S1 | [Bezanson, J., Karpinski, S., Shah, V. B. & Edelman, A. (2012, 14 February). Why We Created Julia. julialang.org blog.](https://julialang.org/blog/2012/02/why-we-created-julia/) |
| 204 | Lua | Julia | named among the dynamic languages Julia borrows from | dotted | design |  | documented | documented | S1 | [The Julia Project (n.d.). Julia Documentation, home page, section 'Julia Compared to Other Languages'. docs.julialang.org (v1).](https://docs.julialang.org/en/v1/) |
| 205 | Ruby | Julia | the dynamism of Ruby as a design aim | dotted | design |  | documented | documented | S1 | [Bezanson, J., Karpinski, S., Shah, V. B. & Edelman, A. (2012, 14 February). Why We Created Julia. julialang.org blog.](https://julialang.org/blog/2012/02/why-we-created-julia/) |
| 206 | JavaScript | TypeScript | superset + types | solid | design |  | documented | documented | S1 | [Microsoft (n.d.). TypeScript (README). GitHub repository microsoft/TypeScript.](https://github.com/microsoft/TypeScript) |
| 207 | C# | TypeScript | same lead designer (Anders Hejlsberg) | dotted | organizational |  | indirect support only | n/a (organizational route) | P1 | [Microsoft (n.d.). Anders Hejlsberg, author page. TypeScript blog, devblogs.microsoft.com.](https://devblogs.microsoft.com/typescript/author/andersh/) |
| 208 | F# | Power Query M | functional; 'similar to F#' (Microsoft) | dotted | design |  | resemblance ('similar to F#') | resemblance | P1 | [Microsoft (n.d.). Power Query M formula language. Microsoft Learn.](https://learn.microsoft.com/en-us/powerquery-m/) |
| 209 | PHP | Hack | PHP plus gradual typing | solid | design |  | documented | documented | S1 | [Verlaguet, J. & Menghrajani, A. (2014, March 20). Hack: a new programming language for HHVM. Engineering at Meta (Facebook Engineering blog).](https://engineering.fb.com/2014/03/20/developer-tools/hack-a-new-programming-language-for-hhvm/) |
| 210 | CLU | Swift | named source of ideas (no feature given) | dotted | design |  | documented | documented | S1 | [Lattner, C. (n.d.). Chris Lattner's Homepage. nondot.org.](https://nondot.org/sabre/) |
| 211 | Objective-C | Swift | named parameters, ARC, Obj-C interop | solid | design |  | documented | documented | S1 | [Swift.org (n.d.). About Swift. swift.org.](https://www.swift.org/about/) |
| 212 | Perl | Swift | string processing model | dotted | design | Swift 4 | documented | documented | S1 | [Lattner, C., interviewed by Arment, M., Liss, C., & Siracusa, J. (2017). ATP Episode 205: Chris Lattner Interview Transcript. Accidental Tech Podcast.](https://atp.fm/205-chris-lattner-interview-transcript) |
| 213 | Haskell | Swift | protocols akin to type classes | dotted | type |  | documented | documented | S1 | [Lattner, C., interviewed by Arment, M., Liss, C., & Siracusa, J. (2017). ATP Episode 205: Chris Lattner Interview Transcript. Accidental Tech Podcast.](https://atp.fm/205-chris-lattner-interview-transcript) |
| 214 | Python | Swift | approachability, script-like top level | dotted | design |  | documented | documented | S1 | [Lattner, C. (n.d.). Chris Lattner's Homepage. nondot.org.](https://nondot.org/sabre/) |
| 215 | Ruby | Swift | named source of ideas (no feature given) | dotted | design |  | documented | documented | S1 | [Lattner, C. (n.d.). Chris Lattner's Homepage. nondot.org.](https://nondot.org/sabre/) |
| 216 | C# | Swift | named source of ideas (no feature given) | dotted | design |  | documented | documented | S1 | [Lattner, C. (n.d.). Chris Lattner's Homepage. nondot.org.](https://nondot.org/sabre/) |
| 217 | Rust | Swift | opt-in ownership model | dotted | design | Swift 5.9 | documented | documented | S1 | [Lattner, C. (2016, July 29). Looking back on Swift 3 and ahead to Swift 4. swift-evolution (Swift Forums).](https://forums.swift.org/t/looking-back-on-swift-3-and-ahead-to-swift-4/3610) |
| 218 | C | Zig | a more pragmatic C (Kelley) | solid | design |  | indirect support only | not stated in the quoted sentence | P1 | [Kelley, A. (2016). Introduction to the Zig Programming Language. andrewkelley.me (8 February 2016).](https://andrewkelley.me/post/intro-to-zig.html) |

## Using the map

| Do this | What happens |
|---|---|
| Hover a language | Its ancestors and successors are highlighted and the rest of the map fades (when nothing is selected). |
| Click a language | It is selected: the highlighting stays and its card opens on the right. Click it again to deselect. |
| Ctrl-click a language (⌘-click on a Mac) | It is added to the selection, or removed if it was already selected. |
| Click **None / Direct / 2nd degree / All** for Ancestors or Successors | Sets how far the highlighting follows the chain in that direction. |
| Untick **weaker or partial influence** in the key | Hides the dotted links, and the highlighting then follows solid links only. Tick it to show them again. |
| Hover or select a language | The labels of its dotted links appear; they are hidden otherwise to keep the map readable. |
| Click a family, health or outlook category | Picks out the languages in that category. Choices in one row add up; choices in different rows narrow down. |
| Hover a flag | Shows the designers' names. |
| Hover a health or outlook badge | Shows the reasoning and, for outlooks, the confidence. |
| Click a language name inside a card | Selects that language. |
| Click **source** in a card | Opens the cited source for that link in a new tab. |
| Click **Hide panel** | Folds the card away and keeps the selection; a **Show panel** button brings it back. |
| Click **Close**, press Esc, or click an empty part of the chart | Clears the selected languages and closes the card. |
| Click **Reset selection** | Clears the category filters. |

## Related work and credits

Éric Lévénez's *Computer Languages History* chart; the O'Reilly *History of Programming Languages* poster (2004); Ramiro Gómez's *Programming Languages Influence Network*; Peter Gleeson's Wikipedia-based influence graph (freeCodeCamp, 2017); the ACM HOPL conference papers. Flags: flag-icons (MIT). Logos: Simple Icons (CC0 icon data; marks belong to their owners). The map, the sourcing and this note were built with Claude (Anthropic) and reviewed by Gemini 3.1 Pro and ChatGPT 6.1 Sol; the author directed the work and decided each disputed point.
