# Programming Language Lineage: method and link list

*Version of 6 October 2026 · 82 languages · 129 influence links (110 solid, 19 dotted)*

## Goal

This project maps how programming languages descend from one another, so the history of programming can be read as a family tree and analysed as a network. Each language is a node placed at the year it first appeared; each influence is a directed link from an earlier language to a later one. Treating the result as a graph makes it possible to ask network questions such as which languages are roots, which act as brokers between generations, and how far an idea travelled (see *Graph analysis* below).

## How a link is determined

- **A link records a major, documented influence** of an earlier language on a later one: a design idea, syntax, semantics or runtime that the later language took on. The label on each link names *what* was passed on.
- **Sources:** the links were compiled with Claude (an AI assistant) from what designers have said about their own languages (language FAQs, design papers, official documentation, interviews, the ACM History of Programming Languages papers) and widely accepted histories. They are not yet individually cited; this list exists so each link can be checked. Influences that are merely plausible, or that only affect a library or tool around the language, are left out unless they are well known.
- **Solid line:** a direct, substantial influence on the language's design.
- **Dotted line:** a weaker, indirect or aesthetic influence, for example a naming or marketing choice (Java → JavaScript), an idea that arrived through a library rather than the language (R → Python via pandas), or a shared creator rather than shared design (Swift → Mojo).
- **Not overcrowding the chart:** only the most important influences per language are drawn, typically one to four. Minor borrowings (a single function name, a comment syntax) were removed after review. Most languages have more ancestors than shown.
- **Direction is by influence, not strictly by date.** In rare cases a later language influenced a newer version of an older one (CoffeeScript → JavaScript's 2015 features).

## Which languages are included

The map covers the major general-purpose languages and their key ancestors, plus languages that matter for data work. Because the map's author is a data scientist, it deliberately includes **statistics and data-processing languages** that general histories often skip: S, R, SAS, SPSS, Stata, MATLAB, Julia, SQL and its spin-offs (T-SQL, PL/SQL, MDX, Cypher, KQL, LookML), and the Microsoft BI languages (Excel formulas, DAX, Power Query M). A few languages are included for their uniqueness rather than their descendants (Forth, TeX).

## Health today and outlook to 2046

Both categories are **expert judgements made in October 2026**, not outputs of a statistical model. They were informed by public indicators (TIOBE index, July–September 2026; GitHub Octoverse 2025; Stack Overflow developer surveys), by whether the language is still maintained and used for new projects, and by the strength of its main platforms.

**Health today**

| Category | Meaning | Count |
|---|---|---|
| 🔥 Thriving | Top-tier usage across many domains, with growth or very large communities. | 12 |
| 🌿 Alive | Actively maintained, with a real community and new projects in its niches. | 38 |
| 🪫 Dying | Still runs important legacy systems or survives in a small niche, but little new work starts in it. | 18 |
| 💀 Dead | No meaningful current use; survives through its influence on other languages. | 14 |

**Outlook to 2046** (given only to alive and thriving languages)

The outlook assumes AI systems keep writing a growing share of the world's code. Five factors were weighed: (1) whether a strict type system or compiler can check AI-written code; (2) how much public code exists for AI models to learn from; (3) the health of the platforms it depends on (Apple, Android, .NET, Power BI, SAP and so on); (4) how entrenched it is in its power centres; and (5) whether a successor is replacing it.

| Category | Meaning | Count |
|---|---|---|
| 🐂 Bullish | Expected to gain share of new code by 2046. | 15 |
| ⚓ Steady | Expected to keep its main power centres thanks to entrenched use, even if it gains little new ground. | 18 |
| 🐻 Bearish | Expected to lose share of new code, though it may still run widely. | 17 |

## Graph analysis

Four standard network measures were computed on the full graph (dotted links count half in PageRank): **direct influence** (number of outgoing links), **reach** (number of descendants through any chain), **betweenness centrality** (how often a language lies on the shortest path between two others, marking brokers between generations) and **PageRank run against the arrows** (a language scores highly if it influenced languages that were themselves influential). The ranking below averages each language's rank on the four measures.

| # | Language | Year | Direct | Reach | Betweenness rank | PageRank rank |
|---|---|---|---|---|---|---|
| 1 | C | 1972 | 9 | 26 | 7 | 4 |
| 2 | ALGOL | 1960 | 4 | 40 | 9 | 2 |
| 3 | Smalltalk | 1972 | 4 | 16 | 5 | 10 |
| 4 | C++ | 1985 | 4 | 15 | 4 | 12 |
| 5 | Simula | 1967 | 3 | 22 | 13 | 8 |
| 6 | Fortran | 1957 | 5 | 48 | 43 | 1 |
| 7 | Lisp | 1958 | 7 | 33 | 44 | 3 |
| 8 | ML | 1973 | 3 | 19 | 25 | 7 |
| 9 | Pascal | 1970 | 2 | 17 | 16 | 9 |
| 10 | Python | 1991 | 6 | 9 | 1 | 22 |
| 11 | Haskell | 1990 | 4 | 13 | 15 | 14 |
| 12 | Java | 1995 | 6 | 8 | 6 | 16 |
| 13 | SQL | 1974 | 9 | 18 | 49 | 6 |
| 14 | BCPL | 1967 | 1 | 27 | 20 | 5 |
| 15 | Bourne sh | 1979 | 4 | 12 | 23 | 17 |

Caveats: the network reflects curated major influences, older languages have had more time to gather descendants, and languages with no links (Forth, SPSS, TeX) score zero by construction.

## Languages and their influences

Alphabetical. *Influenced by* lists the languages with a link into this one; (dotted) marks a weak or aesthetic link. *Reason* gives what each one contributed, in the same order.

| Language | Year | Family | Influenced by | Reason | Health today | Outlook 2046 |
|---|---|---|---|---|---|---|
| **ABAP** | 1983 | Data & BI | COBOL | COBOL: verbose business syntax | 🌿 Alive | ⚓ Steady |
| **ABC** | 1987 | Scripting & web | — | No parent drawn on the map | 💀 Dead | — |
| **Ada** | 1980 | C & systems | — | No parent drawn on the map | 🌿 Alive | ⚓ Steady |
| **ALGOL** | 1960 | C & systems | Fortran | Fortran: algebraic notation | 💀 Dead | — |
| **APL** | 1966 | Arrays & statistics | — | No parent drawn on the map | 🪫 Dying | — |
| **AWK** | 1977 | Scripting & web | SNOBOL<br>C | SNOBOL: associative arrays<br>C: C-like syntax | 🌿 Alive | ⚓ Steady |
| **Bash** | 1989 | Scripting & web | Bourne sh | Bourne sh: Bourne Again | 🔥 Thriving | 🐂 Bullish |
| **BASIC** | 1964 | Teaching & visual | Fortran | Fortran: statements, numeric focus | 💀 Dead | — |
| **BCPL** | 1967 | C & systems | ALGOL | ALGOL: via CPL | 💀 Dead | — |
| **Bourne sh** | 1979 | Scripting & web | ALGOL | ALGOL: ALGOL 68-style syntax | 🌿 Alive | ⚓ Steady |
| **C** | 1972 | C & systems | BCPL | BCPL: braces, via B | 🔥 Thriving | ⚓ Steady |
| **C#** | 2000 | JVM & .NET | C++<br>Eiffel (dotted)<br>Delphi<br>Java | C++: syntax, operator overloading<br>Eiffel: contracts, generics<br>Delphi: properties, events (Hejlsberg)<br>Java: Microsoft's answer | 🔥 Thriving | 🐂 Bullish |
| **C++** | 1985 | C & systems | Simula<br>C<br>Ada | Simula: classes, virtual functions<br>C: C plus classes<br>Ada: templates, exceptions | 🔥 Thriving | ⚓ Steady |
| **Clojure** | 2007 | Lisp | Lisp<br>Java | Lisp: a Lisp, again<br>Java: hosted on the JVM | 🪫 Dying | — |
| **CLU** | 1974 | Other lineages | — | No parent drawn on the map | 💀 Dead | — |
| **COBOL** | 1959 | Other lineages | — | No parent drawn on the map | 🪫 Dying | — |
| **CoffeeScript** | 2009 | Scripting & web | Python (dotted)<br>Ruby | Python: indentation, readability<br>Ruby: Ruby- and Python-style syntax | 🪫 Dying | — |
| **Cypher** | 2011 | Data & BI | SQL | SQL: declarative keywords | 🌿 Alive | 🐂 Bullish |
| **Dart** | 2011 | Scripting & web | JavaScript<br>Java | JavaScript: meant to replace it<br>Java: class syntax | 🌿 Alive | 🐻 Bearish |
| **DAX** | 2009 | Data & BI | SQL (dotted)<br>Excel formulas<br>MDX (dotted) | SQL: table & filter thinking<br>Excel formulas: formula syntax<br>MDX: same Analysis Services team | 🌿 Alive | 🐂 Bullish |
| **Delphi** | 1995 | Teaching & visual | Pascal<br>Visual Basic (dotted) | Pascal: Object Pascal<br>Visual Basic: Borland's answer | 🌿 Alive | 🐻 Bearish |
| **Eiffel** | 1986 | Other lineages | Simula | Simula: classes, inheritance | 🪫 Dying | — |
| **Elixir** | 2012 | Other lineages | Erlang<br>Ruby<br>F# (dotted) | Erlang: runs on the BEAM<br>Ruby: syntax<br>F#: pipe operator |> | 🌿 Alive | 🐻 Bearish |
| **Erlang** | 1986 | Other lineages | Prolog | Prolog: syntax, 1st version | 🌿 Alive | ⚓ Steady |
| **Excel formulas** | 1985 | Data & BI | Haskell | Haskell: LAMBDA (Simon Peyton Jones) | 🔥 Thriving | 🐂 Bullish |
| **F#** | 2005 | ML & Haskell | OCaml | OCaml: OCaml for .NET | 🌿 Alive | 🐻 Bearish |
| **Forth** | 1970 | Other lineages | — | No parent drawn on the map | 🪫 Dying | — |
| **Fortran** | 1957 | Arrays & statistics | — | No parent drawn on the map | 🌿 Alive | ⚓ Steady |
| **Go** | 2009 | C & systems | C<br>Oberon | C: basic syntax<br>Oberon: declarations, packages | 🔥 Thriving | 🐂 Bullish |
| **Hack** | 2014 | Scripting & web | PHP | PHP: PHP plus gradual typing | 🌿 Alive | 🐻 Bearish |
| **Haskell** | 1990 | ML & Haskell | ML<br>Miranda | ML: Hindley-Milner types<br>Miranda: lazy, pure (open rewrite) | 🌿 Alive | 🐻 Bearish |
| **Icon** | 1977 | Other lineages | SNOBOL | SNOBOL: string scanning (same designer) | 💀 Dead | — |
| **Java** | 1995 | JVM & .NET | Smalltalk<br>C++ | Smalltalk: objects, VM, GC<br>C++: syntax, minus pointers | 🔥 Thriving | ⚓ Steady |
| **JavaScript** | 1995 | Scripting & web | Scheme<br>Self<br>Python (dotted)<br>Java (dotted)<br>CoffeeScript | Scheme: first-class functions<br>Self: prototypes<br>Python: generators and iterators<br>Java: syntax, by marketing mandate<br>CoffeeScript: arrow functions, classes (ES2015) | 🔥 Thriving | 🐻 Bearish |
| **Julia** | 2012 | Arrays & statistics | Lisp<br>MATLAB<br>Python (dotted)<br>R (dotted) | Lisp: macros, multiple dispatch<br>MATLAB: syntax, end blocks<br>Python: general-purpose ease (2012 manifesto)<br>R: statistics (2012 manifesto) | 🌿 Alive | 🐻 Bearish |
| **Kotlin** | 2011 | JVM & .NET | Java<br>Scala | Java: 100% interop<br>Scala: concise syntax, val/var | 🌿 Alive | 🐂 Bullish |
| **KQL** | 2014 | Data & BI | SQL<br>Bourne sh (dotted) | SQL: tabular queries<br>Bourne sh: pipe-style syntax | 🌿 Alive | 🐂 Bullish |
| **Lisp** | 1958 | Lisp | — | No parent drawn on the map | 🪫 Dying | — |
| **Logo** | 1967 | Teaching & visual | Lisp | Lisp: Lisp without parentheses | 💀 Dead | — |
| **LookML** | 2012 | Data & BI | SQL | SQL: generates SQL | 🌿 Alive | ⚓ Steady |
| **Lua** | 1993 | Scripting & web | Scheme | Scheme: closures, first-class functions | 🌿 Alive | 🐂 Bullish |
| **Mathematica** | 1988 | Arrays & statistics | Lisp<br>APL | Lisp: symbolic expressions<br>APL: whole-array operations | 🌿 Alive | ⚓ Steady |
| **MATLAB** | 1984 | Arrays & statistics | Fortran | Fortran: front-end to Fortran libs | 🌿 Alive | 🐻 Bearish |
| **MDX** | 1997 | Data & BI | SQL | SQL: SELECT syntax for cubes | 🪫 Dying | — |
| **Miranda** | 1985 | ML & Haskell | — | No parent drawn on the map | 💀 Dead | — |
| **ML** | 1973 | ML & Haskell | Lisp | Lisp: functional core | 🪫 Dying | — |
| **Modula-2** | 1978 | C & systems | Pascal | Pascal: modules | 🪫 Dying | — |
| **Modula-3** | 1989 | C & systems | Modula-2 | Modula-2: safety, objects | 💀 Dead | — |
| **Mojo** | 2023 | C & systems | Python<br>Swift (dotted)<br>Rust | Python: Python superset<br>Swift: same creator (Chris Lattner)<br>Rust: ownership model | 🌿 Alive | 🐻 Bearish |
| **Oberon** | 1987 | C & systems | Modula-2 | Modula-2: simplified successor | 💀 Dead | — |
| **Objective-C** | 1984 | C & systems | C<br>Smalltalk | C: C plus messages<br>Smalltalk: message passing | 🪫 Dying | — |
| **OCaml** | 1996 | ML & Haskell | ML | ML: dialect + objects | 🌿 Alive | 🐻 Bearish |
| **Pascal** | 1970 | C & systems | COBOL (dotted)<br>ALGOL | COBOL: record types (via Hoare)<br>ALGOL: structured programming | 🪫 Dying | — |
| **Perl** | 1987 | Scripting & web | C<br>AWK<br>Bourne sh | C: C-like syntax<br>AWK: text patterns<br>Bourne sh: shell scripting style | 🪫 Dying | — |
| **PHP** | 1995 | Scripting & web | C<br>Perl | C: C-like syntax, function names<br>Perl: syntax, $ variables | 🌿 Alive | ⚓ Steady |
| **PL/I** | 1964 | C & systems | Fortran<br>COBOL | Fortran: the scientific half<br>COBOL: the business half | 🪫 Dying | — |
| **PL/SQL** | 1988 | Data & BI | SQL<br>Ada | SQL: procedural extensions<br>Ada: block syntax, packages, exceptions | 🌿 Alive | ⚓ Steady |
| **Power Query M** | 2013 | Data & BI | F# (dotted) | F#: functional, F#-like | 🌿 Alive | ⚓ Steady |
| **PowerShell** | 2006 | Scripting & web | Bourne sh<br>C# | Bourne sh: pipelines, but of objects<br>C#: .NET objects, C#-like syntax | 🌿 Alive | ⚓ Steady |
| **Prolog** | 1972 | Other lineages | — | No parent drawn on the map | 🪫 Dying | — |
| **Python** | 1991 | Scripting & web | C<br>SQL (dotted)<br>Icon<br>C++<br>ABC<br>Modula-3<br>Haskell<br>R (dotted) | C: operators, C extension API<br>SQL: joins, group-by (via pandas)<br>Icon: generators (yield)<br>C++: class mechanism (with Modula-3)<br>ABC: indentation, built-in types<br>Modula-3: modules, exceptions, classes<br>Haskell: list comprehensions<br>R: data frames (via pandas) | 🔥 Thriving | 🐂 Bullish |
| **R** | 1993 | Arrays & statistics | SQL (dotted)<br>Scheme<br>S<br>F# | SQL: dplyr verbs (select, filter, group_by)<br>Scheme: closures, lexical scope<br>S: syntax, data structures<br>F#: pipe |> (magrittr 2014, R 4.1) | 🌿 Alive | ⚓ Steady |
| **Ruby** | 1995 | Scripting & web | Smalltalk<br>CLU<br>Eiffel<br>Perl | Smalltalk: blocks, all objects<br>CLU: iterators, yield<br>Eiffel: clean object model<br>Perl: regex, scripting | 🌿 Alive | 🐻 Bearish |
| **Rust** | 2015 | C & systems | C++<br>Haskell<br>OCaml | C++: zero-cost abstractions<br>Haskell: traits from type classes<br>OCaml: enums, match, 1st compiler | 🔥 Thriving | 🐂 Bullish |
| **S** | 1976 | Arrays & statistics | Fortran<br>APL | Fortran: front-end to Fortran routines<br>APL: whole-array operations | 💀 Dead | — |
| **SAS** | 1972 | Arrays & statistics | PL/I | PL/I: statement syntax | 🌿 Alive | 🐻 Bearish |
| **Scala** | 2004 | JVM & .NET | ML<br>Haskell<br>Python (dotted)<br>Java | ML: pattern matching<br>Haskell: type classes<br>Python: Scala 3 optional braces<br>Java: JVM + libraries | 🌿 Alive | 🐻 Bearish |
| **Scheme** | 1975 | Lisp | Lisp | Lisp: minimal dialect | 🪫 Dying | — |
| **Scratch** | 2007 | Teaching & visual | Logo | Logo: turtle, learning by tinkering | 🌿 Alive | 🐻 Bearish |
| **Self** | 1987 | Other lineages | Smalltalk | Smalltalk: a Smalltalk dialect | 💀 Dead | — |
| **Simula** | 1967 | Other lineages | ALGOL | ALGOL: ALGOL 60 superset | 💀 Dead | — |
| **Smalltalk** | 1972 | Other lineages | Lisp<br>Simula<br>Logo | Lisp: GC, live environment<br>Simula: classes & objects<br>Logo: learning by programming | 🪫 Dying | — |
| **SNOBOL** | 1962 | Other lineages | — | No parent drawn on the map | 💀 Dead | — |
| **SPSS** | 1968 | Arrays & statistics | — | No parent drawn on the map | 🌿 Alive | 🐻 Bearish |
| **SQL** | 1974 | Data & BI | — | No parent drawn on the map | 🔥 Thriving | 🐂 Bullish |
| **Stata** | 1985 | Arrays & statistics | C | C: Mata's C-like syntax | 🌿 Alive | 🐻 Bearish |
| **Swift** | 2014 | C & systems | Objective-C<br>Python (dotted)<br>Rust | Objective-C: replaced it at Apple<br>Python: readability ideas<br>Rust: safety ideas | 🌿 Alive | 🐂 Bullish |
| **T-SQL** | 1987 | Data & BI | SQL | SQL: procedural extensions | 🌿 Alive | ⚓ Steady |
| **TeX** | 1978 | Other lineages | — | No parent drawn on the map | 🌿 Alive | ⚓ Steady |
| **TypeScript** | 2012 | Scripting & web | JavaScript<br>C# | JavaScript: superset + types<br>C#: type-system style (Hejlsberg) | 🔥 Thriving | 🐂 Bullish |
| **Visual Basic** | 1991 | Teaching & visual | BASIC | BASIC: BASIC + visual forms | 🪫 Dying | — |
| **Zig** | 2016 | C & systems | C | C: a better C | 🌿 Alive | 🐂 Bullish |

## Notes for checking

- Years are first public release (Rust: version 1.0, 2015).
- Links labelled *via* name the intermediate language or library that carried the influence (for example ALGOL → C via BCPL and B).
- Interactive version: the published *Programming Language Lineage* page, where each language's card also explains its origin, strengths, weaknesses, uses and famous software.
