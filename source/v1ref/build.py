import json, math, html

# ---------- data ----------
# id, label, year, y, family, info
NODES = [
    ("fortran", "Fortran", 1957, 390, "array", "IBM, John Backus. The first widely used high-level language; still runs weather models and the math libraries under NumPy and R."),
    ("lisp", "Lisp", 1958, 140, "lisp", "MIT, John McCarthy. Code is data. Gave the world garbage collection, the REPL, lambda and map."),
    ("cobol", "COBOL", 1959, 1010, "other", "Grace Hopper's committee. English-like business language that still processes a large share of bank transactions."),
    ("algol", "ALGOL", 1960, 480, "c", "European-American committee (ALGOL 58/60/68). Block structure and the grammar notation nearly every later language inherited."),
    ("apl", "APL", 1966, 320, "array", "IBM, Kenneth Iverson. A math notation turned language; whole-array operations, read right to left."),
    ("pascal", "Pascal", 1970, 440, "c", "ETH Zurich, Niklaus Wirth. Built to teach structured programming; ancestor of Modula and Oberon."),
    ("forth", "Forth", 1970, 1010, "other", "Chuck Moore. Stack-based, postfix: 2 3 + . The 'German' language, verb last."),
    ("c", "C", 1972, 530, "c", "Bell Labs, Dennis Ritchie. Written to build Unix. The source of braces, semicolons and printf."),
    ("smalltalk", "Smalltalk", 1972, 640, "other", "Xerox PARC, Alan Kay. Everything is an object that receives messages; also pioneered the GUI."),
    ("prolog", "Prolog", 1972, 930, "other", "Marseille, Alain Colmerauer. Logic programming: you state facts and rules, it searches for answers."),
    ("ml", "ML", 1973, 205, "ml", "Edinburgh, Robin Milner. Built for a theorem prover. Type inference and pattern matching."),
    ("sql", "SQL", 1974, 1010, "data", "IBM, Chamberlin and Boyce. Describe the result, not the loop. Based on Codd's relational model."),
    ("scheme", "Scheme", 1975, 75, "lisp", "MIT, Sussman and Steele. A minimal Lisp; the internals R was built on."),
    ("s", "S", 1976, 320, "array", "Bell Labs, John Chambers. Interactive statistics language; R is its open-source successor."),
    ("matlab", "MATLAB", 1984, 390, "array", "Cleve Moler, then MathWorks. Started as an interactive front-end to Fortran linear-algebra libraries."),
    ("objc", "Objective-C", 1984, 605, "c", "Brad Cox. C plus Smalltalk-style messages; the language of NeXT, macOS and early iPhone apps."),
    ("cpp", "C++", 1985, 530, "c", "Bell Labs, Bjarne Stroustrup. C with classes; games, trading systems, browsers."),
    ("excel", "Excel formulas", 1985, 985, "data", "Microsoft. The world's most used programming language, arguably. Since 2020 it even has LAMBDA."),
    ("erlang", "Erlang", 1986, 930, "other", "Ericsson. Telecom-grade concurrency and fault tolerance; runs on the BEAM VM. WhatsApp's backend."),
    ("perl", "Perl", 1987, 800, "script", "Larry Wall. 'There's more than one way to do it.' Regex and text glue for the early web."),
    ("bash", "Bash", 1989, 720, "script", "GNU, Brian Fox. 'Bourne Again SHell'. Glues programs together; integer maths only."),
    ("haskell", "Haskell", 1990, 225, "ml", "A research committee. Pure and lazy, with type classes and monads. Pandoc is written in it."),
    ("python", "Python", 1991, 760, "script", "Guido van Rossum, CWI Amsterdam. Readable, batteries included; now the lingua franca of data."),
    ("r", "R", 1993, 320, "array", "Auckland, Ihaka and Gentleman. S on the outside, Scheme on the inside."),
    ("java", "Java", 1995, 570, "jvm", "Sun, James Gosling. Write once, run anywhere: bytecode on the JVM, garbage collected."),
    ("js", "JavaScript", 1995, 690, "script", "Netscape, Brendan Eich, written in 10 days. Scheme's ideas in Java's clothes."),
    ("ruby", "Ruby", 1995, 850, "script", "Japan, Yukihiro Matsumoto. Designed for programmer happiness; Ruby on Rails."),
    ("php", "PHP", 1995, 780, "script", "Rasmus Lerdorf. Started as personal home-page tools; now runs much of the web, WordPress included."),
    ("ocaml", "OCaml", 1996, 165, "ml", "INRIA, France. ML with objects. Jane Street runs on it; Rust's first compiler was written in it."),
    ("csharp", "C#", 2000, 640, "jvm", "Microsoft, Anders Hejlsberg. Java's rival on .NET's own VM, the CLR."),
    ("scala", "Scala", 2004, 490, "jvm", "EPFL Lausanne, Martin Odersky. Functional plus object-oriented on the JVM. Spark is written in it."),
    ("fsharp", "F#", 2005, 165, "ml", "Microsoft Research, Don Syme. OCaml's ideas on .NET."),
    ("clojure", "Clojure", 2007, 420, "lisp", "Rich Hickey. A modern, immutable-by-default Lisp hosted on the JVM."),
    ("dax", "DAX", 2009, 990, "data", "Microsoft (Power Pivot, then Power BI). Excel-style formulas evaluated in filter context."),
    ("go", "Go", 2009, 650, "c", "Google: Griesemer, Pike, Thompson. Deliberately small; goroutines and channels from Hoare's CSP."),
    ("dart", "Dart", 2011, 760, "script", "Google Aarhus, Lars Bak. Meant to replace JavaScript; found its role in Flutter (and AngularDart)."),
    ("kotlin", "Kotlin", 2011, 560, "jvm", "JetBrains. A pragmatic, null-safe 'better Java'; Android's preferred language since 2019."),
    ("julia", "Julia", 2012, 360, "array", "MIT. As easy as R, as fast as C. Multiple dispatch; strong in scientific computing."),
    ("ts", "TypeScript", 2012, 690, "script", "Microsoft, Anders Hejlsberg. JavaScript plus types; powers Angular."),
    ("elixir", "Elixir", 2012, 880, "other", "José Valim. Ruby-like syntax on Erlang's BEAM VM."),
    ("m", "Power Query M", 2013, 1040, "data", "Microsoft. Functional, lazy, case-sensitive language behind Power Query's Applied Steps."),
    ("swift", "Swift", 2014, 605, "c", "Apple, Chris Lattner (also LLVM's creator). Replaced Objective-C; safe by default."),
    ("rust", "Rust", 2015, 480, "c", "Graydon Hoare, started in Vancouver in 2006; Mozilla sponsored it from 2009. Memory safety without a garbage collector, checked by the borrow checker."),
    # added: major influences not discussed in the chat
    ("simula", "Simula", 1967, 600, "other", "Norwegian Computing Center, Ole-Johan Dahl and Kristen Nygaard. The first object-oriented language: classes, objects, inheritance."),
    ("bcpl", "BCPL", 1967, 505, "c", "Cambridge, Martin Richards. A stripped-down CPL that became B and then C. 'hello, world' first appeared in a tutorial for its descendant B."),
    ("clu", "CLU", 1974, 965, "other", "MIT, Barbara Liskov. Data abstraction, iterators with yield, multiple return values. Liskov won the 2008 Turing Award."),
    ("awk", "AWK", 1977, 805, "script", "Bell Labs: Aho, Weinberger, Kernighan (the name is their initials). Pattern-action text processing on the command line."),
    ("sh", "Bourne sh", 1979, 740, "script", "Bell Labs, Stephen Bourne. The Unix shell that Bash re-implements; its keywords came from ALGOL 68."),
    ("ada", "Ada", 1980, 570, "c", "CII Honeywell Bull for the US Department of Defense, led by Jean Ichbiah. Strong typing, generics, exceptions; still used in avionics."),
    ("miranda", "Miranda", 1985, 275, "ml", "University of Kent, David Turner. Lazy and pure; Haskell was created partly because Miranda was proprietary."),
    ("abc", "ABC", 1987, 865, "script", "CWI Amsterdam: Geurts, Meertens, Pemberton. A teaching language; Guido van Rossum worked on it before creating Python."),
    ("self", "Self", 1987, 665, "other", "Xerox PARC and Stanford, David Ungar and Randall Smith. Objects without classes (prototypes); its fast VM techniques later fed Java's HotSpot."),
    ("oberon", "Oberon", 1987, 470, "c", "ETH Zurich, Niklaus Wirth and Jürg Gutknecht. Successor of Pascal and Modula-2; Robert Griesemer did his PhD on it before co-creating Go."),
    # added in round 3
    ("basic", "BASIC", 1964, 1095, "edu", "Dartmouth College, John Kemeny and Thomas Kurtz. Made for students; Microsoft's first product was a BASIC interpreter."),
    ("logo", "Logo", 1967, 1180, "edu", "BBN and MIT: Wally Feurzeig, Seymour Papert, Cynthia Solomon. 'Lisp without parentheses' for children, with the drawing turtle."),
    ("vb", "Visual Basic", 1991, 1095, "edu", "Microsoft, after Alan Cooper's prototype. Drag buttons onto a form, then write BASIC behind them; lives on as VBA in Office."),
    ("delphi", "Delphi", 1995, 1050, "edu", "Borland, chief architect Anders Hejlsberg. Visual Object Pascal: Visual Basic's ease with compiled speed."),
    ("lua", "Lua", 1993, 1140, "script", "PUC-Rio, Brazil: Ierusalimschy, de Figueiredo, Celes. Tiny and embeddable; scripting in games, Roblox and Neovim."),
    ("scratch", "Scratch", 2007, 1180, "edu", "MIT Media Lab, Mitchel Resnick's group. Programming by snapping blocks together; first built in Squeak Smalltalk."),
    ("zig", "Zig", 2016, 420, "c", "Andrew Kelley. A simpler, safer replacement for C with no hidden control flow. The Bun JavaScript runtime is written in it."),
    ("mojo", "Mojo", 2023, 820, "c", "Modular, Chris Lattner (Swift, LLVM). A Python superset that compiles to fast code for AI hardware."),
    # added in round 4
    ("pli", "PL/I", 1964, 440, "c", "IBM, led by George Radin. Meant to merge Fortran's science and COBOL's business data in one language; Multics was written in it."),
    ("spss", "SPSS", 1968, 255, "array", "Stanford: Norman Nie, Dale Bent, Hadlai Hull. Command syntax for social-science statistics; owned by IBM since 2009."),
    ("sas", "SAS", 1972, 270, "array", "North Carolina State University: Anthony Barr, James Goodnight, John Sall, Jane Helwig. DATA steps and PROCs; the standard in pharma for decades."),
    ("stata", "Stata", 1985, 355, "array", "William Gould, later StataCorp in Texas. Do-files, ado-files and the Mata matrix language; the default in applied economics."),
    ("abap", "ABAP", 1983, 1150, "data", "SAP, Walldorf. The language of SAP's business systems; reads a lot like COBOL."),
    ("modula3", "Modula-3", 1989, 422, "c", "DEC Systems Research Center and Olivetti Research. A safer, object-oriented successor of Modula-2; Python took its module, exception and class design from it."),
    ("hack", "Hack", 2014, 722, "script", "Meta (Facebook). PHP with gradual static typing, running on Meta's HHVM engine."),
    ("powershell", "PowerShell", 2006, 775, "script", "Microsoft, Jeffrey Snover. A shell where commands pass .NET objects to each other instead of plain text."),
    ("coffee", "CoffeeScript", 2009, 840, "script", "Jeremy Ashkenas. A cleaner syntax that compiles to JavaScript; much of it was later adopted by JavaScript itself."),
    ("mathematica", "Mathematica", 1988, 95, "array", "Wolfram Research, Stephen Wolfram. The Wolfram Language: symbolic maths, notebooks and built-in knowledge."),
    ("tex", "TeX", 1978, 1010, "other", "Stanford, Donald Knuth. A typesetting system that is also a full programming language; LaTeX is built on it."),
    ("modula2", "Modula-2", 1978, 440, "c", "ETH Zurich, Niklaus Wirth. Pascal plus modules, designed for the Lilith workstation."),
    ("eiffel", "Eiffel", 1986, 760, "other", "Interactive Software Engineering, Bertrand Meyer. Object-oriented with 'design by contract': routines declare what they require and guarantee."),
    ("icon", "Icon", 1977, 870, "other", "University of Arizona, Ralph Griswold. Goal-directed evaluation and generators; successor of SNOBOL."),
    ("snobol", "SNOBOL", 1962, 580, "other", "Bell Labs: Farber, Griswold, Polonsky. A language built around pattern matching on text."),
    ("tsql", "T-SQL", 1987, 1240, "data", "Sybase, later Microsoft. Procedural extensions to SQL for SQL Server."),
    ("plsql", "PL/SQL", 1988, 1290, "data", "Oracle. Procedural SQL with Ada-style syntax."),
    ("mdx", "MDX", 1997, 1240, "data", "Microsoft. Queries for multidimensional OLAP cubes."),
    ("cypher", "Cypher", 2011, 1240, "data", "Neo4j. Pattern-based queries for graph databases."),
    ("lookml", "LookML", 2012, 1290, "data", "Looker. A semantic modelling language that generates SQL."),
    ("kql", "KQL", 2014, 1240, "data", "Microsoft. Pipe-style queries over logs and telemetry."),
]


# status now (late 2026): dead / dying / alive / thriving; outlook to ~2046 assuming AI: bull / bear (alive and thriving only)
STATUS = {
 "fortran": ("alive", "steady", "Weather, climate and physics codes and the maths libraries under NumPy and R keep it in use."),
 "lisp": ("dying", None, "Common Lisp survives in niches; its ideas live on in almost everything."),
 "cobol": ("dying", None, "Billions of lines still run banks and governments; almost nothing new is written."),
 "algol": ("dead", None, "Not used since the 1970s, but its block structure is in nearly every language."),
 "apl": ("dying", None, "A small, devoted niche (Dyalog); its descendants k and q run trading systems."),
 "pascal": ("dying", None, "Free Pascal keeps it going; it mostly lives on as Delphi."),
 "forth": ("dying", None, "Embedded hobby niche; its idea survives in PostScript."),
 "c": ("thriving", "steady", "Operating systems, databases and embedded devices will run on C for decades; new security-critical code moves to Rust."),
 "smalltalk": ("dying", None, "Pharo and Squeak keep it alive for enthusiasts."),
 "prolog": ("dying", None, "Research and teaching niche."),
 "ml": ("dying", None, "Standard ML is mostly a teaching language now; OCaml and F# carry the line."),
 "sql": ("thriving", "bull", "AI writes more SQL than ever, and declarative queries are easy to check."),
 "scheme": ("dying", None, "Racket and Guile keep it alive, mainly in teaching."),
 "s": ("dead", None, "Replaced by R; S-PLUS is discontinued."),
 "matlab": ("alive", "bear", "Losing ground to Python in universities and industry."),
 "objc": ("dying", None, "Maintained in older Apple code; Swift has taken over."),
 "cpp": ("thriving", "steady", "Game engines (Unreal), browsers, trading and ML runtimes stay C++; Rust takes some new systems work."),
 "excel": ("thriving", "bull", "Copilot writes formulas for people who never could; usage keeps growing."),
 "erlang": ("alive", "steady", "The BEAM runtime keeps telecom and messaging systems (WhatsApp) running; Elixir draws the newcomers."),
 "perl": ("dying", None, "Still glues old servers together; new scripting goes to Python."),
 "bash": ("thriving", "bull", "AI agents live in terminals and run shell commands constantly."),
 "haskell": ("alive", "bear", "Influential and loved, but small; AI tools have little Haskell to learn from."),
 "python": ("thriving", "bull", "The language AI is built in, and the one models write most."),
 "r": ("alive", "steady", "Academic statistics, survey methodology, biostatistics and pharma keep R strong; general data work tilts to Python."),
 "java": ("thriving", "steady", "A huge enterprise and Android base that will keep running for decades; new JVM work leans to Kotlin."),
 "js": ("thriving", "bear", "Still what every browser runs, but new code is written in TypeScript."),
 "ruby": ("alive", "bear", "Rails keeps it alive (GitHub, Shopify); new projects choose TypeScript or Python."),
 "php": ("alive", "steady", "WordPress alone runs a large share of the web; little momentum for new projects."),
 "ocaml": ("alive", "bear", "Finance and compiler niche (Jane Street)."),
 "csharp": ("thriving", "bull", "Typed, fast, backed by Microsoft and Unity; a good fit for AI-written code."),
 "scala": ("alive", "bear", "Spark keeps it relevant, but data teams moved to PySpark and SQL."),
 "fsharp": ("alive", "bear", "Small, loyal .NET niche."),
 "clojure": ("dying", None, "Loyal users, shrinking community."),
 "dax": ("alive", "bull", "Power BI and Fabric keep growing, and Copilot writes DAX."),
 "go": ("thriving", "bull", "Runs the cloud; plain code is easy to review when AI writes it."),
 "dart": ("alive", "bear", "Tied to Flutter's fortunes and to Google's commitment."),
 "kotlin": ("alive", "bull", "Android's default, and Kotlin Multiplatform reaches iOS and servers."),
 "julia": ("alive", "bear", "Strong in science, but AI tools default to Python."),
 "ts": ("thriving", "bull", "GitHub's most used language since 2025; types make AI-written code safer."),
 "elixir": ("alive", "bear", "Loved niche; small training corpus for AI tools."),
 "m": ("alive", "steady", "Lives as long as Power Query in Excel and Power BI, even if people increasingly click or prompt rather than type it."),
 "swift": ("alive", "bull", "Apple's future; rising on TIOBE."),
 "rust": ("thriving", "bull", "The memory-safety push plus a compiler that checks AI-written code."),
 "simula": ("dead", None, "Unused, but every class you write descends from it."),
 "bcpl": ("dead", None, "Museum piece; lives on through C."),
 "clu": ("dead", None, "Research language; its iterators are everywhere."),
 "awk": ("alive", "steady", "Still on every Unix machine for one-liners."),
 "sh": ("alive", "steady", "Lives on as POSIX sh, the shell every script can count on."),
 "ada": ("alive", "steady", "Avionics, rail and defence certify on Ada; Rust is entering the same safety niche."),
 "miranda": ("dead", None, "Superseded by Haskell."),
 "abc": ("dead", None, "Superseded by Python."),
 "self": ("dead", None, "Research language; lives on in JavaScript and in JVM speed tricks."),
 "oberon": ("dead", None, "Academic; lives on through Go."),
 "basic": ("dead", None, "Line-numbered classic BASIC is gone; its heirs are VB and VBA."),
 "logo": ("dead", None, "Replaced by Scratch in classrooms."),
 "vb": ("dying", None, "VB6 is long gone and VB.NET frozen since 2020; VBA lingers in Office."),
 "delphi": ("alive", "bear", "Top 15 on TIOBE thanks to long-lived business apps; few new projects."),
 "lua": ("alive", "bull", "Roblox, games and Neovim; tiny and easy to embed."),
 "scratch": ("alive", "bear", "How millions of children start coding; AI tutors may change that."),
 "zig": ("alive", "bull", "A simpler 'better C' with growing adoption; Bun is written in it."),
 "mojo": ("alive", "bear", "Built for the AI era, but too little code exists for AI models to learn it well."),
 "hack": ("alive", "bear", "Used almost only inside Meta and a few companies such as Slack."),
 "powershell": ("alive", "steady", "Windows and Azure administration depend on it."),
 "coffee": ("dying", None, "Its best ideas were absorbed into JavaScript itself in 2015."),
 "mathematica": ("alive", "steady", "Entrenched in physics and maths research; AI assistants compete for casual use."),
 "tex": ("alive", "steady", "Still how mathematics and physics are typeset; Overleaf keeps it current."),
 "modula2": ("dying", None, "A GCC front end keeps it compilable; mostly historical."),
 "eiffel": ("dying", None, "A small commercial niche; its ideas live on in other languages."),
 "icon": ("dead", None, "Research language; its generators live on in Python."),
 "snobol": ("dead", None, "Its text pattern matching lives on in AWK, Perl and regular expressions."),
 "tsql": ("alive", "steady", "SQL Server, Azure SQL and Fabric keep it essential."),
 "plsql": ("alive", "steady", "Oracle systems in banks and governments will run for decades."),
 "mdx": ("dying", None, "Replaced by tabular models and DAX; legacy cubes remain."),
 "cypher": ("alive", "bull", "Graph databases and knowledge graphs for AI are growing, and GQL made it a standard."),
 "lookml": ("alive", "steady", "Semantic layers that feed governed metrics to AI tools keep it relevant."),
 "kql": ("alive", "bull", "Security and observability data keep growing, and Copilot writes KQL."),
 "modula3": ("dead", None, "Academic; lives on through Python."),
 "pli": ("dying", None, "Still runs on IBM mainframes; nothing new is written in it."),
 "spss": ("alive", "bear", "Point-and-click users in social science and market research; syntax users drift to R and Python."),
 "sas": ("alive", "bear", "Entrenched in pharma and banking, but the FDA now accepts R and licences are expensive."),
 "stata": ("alive", "bear", "Still the default in applied economics; slowly losing students to R and Python."),
 "abap": ("alive", "steady", "Runs SAP systems worldwide, and SAP keeps it alive as ABAP Cloud."),
}

# where it was developed (right flag), then designers' birth countries (left flags, shown when different)
FLAGS = {
    "fortran": ("us", []), "lisp": ("us", []), "cobol": ("us", []), "algol": ("intl", []),
    "apl": ("us", ["ca"]), "pascal": ("ch", []), "forth": ("us", []), "c": ("us", []),
    "smalltalk": ("us", []), "prolog": ("fr", []), "ml": ("gb", []), "sql": ("us", []),
    "scheme": ("us", []), "s": ("us", ["ca"]), "matlab": ("us", []), "objc": ("us", []),
    "cpp": ("us", ["dk"]), "excel": ("us", []), "erlang": ("se", ["gb"]), "perl": ("us", []),
    "bash": ("us", []), "haskell": ("intl", []), "python": ("nl", []), "r": ("nz", ["ca"]),
    "java": ("us", ["ca"]), "js": ("us", []), "ruby": ("jp", []), "php": ("ca", ["gl"]),
    "ocaml": ("fr", []), "csharp": ("us", ["dk"]), "scala": ("ch", ["de"]), "fsharp": ("gb", ["au"]),
    "clojure": ("us", []), "dax": ("us", []), "go": ("us", ["ch", "ca"]), "dart": ("dk", []),
    "kotlin": ("ru", []), "julia": ("us", ["in"]), "ts": ("us", ["dk"]), "elixir": ("br", []),
    "m": ("us", []), "swift": ("us", []), "rust": ("ca", []),
    "simula": ("no", []), "bcpl": ("gb", []), "clu": ("us", []), "awk": ("us", ["ca"]),
    "sh": ("us", ["gb"]), "ada": ("fr", []), "miranda": ("gb", []), "abc": ("nl", ["gb"]),
    "self": ("us", []), "oberon": ("ch", []),
    "basic": ("us", ["hu"]), "logo": ("us", ["za"]), "vb": ("us", []), "delphi": ("us", ["dk"]),
    "lua": ("br", []), "scratch": ("us", []), "zig": ("us", []), "mojo": ("us", []),
    "modula3": ("us", ["it"]), "hack": ("us", ["fr"]), "powershell": ("us", []), "coffee": ("us", []), "mathematica": ("us", ["gb"]), "tex": ("us", []), "modula2": ("ch", []), "eiffel": ("us", ["fr"]), "icon": ("us", []), "snobol": ("us", []), "tsql": ("us", []), "plsql": ("us", []), "mdx": ("us", []), "cypher": ("se", []), "lookml": ("us", []), "kql": ("il", []), "pli": ("us", []), "spss": ("us", []), "sas": ("us", []), "stata": ("us", []), "abap": ("de", []),
}
COUNTRY = {"us": "United States", "gb": "United Kingdom", "fr": "France", "ch": "Switzerland", "de": "Germany",
           "dk": "Denmark", "nl": "Netherlands", "jp": "Japan", "ca": "Canada", "nz": "New Zealand", "se": "Sweden",
           "au": "Australia", "br": "Brazil", "in": "India", "ru": "Russia", "gl": "Greenland", "no": "Norway",
           "hu": "Hungary", "it": "Italy", "il": "Israel", "za": "South Africa", "intl": "International committee"}

# from, to, label, style ('s' solid, 'd' dashed)
EDGES = [
    ("lisp", "scheme", "minimal dialect", "s"),
    ("lisp", "clojure", "a Lisp, again", "s"),
    ("java", "clojure", "hosted on the JVM", "s"),
    ("lisp", "ml", "functional core", "s"),
    ("lisp", "smalltalk", "GC, live environment", "s"),
    ("lisp", "julia", "macros, multiple dispatch", "s"),
    ("scheme", "r", "closures, lexical scope", "s"),
    ("scheme", "js", "first-class functions", "s"),
    ("apl", "s", "whole-array operations", "s"),
    ("s", "r", "syntax, data structures", "s"),
    ("fortran", "matlab", "front-end to Fortran libs", "s"),
    ("matlab", "julia", "syntax, end blocks", "s"),
    ("fortran", "algol", "algebraic notation", "s"),
    ("algol", "bcpl", "via CPL", "s"),
    ("bcpl", "c", "braces, via B", "s"),
    ("algol", "simula", "ALGOL 60 superset", "s"),
    ("simula", "smalltalk", "classes & objects", "s"),
    ("simula", "cpp", "classes, virtual functions", "s"),
    ("algol", "pascal", "structured programming", "s"),
    ("algol", "sh", "ALGOL 68-style syntax", "s"),
    ("sh", "bash", "Bourne Again", "s"),
    ("sh", "perl", "shell scripting style", "s"),
    ("awk", "perl", "text patterns", "s"),
    ("oberon", "go", "declarations, packages", "s"),
    ("pascal", "delphi", "Object Pascal", "s"),
    ("delphi", "csharp", "properties, events (Hejlsberg)", "s"),
    ("basic", "vb", "BASIC + visual forms", "s"),
    ("vb", "delphi", "Borland's answer", "d"),
    ("lisp", "logo", "Lisp without parentheses", "s"),
    ("logo", "smalltalk", "learning by programming", "s"),
    ("logo", "scratch", "turtle, learning by tinkering", "s"),
    ("c", "zig", "a better C", "s"),
    ("python", "scala", "Scala 3 optional braces", "d"),
    ("python", "coffee", "indentation, readability", "d"),
    ("python", "julia", "general-purpose ease (2012 manifesto)", "d"),
    ("r", "julia", "statistics (2012 manifesto)", "d"),
    ("python", "swift", "readability ideas", "d"),
    ("python", "js", "generators and iterators", "d"),
    ("cpp", "python", "class mechanism (with Modula-3)", "s"),
    ("cpp", "csharp", "syntax, operator overloading", "s"),
    ("c", "awk", "C-like syntax", "s"),
    ("c", "php", "C-like syntax, function names", "s"),
    ("fsharp", "r", "pipe |> (magrittr 2014, R 4.1)", "s"),
    ("fsharp", "elixir", "pipe operator |>", "d"),
    ("sql", "r", "dplyr verbs (select, filter, group_by)", "d"),
    ("sql", "python", "joins, group-by (via pandas)", "d"),
    ("sql", "tsql", "procedural extensions", "s"),
    ("sql", "plsql", "procedural extensions", "s"),
    ("ada", "plsql", "block syntax, packages, exceptions", "s"),
    ("sql", "mdx", "SELECT syntax for cubes", "s"),
    ("mdx", "dax", "same Analysis Services team", "d"),
    ("sql", "cypher", "declarative keywords", "s"),
    ("sql", "lookml", "generates SQL", "s"),
    ("sql", "kql", "tabular queries", "s"),
    ("sh", "kql", "pipe-style syntax", "d"),
    ("haskell", "excel", "LAMBDA (Simon Peyton Jones)", "s"),
    ("swift", "mojo", "same creator (Chris Lattner)", "d"),
    ("php", "hack", "PHP plus gradual typing", "s"),
    ("sh", "powershell", "pipelines, but of objects", "s"),
    ("csharp", "powershell", ".NET objects, C#-like syntax", "s"),
    ("ruby", "coffee", "Ruby- and Python-style syntax", "s"),
    ("coffee", "js", "arrow functions, classes (ES2015)", "s"),
    ("lisp", "mathematica", "symbolic expressions", "s"),
    ("apl", "mathematica", "whole-array operations", "s"),
    ("pascal", "modula2", "modules", "s"),
    ("modula2", "oberon", "simplified successor", "s"),
    ("modula2", "modula3", "safety, objects", "s"),
    ("simula", "eiffel", "classes, inheritance", "s"),
    ("eiffel", "ruby", "clean object model", "s"),
    ("eiffel", "csharp", "contracts, generics", "d"),
    ("snobol", "icon", "string scanning (same designer)", "s"),
    ("icon", "python", "generators (yield)", "s"),
    ("snobol", "awk", "associative arrays", "s"),
    ("c", "perl", "C-like syntax", "s"),
    ("modula3", "python", "modules, exceptions, classes", "s"),
    ("r", "python", "data frames (via pandas)", "d"),
    ("fsharp", "m", "functional, F#-like", "d"),
    ("scheme", "lua", "closures, first-class functions", "s"),
    ("fortran", "basic", "statements, numeric focus", "s"),
    ("fortran", "s", "front-end to Fortran routines", "s"),
    ("fortran", "pli", "the scientific half", "s"),
    ("cobol", "pli", "the business half", "s"),
    ("pli", "sas", "statement syntax", "s"),
    ("cobol", "abap", "verbose business syntax", "s"),
    ("cobol", "pascal", "record types (via Hoare)", "d"),
    ("c", "stata", "Mata's C-like syntax", "s"),
    ("python", "mojo", "Python superset", "s"),
    ("rust", "mojo", "ownership model", "s"),
    ("c", "cpp", "C plus classes", "s"),
    ("c", "objc", "C plus messages", "s"),
    ("smalltalk", "objc", "message passing", "s"),
    ("cpp", "java", "syntax, minus pointers", "s"),
    ("smalltalk", "java", "objects, VM, GC", "s"),
    ("c", "go", "basic syntax", "s"),
    ("c", "python", "operators, C extension API", "s"),
    ("java", "csharp", "Microsoft's answer", "s"),
    ("java", "scala", "JVM + libraries", "s"),
    ("ml", "scala", "pattern matching", "s"),
    ("haskell", "scala", "type classes", "s"),
    ("java", "kotlin", "100% interop", "s"),
    ("scala", "kotlin", "concise syntax, val/var", "s"),
    ("cpp", "rust", "zero-cost abstractions", "s"),
    ("ocaml", "rust", "enums, match, 1st compiler", "s"),
    ("haskell", "rust", "traits from type classes", "s"),
    ("objc", "swift", "replaced it at Apple", "s"),
    ("rust", "swift", "safety ideas", "s"),
    ("ml", "haskell", "Hindley-Milner types", "s"),
    ("miranda", "haskell", "lazy, pure (open rewrite)", "s"),
    ("ml", "ocaml", "dialect + objects", "s"),
    ("ocaml", "fsharp", "OCaml for .NET", "s"),
    ("haskell", "python", "list comprehensions", "s"),
    ("abc", "python", "indentation, built-in types", "s"),
    ("clu", "ruby", "iterators, yield", "s"),
    ("ada", "cpp", "templates, exceptions", "s"),
    ("smalltalk", "self", "a Smalltalk dialect", "s"),
    ("self", "js", "prototypes", "s"),
    ("perl", "ruby", "regex, scripting", "s"),
    ("smalltalk", "ruby", "blocks, all objects", "s"),
    ("perl", "php", "syntax, $ variables", "s"),
    ("ruby", "elixir", "syntax", "s"),
    ("erlang", "elixir", "runs on the BEAM", "s"),
    ("prolog", "erlang", "syntax, 1st version", "s"),
    ("java", "js", "syntax, by marketing mandate", "d"),
    ("js", "ts", "superset + types", "s"),
    ("csharp", "ts", "type-system style (Hejlsberg)", "s"),
    ("js", "dart", "meant to replace it", "s"),
    ("java", "dart", "class syntax", "s"),
    ("sql", "dax", "table & filter thinking", "d"),
    ("excel", "dax", "formula syntax", "s"),
]

FAMILIES = [
    ("lisp", "Lisp"),
    ("ml", "ML & Haskell"),
    ("array", "Arrays & statistics"),
    ("c", "C & systems"),
    ("jvm", "JVM & .NET"),
    ("script", "Scripting & web"),
    ("data", "Data & BI"),
    ("edu", "Teaching & visual"),
    ("other", "Other lineages"),
]
YOURS = {"r", "python", "sql", "dax", "m", "bash", "stata", "spss", "tex"}
SWISS = {"pascal", "scala"}


# main inventors: (name, birth country or None). Three or more = "collective" in the hover text.
INVENTORS = {
 "fortran": [("John Backus", "us")], "lisp": [("John McCarthy", "us")],
 "cobol": [("Grace Hopper", "us"), ("Jean Sammet", "us"), ("the CODASYL committee", None)],
 "algol": [("Backus", "us"), ("Naur", "dk"), ("Bauer", "de"), ("van Wijngaarden", "nl")],
 "apl": [("Kenneth Iverson", "ca")], "pascal": [("Niklaus Wirth", "ch")], "forth": [("Chuck Moore", "us")],
 "c": [("Dennis Ritchie", "us")], "smalltalk": [("Alan Kay", "us")], "prolog": [("Alain Colmerauer", "fr")],
 "ml": [("Robin Milner", "gb")], "sql": [("Donald Chamberlin", "us"), ("Raymond Boyce", "us")],
 "scheme": [("Gerald Sussman", "us"), ("Guy Steele", "us")], "s": [("John Chambers", "ca")],
 "matlab": [("Cleve Moler", "us")], "objc": [("Brad Cox", "us"), ("Tom Love", "us")],
 "cpp": [("Bjarne Stroustrup", "dk")], "excel": [("Microsoft team", None), ("", None), ("", None)],
 "erlang": [("Joe Armstrong", "gb"), ("Robert Virding", "se"), ("Mike Williams", "gb")],
 "perl": [("Larry Wall", "us")], "bash": [("Brian Fox", "us")], "haskell": [("committee", None), ("", None), ("", None)],
 "python": [("Guido van Rossum", "nl")], "r": [("Ross Ihaka", "nz"), ("Robert Gentleman", "ca")],
 "java": [("James Gosling", "ca")], "js": [("Brendan Eich", "us")], "ruby": [("Yukihiro Matsumoto", "jp")],
 "php": [("Rasmus Lerdorf", "gl")], "ocaml": [("Xavier Leroy", "fr")], "csharp": [("Anders Hejlsberg", "dk")],
 "scala": [("Martin Odersky", "de")], "fsharp": [("Don Syme", "au")], "clojure": [("Rich Hickey", "us")],
 "dax": [("Microsoft team", None), ("", None), ("", None)],
 "go": [("Robert Griesemer", "ch"), ("Rob Pike", "ca"), ("Ken Thompson", "us")],
 "dart": [("Lars Bak", "dk"), ("Kasper Lund", "dk")], "kotlin": [("Andrey Breslav", None)],
 "julia": [("Jeff Bezanson", "us"), ("Stefan Karpinski", "us"), ("Viral Shah", "in"), ("Alan Edelman", "us")],
 "ts": [("Anders Hejlsberg", "dk")], "elixir": [("José Valim", "br")], "m": [("Microsoft team", None), ("", None), ("", None)],
 "swift": [("Chris Lattner", "us")], "rust": [("Graydon Hoare", "ca")],
 "simula": [("Ole-Johan Dahl", "no"), ("Kristen Nygaard", "no")], "bcpl": [("Martin Richards", "gb")],
 "clu": [("Barbara Liskov", "us")], "awk": [("Alfred Aho", "ca"), ("Peter Weinberger", "us"), ("Brian Kernighan", "ca")],
 "sh": [("Stephen Bourne", "gb")], "ada": [("Jean Ichbiah", "fr")], "miranda": [("David Turner", "gb")],
 "abc": [("Leo Geurts", "nl"), ("Lambert Meertens", "nl"), ("Steven Pemberton", "gb")],
 "self": [("David Ungar", "us"), ("Randall Smith", "us")], "oberon": [("Niklaus Wirth", "ch"), ("Jürg Gutknecht", "ch")],
 "basic": [("John Kemeny", "hu"), ("Thomas Kurtz", "us")],
 "logo": [("Wally Feurzeig", "us"), ("Seymour Papert", "za"), ("Cynthia Solomon", "us")],
 "vb": [("Alan Cooper", "us")], "delphi": [("Anders Hejlsberg", "dk")],
 "lua": [("Roberto Ierusalimschy", "br"), ("Luiz Henrique de Figueiredo", "br"), ("Waldemar Celes", "br")],
 "scratch": [("Mitchel Resnick", "us")], "zig": [("Andrew Kelley", "us")], "mojo": [("Chris Lattner", "us")],
 "hack": [("Julien Verlaguet", "fr"), ("Alok Menghrajani", None), ("Drew Paroski", None)],
 "powershell": [("Jeffrey Snover", "us")], "coffee": [("Jeremy Ashkenas", "us")], "mathematica": [("Stephen Wolfram", "gb")],
 "tex": [("Donald Knuth", "us")], "modula2": [("Niklaus Wirth", "ch")], "eiffel": [("Bertrand Meyer", "fr")],
 "icon": [("Ralph Griswold", "us")], "snobol": [("David Farber", "us"), ("Ralph Griswold", "us"), ("Ivan Polonsky", None)],
 "tsql": [("Sybase team", None), ("", None), ("", None)], "plsql": [("Oracle team", None), ("", None), ("", None)],
 "mdx": [("Mosha Pasumansky", None)], "cypher": [("Andrés Taylor", None)], "lookml": [("Lloyd Tabb", "us")],
 "kql": [("Microsoft Israel team", None), ("", None), ("", None)],
 "modula3": [("Luca Cardelli", "it"), ("Greg Nelson", "us"), ("Bill Kalsow", None), ("Jim Donahue", None), ("Mick Jordan", None)],
 "pli": [("George Radin", "us")],
 "spss": [("Norman Nie", "us"), ("Dale Bent", None), ("Hadlai Hull", None)],
 "sas": [("Anthony Barr", "us"), ("James Goodnight", "us"), ("John Sall", "us"), ("Jane Helwig", "us")],
 "stata": [("William Gould", "us")], "abap": [("SAP team", None), ("", None), ("", None)],
}
def who(nid):
    inv = INVENTORS[nid]
    if len(inv) >= 3:
        return "Inventors: collective"
    parts = [f"{n} ({COUNTRY[c]})" if c else n for n, c in inv]
    return ("Inventor: " if len(parts) == 1 else "Inventors: ") + " and ".join(parts)
def born_names(nid, cc):
    names = [n for n, c in INVENTORS[nid] if c == cc and n]
    return (" and ".join(names) + f", born in {COUNTRY[cc]}") if names else f"Designer born in {COUNTRY[cc]}"


# organisation at the time of invention
ORG = {
 "fortran": "IBM", "lisp": "MIT", "cobol": "CODASYL committee, sponsored by the US Department of Defense",
 "algol": "International committee (meetings in Zurich 1958 and Paris 1960)", "apl": "Harvard, then IBM",
 "pascal": "ETH Zurich", "forth": "National Radio Astronomy Observatory", "c": "Bell Labs (AT&T)",
 "smalltalk": "Xerox PARC", "prolog": "University of Aix-Marseille", "ml": "University of Edinburgh",
 "sql": "IBM San Jose Research Laboratory", "scheme": "MIT", "s": "Bell Labs (AT&T)",
 "matlab": "University of New Mexico, then MathWorks", "objc": "Productivity Products International (Stepstone)",
 "cpp": "Bell Labs (AT&T)", "excel": "Microsoft", "erlang": "Ericsson", "perl": "Unisys",
 "bash": "GNU Project (Free Software Foundation)", "haskell": "Academic committee (Glasgow, Yale and others)",
 "python": "CWI, Amsterdam", "r": "University of Auckland", "java": "Sun Microsystems", "js": "Netscape",
 "ruby": "Independent project", "php": "University of Toronto", "ocaml": "INRIA", "csharp": "Microsoft",
 "scala": "EPFL", "fsharp": "Microsoft Research Cambridge", "clojure": "Independent project", "dax": "Microsoft",
 "go": "Google", "dart": "Google (Aarhus office)", "kotlin": "JetBrains (St Petersburg team)", "julia": "MIT",
 "ts": "Microsoft", "elixir": "Plataformatec, São Paulo", "m": "Microsoft", "swift": "Apple",
 "rust": "Personal project, then Mozilla Research", "simula": "Norwegian Computing Center",
 "bcpl": "University of Cambridge", "clu": "MIT", "awk": "Bell Labs (AT&T)", "sh": "Bell Labs (AT&T)",
 "ada": "CII Honeywell Bull, for the US Department of Defense", "miranda": "University of Kent",
 "abc": "CWI, Amsterdam", "self": "Xerox PARC and Stanford", "oberon": "ETH Zurich", "basic": "Dartmouth College",
 "logo": "BBN and MIT", "vb": "Microsoft", "delphi": "Borland", "lua": "Tecgraf, PUC-Rio (for Petrobras)",
 "scratch": "MIT Media Lab", "zig": "Independent, now the Zig Software Foundation", "mojo": "Modular",
 "modula3": "DEC Systems Research Center and Olivetti Research",
 "tsql": "Sybase, later Microsoft SQL Server", "plsql": "Oracle", "mdx": "Microsoft (OLAP Services, later Analysis Services)",
 "cypher": "Neo4j (Neo Technology), founded in Malmö", "lookml": "Looker, Santa Cruz (Google Cloud since 2020)", "kql": "Microsoft Israel R&D Center",
 "hack": "Meta (Facebook)", "powershell": "Microsoft", "coffee": "Independent project (DocumentCloud)",
 "mathematica": "Wolfram Research", "tex": "Stanford University", "modula2": "ETH Zurich",
 "eiffel": "Interactive Software Engineering, Santa Barbara", "icon": "University of Arizona", "snobol": "Bell Labs (AT&T)", "pli": "IBM", "spss": "Stanford University, then SPSS Inc.", "sas": "North Carolina State University, then SAS Institute",
 "stata": "Computing Resource Center (now StataCorp)", "abap": "SAP",
}
# famous software written (mostly) in each language
SOFTWARE = {
 "fortran": [("BLAS and LAPACK", "the reference linear-algebra libraries that NumPy, R and MATLAB ultimately call"), ("WRF", "the Weather Research and Forecasting model used by forecasters worldwide"), ("ECMWF IFS", "the European Centre's global forecast model, among the most accurate in the world"), ("Parts of SciPy", "optimisation and special-function routines wrapped for Python")],
 "lisp": [("Emacs", "the editor is largely written in, and extended with, Emacs Lisp"), ("ITA's QPX", "the airfare search engine behind Orbitz and later Google Flights"), ("Reddit (2005)", "the first version, before a rewrite in Python"), ("Grammarly", "its core grammar engine runs on Common Lisp")],
 "cobol": [("Core banking ledgers", "account and transaction processing at many of the world's banks"), ("US unemployment systems", "state benefit systems that buckled under demand in 2020")],
 "algol": [("Burroughs B5000 MCP", "an operating system written in an ALGOL dialect, unusual in 1961")],
 "pascal": [("TeX", "Knuth wrote it in WEB, a literate-programming form of Pascal"), ("Apple Lisa and early Mac apps", "Apple's 1980s application code was mostly Pascal")],
 "forth": [("Open Firmware", "boot firmware of Sun workstations and PowerPC Macs, with a Forth prompt")],
 "c": [("Linux kernel", "runs Android, most servers and nearly all supercomputers"), ("Unix", "C was created to rewrite it"), ("Git", "Linus Torvalds's version-control system"), ("SQLite", "the most widely deployed database, inside every phone"), ("CPython", "the standard Python interpreter"), ("PostgreSQL", "the leading open-source relational database"), ("Redis", "in-memory data store used for caching")],
 "smalltalk": [("Squeak and Pharo", "live environments where everything can be edited while it runs"), ("JPMorgan Kapital", "a derivatives risk system built in the 1990s")],
 "prolog": [("IBM Watson", "used Prolog to parse questions when it won Jeopardy! in 2011"), ("NASA Clarissa", "voice-operated procedure assistant on the International Space Station")],
 "ml": [("Isabelle and HOL", "theorem provers used to verify mathematics and hardware")],
 "sql": [("dbt pipelines", "analytics transformations written as SQL models"), ("Stored procedures", "business logic inside banking and ERP databases")],
 "scheme": [("GNU Guix", "a package manager and Linux distribution configured in Guile Scheme"), ("DrRacket", "teaching environment used in many introductory courses")],
 "s": [("S-PLUS", "the commercial S system, popular in the 1990s before R took over")],
 "matlab": [("Simulink models", "control-system designs that generate code for cars and aircraft")],
 "objc": [("WorldWideWeb", "Tim Berners-Lee's first web browser, written on a NeXT computer"), ("Cocoa and early iPhone apps", "Apple's frameworks and the first App Store generation")],
 "cpp": [("Google Chrome", "the browser and its V8 JavaScript engine"), ("Unreal Engine", "the engine behind Fortnite and many big-budget games"), ("Adobe Photoshop", "the standard image editor"), ("Microsoft Office", "large parts of Word and Excel"), ("MySQL", "open-source database behind much of the early web"), ("PyTorch and TensorFlow cores", "the fast engines under the Python interfaces")],
 "excel": [("Financial models", "budgets, forecasts and valuations in almost every company")],
 "erlang": [("WhatsApp backend", "served hundreds of millions of users with a small team"), ("RabbitMQ", "widely used message broker"), ("Ericsson AXD301", "telecom switch famous for 'nine nines' reliability")],
 "perl": [("IMDb", "the movie database ran on Perl in its early years"), ("Booking.com", "one of the largest Perl codebases in the world"), ("Bugzilla", "Mozilla's bug tracker")],
 "bash": [("makepkg", "Arch Linux's package-building tool"), ("Build, deploy and CI scripts", "the glue of almost every software team")],
 "haskell": [("Pandoc", "document converter behind R Markdown and Quarto"), ("Meta's Sigma", "rule engine that fights spam and abuse"), ("ShellCheck", "finds bugs in shell scripts")],
 "python": [("Instagram", "one of the largest Django deployments in the world"), ("Dropbox desktop client", "where Guido van Rossum worked from 2013 to 2019"), ("YouTube", "originally written mostly in Python"), ("PyTorch", "the leading deep-learning framework, Python on top of C++"), ("Reddit", "rewritten from Lisp to Python in 2005")],
 "r": [("ggplot2 and the tidyverse", "Hadley Wickham's grammar of graphics and data tools"), ("Shiny", "interactive web apps written in R"), ("Bioconductor", "genomics and bioinformatics packages"), ("BBC News graphics", "the BBC data team's bbplot style")],
 "java": [("Minecraft: Java Edition", "the original version of the best-selling game"), ("Apache Hadoop", "the open-source big-data platform of the 2010s"), ("Elasticsearch", "search engine behind many site searches and log tools"), ("IntelliJ IDEA", "JetBrains' IDE, where Kotlin was born"), ("Jenkins", "continuous-integration server")],
 "js": [("Website front-ends", "every interactive web page runs JavaScript"), ("Node.js servers", "JavaScript on the server since 2009"), ("Google Maps (2005)", "showed what AJAX web apps could do")],
 "ruby": [("GitHub", "built on Ruby on Rails"), ("Shopify", "one of the largest Rails applications"), ("Homebrew", "the Mac package manager"), ("Basecamp", "the app Rails was extracted from")],
 "php": [("WordPress", "powers a large share of all websites"), ("MediaWiki", "the software behind Wikipedia"), ("Facebook (originally)", "later moved to Hack")],
 "ocaml": [("Jane Street trading systems", "a trading firm that runs almost entirely on OCaml"), ("Rust's first compiler", "used until Rust could compile itself"), ("Flow and Hack type checkers", "Meta's tools for JavaScript and Hack"), ("Coq/Rocq", "proof assistant used to verify mathematics and compilers")],
 "csharp": [("Unity games", "including Hollow Knight and Pokémon Go"), ("Stack Overflow", "runs on .NET with famously few servers"), ("Roslyn", "the C# compiler, written in C#")],
 "scala": [("Apache Spark", "the engine under Databricks"), ("Apache Kafka", "event-streaming platform; its original broker was in Scala"), ("Akka", "toolkit for concurrent, distributed systems"), ("Twitter backend", "replaced Ruby on Rails around 2009 to 2011")],
 "fsharp": [("Jet.com pricing engine", "e-commerce pricing; Jet.com was later bought by Walmart")],
 "clojure": [("Nubank", "Brazil's digital bank, one of the largest Clojure users"), ("Datomic", "database built around immutable facts"), ("Metabase", "open-source BI tool")],
 "go": [("Docker", "packages software into containers"), ("Kubernetes", "runs containers across clusters; born at Google"), ("Terraform", "infrastructure as code"), ("Prometheus", "monitoring and alerting"), ("Hugo", "static website generator"), ("CockroachDB", "distributed SQL database")],
 "dart": [("Google Pay", "rewritten in Flutter"), ("Google Ads app", "Flutter mobile app"), ("BMW app", "Flutter app for car owners"), ("AngularDart apps", "Google's internal web front-ends, Ads and Merchant Center among them")],
 "kotlin": [("Android apps", "most new apps, Google's own included"), ("Gradle build scripts", "Kotlin DSL for builds"), ("JetBrains IDEs", "parts of IntelliJ and its plugins")],
 "julia": [("CliMA", "Caltech-led climate model"), ("Pumas", "drug-dosing models used in pharma"), ("NY Fed DSGE model", "the New York Fed's macroeconomic model")],
 "ts": [("Visual Studio Code", "Microsoft's open-source editor"), ("Angular", "Google's web framework"), ("Claude Code", "Anthropic's coding agent"), ("Slack desktop app", "Electron app written in TypeScript")],
 "elixir": [("Discord", "real-time messaging for millions of users"), ("Phoenix", "web framework with live-updating pages")],
 "swift": [("iPhone and Mac apps", "most new ones"), ("SwiftUI", "Apple's declarative UI framework")],
 "rust": [("Firefox Stylo", "parallel CSS engine"), ("Linux kernel drivers", "Rust was accepted into the kernel in 2022"), ("Polars", "fast DataFrame library for Python"), ("uv and Ruff", "Python package manager and linter"), ("Cloudflare Pingora", "proxy handling a large share of web traffic"), ("AWS Firecracker", "micro-VMs behind AWS Lambda")],
 "bcpl": [("Xerox Alto software", "the 1973 computer that pioneered the graphical interface"), ("MUD1", "the first multi-user dungeon game, rewritten in BCPL")],
 "sh": [("Unix startup scripts", "booted classic Unix systems")],
 "ada": [("Boeing 777", "flight-control software"), ("Paris Métro Line 14", "driverless train control"), ("Air-traffic control", "several European systems")],
 "oberon": [("Oberon OS", "a complete operating system written by two people at ETH")],
 "basic": [("Altair BASIC", "Microsoft's first product, 1975"), ("Home computers", "the built-in language of the C64, ZX Spectrum and Apple II")],
 "vb": [("VBA macros", "automation in Excel and Access"), ("Windows business apps", "countless 1990s in-house tools")],
 "delphi": [("Skype", "the original Windows client"), ("FL Studio", "music production software"), ("Total Commander", "two-pane file manager")],
 "lua": [("Roblox", "games written in Luau, a Lua dialect"), ("World of Warcraft add-ons", "player-written interface mods"), ("Neovim", "the editor's plugins and configuration"), ("Adobe Lightroom", "large parts of its interface logic")],
 "zig": [("Bun", "fast JavaScript runtime"), ("TigerBeetle", "financial-transactions database"), ("Ghostty", "terminal emulator")],
 "mojo": [("Modular MAX", "kernels in Modular's AI inference engine")],
 "pli": [("Multics", "the 1960s operating system that inspired Unix")],
 "sas": [("Clinical-trial analyses", "decades of drug-approval submissions to regulators")],
 "abap": [("SAP S/4HANA", "ERP software running finance and logistics at large companies")],
 "hack": [("Facebook backend", "the web tier of Facebook and Messenger"), ("Slack backend", "migrated from PHP to Hack")],
 "powershell": [("Windows Server and Azure automation", "how administrators script Microsoft's cloud and servers"), ("Microsoft 365 administration", "user, mailbox and licence management at scale")],
 "coffee": [("Atom", "GitHub's code editor, originally written in CoffeeScript"), ("Dropbox web front-end", "migrated to TypeScript in 2017")],
 "mathematica": [("Wolfram|Alpha", "the computational answer engine"), ("Mathematica notebooks", "the notebook format that inspired Jupyter")],
 "tex": [("LaTeX", "Leslie Lamport's macro package that most people actually use"), ("arXiv papers", "most mathematics and physics preprints"), ("The Art of Computer Programming", "Knuth created TeX to typeset it")],
 "tsql": [("SQL Server stored procedures", "business logic in countless Microsoft-based companies"), ("Fabric and Synapse warehouses", "Microsoft's cloud data warehouses")],
 "plsql": [("Oracle E-Business Suite", "Oracle's own ERP applications"), ("Oracle APEX apps", "low-code web apps that run inside the database")],
 "mdx": [("Analysis Services cubes", "multidimensional models behind Excel pivot tables")],
 "cypher": [("Neo4j applications", "fraud detection, recommendations and knowledge graphs")],
 "lookml": [("Looker models", "governed metric definitions behind Looker dashboards")],
 "kql": [("Azure Monitor and Log Analytics", "querying logs and telemetry"), ("Microsoft Sentinel", "threat hunting in security data")],
 "modula2": [("Lilith", "ETH's workstation, with its operating system written in Modula-2")],
}
# logos from Simple Icons (CC0 icon data; marks belong to their owners)
LOGO_SLUG = {"python": "python", "r": "r", "rust": "rust", "go": "go", "kotlin": "kotlin", "swift": "swift",
 "ts": "typescript", "js": "javascript", "java": "openjdk", "c": "c", "cpp": "cplusplus", "scala": "scala",
 "haskell": "haskell", "julia": "julia", "elixir": "elixir", "erlang": "erlang", "dart": "dart", "clojure": "clojure",
 "ocaml": "ocaml", "fsharp": "fsharp", "ruby": "ruby", "php": "php", "perl": "perl", "lua": "lua", "zig": "zig",
 "bash": "gnubash", "fortran": "fortran", "ada": "ada", "lisp": "commonlisp", "scratch": "scratch", "delphi": "delphi", "coffee": "coffeescript", "mathematica": "wolframmathematica", "cypher": "neo4j", "lookml": "looker"}
import json as _json, re as _re
_SI = {i["slug"]: i for i in _json.load(open("si/package/data/simple-icons.json"))}
def _logo(nid):
    slug = LOGO_SLUG.get(nid)
    if not slug: return None
    raw = open(f"si/package/icons/{slug}.svg").read()
    d = _re.search(r' d="([^"]+)"', raw).group(1)
    hx = _SI[slug]["hex"]
    r, g, b = (int(hx[i:i+2], 16) / 255 for i in (0, 2, 4))
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return {"d": d, "hex": None if lum < 0.22 else "#" + hx}

exec(open('desc.py').read())
# ---------- layout ----------
X0, PX = 80, 26.0
Y_OFF = 12
FONT_W = 7.6   # approx width per char at 13px mono
LBL_W = 5.7    # per char at 11px sans
H_NODE = 24

def xpos(year): return X0 + (year - 1955) * PX

nodes = {}
FW, FH, FGAP, PAD = 16, 12, 5, 8
for nid, label, year, y, fam, info in NODES:
    dev, born = FLAGS[nid]
    left = [b for b in born if b != dev]
    tw = len(label) * FONT_W
    w = PAD * 2 + tw + (len(left) + 1) * (FW + FGAP) - (3 if len(left) > 1 else 0) * 0
    nodes[nid] = dict(id=nid, label=label, year=year, x=xpos(year), y=y + Y_OFF, w=w, h=H_NODE, fam=fam, info=info,
                      dev=dev, left=left, tw=tw, st=STATUS[nid][0], ol=STATUS[nid][1], note=STATUS[nid][2])

W = int(max(n["x"] + n["w"] / 2 for n in nodes.values()) + 60)
H = int(max(n["y"] for n in nodes.values()) + 60)

def inside(px, py, n, pad=0):
    return abs(px - n["x"]) <= n["w"] / 2 + pad and abs(py - n["y"]) <= n["h"] / 2 + pad

def qpt(p0, p1, p2, t):
    a = (1 - t) ** 2; b = 2 * (1 - t) * t; c = t * t
    return (a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1])

def blossom(p0, p1, p2, s, t):
    a = (1 - s) * (1 - t); b = (1 - s) * t + s * (1 - t); c = s * t
    return (a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1])

# node overlap check
ids = list(nodes)
for i in range(len(ids)):
    for j in range(i + 1, len(ids)):
        a, b = nodes[ids[i]], nodes[ids[j]]
        if abs(a["x"] - b["x"]) < (a["w"] + b["w"]) / 2 + 6 and abs(a["y"] - b["y"]) < H_NODE + 8:
            print("NODE OVERLAP", ids[i], ids[j])

BENDS = [0.12, -0.12, 0.22, -0.22, 0.04, 0.32, -0.32, 0.42, -0.42]

edges = []
for f, t, lab, sty in EDGES:
    A, B = nodes[f], nodes[t]
    p0, p2 = (A["x"], A["y"]), (B["x"], B["y"])
    dx, dy = p2[0] - p0[0], p2[1] - p0[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    best = None
    for bend in BENDS:
        p1 = ((p0[0] + p2[0]) / 2 + nx * bend * L, (p0[1] + p2[1]) / 2 + ny * bend * L)
        hits = 0
        for k in range(1, 100):
            q = qpt(p0, p1, p2, k / 100)
            if q[1] > H - 26 or q[1] < 26 or q[0] < 10 or q[0] > W - 10: hits += 1
            for n in nodes.values():
                if n["id"] in (f, t): continue
                if inside(q[0], q[1], n, 4): hits += 1
        score = hits * 10 + abs(bend) * 3
        if best is None or score < best[0]:
            best = (score, bend, p1, hits)
    _, bend, p1, hits = best
    if hits: print("EDGE HITS NODE", f, t, hits)
    # trim to node borders
    t0 = 0.0
    while t0 < 0.5 and inside(*qpt(p0, p1, p2, t0), A, 3): t0 += 0.002
    t1 = 1.0
    while t1 > 0.5 and inside(*qpt(p0, p1, p2, t1), B, 5): t1 -= 0.002
    s0 = qpt(p0, p1, p2, t0); s2 = qpt(p0, p1, p2, t1); s1 = blossom(p0, p1, p2, t0, t1)
    edges.append(dict(f=f, t=t, lab=lab, sty=sty, p=(p0, p1, p2), seg=(s0, s1, s2), t0=t0, t1=t1))

# label placement
placed = []
def lbl_box(cx, cy, text):
    w = len(text) * LBL_W + 6
    return (cx - w / 2, cy - 8, cx + w / 2, cy + 6)

def box_hits(b):
    for n in nodes.values():
        if b[0] < n["x"] + n["w"] / 2 + 2 and b[2] > n["x"] - n["w"] / 2 - 2 and b[1] < n["y"] + n["h"] / 2 + 2 and b[3] > n["y"] - n["h"] / 2 - 2:
            return True
    for o in placed:
        if b[0] < o[2] and b[2] > o[0] and b[1] < o[3] and b[3] > o[1]:
            return True
    return False

TS = [0.5, 0.42, 0.58, 0.35, 0.65, 0.28, 0.72, 0.22, 0.78, 0.46, 0.54, 0.38, 0.62, 0.3, 0.7]
# place shorter edges first so they get their midpoints
order = sorted(range(len(edges)), key=lambda i: math.dist(edges[i]["p"][0], edges[i]["p"][2]))
for i in order:
    e = edges[i]
    p0, p1, p2 = e["p"]
    chosen = None
    for tt in TS:
        tt2 = e["t0"] + (e["t1"] - e["t0"]) * tt
        for off in (0, -9, 9):
            c = qpt(p0, p1, p2, tt2)
            b = lbl_box(c[0], c[1] + off + 4, e["lab"])
            if not box_hits(b):
                chosen = (c[0], c[1] + off + 4, b); break
        if chosen: break
    if not chosen:
        c = qpt(p0, p1, p2, (e["t0"] + e["t1"]) / 2)
        chosen = (c[0], c[1] + 4, lbl_box(c[0], c[1] + 4, e["lab"]))
        print("LABEL CLASH", e["f"], e["t"], e["lab"])
    placed.append(chosen[2])
    e["lx"], e["ly"] = chosen[0], chosen[1]
    if chosen[2][0] < 0 or chosen[2][2] > W: print("LABEL OUT", e["lab"])


import base64
INTL_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 480"><rect width="640" height="480" fill="#4b6fa8"/><g fill="none" stroke="#fff" stroke-width="30"><circle cx="320" cy="240" r="175"/><ellipse cx="320" cy="240" rx="72" ry="175"/><path d="M145 240h350"/></g></svg>'
def flag_uri(c):
    raw = INTL_SVG if c == "intl" else open(f"package/flags/4x3/{c}.svg").read()
    return "data:image/svg+xml;base64," + base64.b64encode(raw.encode()).decode()
used = sorted({c for d, b in FLAGS.values() for c in [d] + b})
FLAG_DEFS = "".join(
    f'<g id="flag-{c}"><image width="16" height="12" preserveAspectRatio="none" href="{flag_uri(c)}"/>'
    f'<rect class="flag-edge" x=".25" y=".25" width="15.5" height="11.5" rx="1.5"/></g>' for c in used)
EMO = 'class="emoji" x="8" y="12" text-anchor="middle"'
BADGES = {
 "st-dead": f'<text {EMO}>\U0001F480</text>',
 "st-dying": '<rect x="2.6" y="5" width="10" height="6" rx="1.3" class="bat"/><rect x="12.9" y="6.8" width="1.5" height="2.4" rx=".4" class="bat-tip"/><rect x="3.8" y="6.2" width="2.3" height="3.6" rx=".5" class="bat-low"/>',
 "st-alive": f'<text {EMO}>\U0001F33F</text>',
 "st-thriving": f'<text {EMO}>\U0001F525</text>',
 "ol-bull": '<path class="horn" d="M6.6 10.4C3.6 10.3 1.7 7.8 1.5 3.2 2.9 6 4.6 7.4 7.1 7.9Z"/><path class="horn" d="M9.4 10.4C12.4 10.3 14.3 7.8 14.5 3.2 13.1 6 11.4 7.4 8.9 7.9Z"/><ellipse class="bull-head" cx="8" cy="10.2" rx="2.5" ry="2.3"/>',
 "ol-bear": f'<text {EMO}>\U0001F43B</text>',
 "ol-steady": f'<text {EMO}>\u2693</text>',
}
FLAG_DEFS += "".join(f'<g id="{k}"><circle class="badge-bg" cx="8" cy="8" r="8"/>{v}</g>' for k, v in BADGES.items())

# ---------- svg ----------
def f1(v): return f"{v:.1f}"
out = []
out.append(f'<svg id="map" viewBox="0 0 {W} {H}" aria-label="Influence map of {len(nodes)} programming languages from 1957 to 2023. Arrows point from a language to the languages it influenced." xmlns="http://www.w3.org/2000/svg">')
out.append('<defs>'
           '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ah" d="M0 1 L10 5 L0 9 z"/></marker>'
           '<marker id="ah-hi" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ah-hi" d="M0 1 L10 5 L0 9 z"/></marker>'
           '<marker id="ah-root" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ah-root" d="M0 1 L10 5 L0 9 z"/></marker>'
           '<marker id="ah-leaf" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="ah-leaf" d="M0 1 L10 5 L0 9 z"/></marker>'
           + FLAG_DEFS + '</defs>')
# decade grid
out.append('<g class="grid">')
for yr in range(1960, 2021, 10):
    x = xpos(yr)
    out.append(f'<line x1="{f1(x)}" y1="22" x2="{f1(x)}" y2="{H - 8}"/>')
    out.append(f'<text class="tick" x="{f1(x)}" y="14" text-anchor="middle">{yr}s</text>')
out.append('</g>')
out.append('<g class="edges">')
for i, e in enumerate(edges):
    s0, s1, s2 = e["seg"]
    d = f"M{f1(s0[0])} {f1(s0[1])} Q{f1(s1[0])} {f1(s1[1])} {f1(s2[0])} {f1(s2[1])}"
    cls = "edge dashed" if e["sty"] == "d" else "edge"
    out.append(f'<path class="{cls}" data-e="{i}" data-f="{e["f"]}" data-t="{e["t"]}" d="{d}"/>')
out.append('</g><g class="labels">')
for i, e in enumerate(edges):
    out.append(f'<text class="elabel" data-e="{i}" data-f="{e["f"]}" data-t="{e["t"]}" x="{f1(e["lx"])}" y="{f1(e["ly"])}" text-anchor="middle">{html.escape(e["lab"])}</text>')
out.append('</g><g class="nodes">')
for n in nodes.values():
    x0 = n["x"] - n["w"] / 2; y0 = n["y"] - n["h"] / 2
    cls = f'node fam-{n["fam"]} st-{n["st"]}' + (f' ol-{n["ol"]}' if n["ol"] else "") + (" yours" if n["id"] in YOURS else "")
    out.append(f'<g class="{cls}" data-id="{n["id"]}" tabindex="0" role="button" aria-label="{html.escape(n["label"])}, {n["year"]}">')
    out.append(f'<rect x="{f1(x0)}" y="{f1(y0)}" width="{f1(n["w"])}" height="{n["h"]}" rx="12"/>')
    fy = n["y"] - FH / 2
    fx = x0 + PAD
    for b in n["left"]:
        out.append(f'<use href="#flag-{b}" x="{f1(fx)}" y="{f1(fy)}"><title>{html.escape(born_names(n["id"], b))}</title></use>')
        fx += FW + FGAP
    tx = fx + n["tw"] / 2
    out.append(f'<text x="{f1(tx)}" y="{f1(n["y"] + 4.5)}" text-anchor="middle">{html.escape(n["label"])}</text>')
    rx_ = x0 + n["w"] - PAD - FW
    out.append(f'<use href="#flag-{n["dev"]}" x="{f1(rx_)}" y="{f1(fy)}"><title>{html.escape("Built in " + COUNTRY[n["dev"]] + chr(10) + who(n["id"]))}</title></use>')
    out.append(f'<use class="badge" href="#st-{n["st"]}" x="{f1(x0)}" y="{f1(y0 - 9)}"><title>Status: {n["st"]}</title></use>')
    if n["ol"]:
        out.append(f'<use class="badge" href="#ol-{n["ol"]}" x="{f1(x0 + n["w"] - 16)}" y="{f1(y0 - 9)}"><title>20-year outlook: {dict(bull="bullish", bear="bearish", steady="steady")[n["ol"]]}</title></use>')
    out.append('</g>')
out.append('</g></svg>')
svg = "\n".join(out)

data = dict(
    nodes={n["id"]: dict(label=n["label"], year=n["year"], fam=n["fam"], info=n["info"], dev=n["dev"], left=n["left"], st=n["st"], ol=n["ol"], note=n["note"], who=who(n["id"]), inv=[[a, c] for a, c in INVENTORS[n["id"]] if a], org=ORG[n["id"]], desc=DESC[n["id"]], sw=[list(x) for x in SOFTWARE.get(n["id"], [])], logo=_logo(n["id"])) for n in nodes.values()},
    countries=COUNTRY,
    edges=[dict(f=e["f"], t=e["t"], lab=e["lab"], d=e["sty"] == "d") for e in edges],
    fams=dict(FAMILIES),
)

tpl = open("template.html").read()
def lkey(key, inner, label):
    return f'<button type="button" class="lkey" data-key="{key}" aria-pressed="false">{inner}{label}</button>'
def bmini(k): return f'<svg class="badge-mini" viewBox="0 0 16 16" aria-hidden="true"><use href="#{k}"/></svg>'
rows = [
    ("Family", "".join(lkey(f"fam-{k}", f'<span class="chip fam-{k}"></span>', v) for k, v in FAMILIES)),
    ("Health today", "".join(lkey(f"st-{k}", bmini(f"st-{k}"), v) for k, v in [("thriving", "Thriving"), ("alive", "Alive"), ("dying", "Dying"), ("dead", "Dead")])),
    ("Outlook to 2046", lkey("ol-bull", bmini("ol-bull"), "Bullish") + lkey("ol-steady", bmini("ol-steady"), "Steady") + lkey("ol-bear", bmini("ol-bear"), "Bearish")),
    ("Yours", lkey("yours", '<span class="key-ring"></span>', "Languages you work in")),
]
legend = "".join(f'<div class="lrow"><span class="lhead">{h}</span><div class="lkeys">{b}</div></div>' for h, b in rows)
page = tpl.replace("%%SVG%%", svg).replace("%%DATA%%", json.dumps(data)).replace("%%LEGEND%%", legend)
open("language-lineage.html", "w").write(page)
print("W,H", W, H, "nodes", len(nodes), "edges", len(edges))
