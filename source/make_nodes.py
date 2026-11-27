# Generates nodes.py from the v1 data in v1ref/build.py plus the changes made after AI review.
import os, pprint
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "us_spelling.py"), encoding="utf-8").read())   # us(): US spelling for our own text
src = open(os.path.join(HERE, "v1ref", "build.py")).read()
ns = {}
exec(src[:src.index("import json as _json")], ns)
NODES = [list(n) for n in ns["NODES"]]
FLAGS, COUNTRY, INVENTORS, ORG, SOFTWARE, LOGO_SLUG, FAMILIES = (ns[k] for k in ["FLAGS", "COUNTRY", "INVENTORS", "ORG", "SOFTWARE", "LOGO_SLUG", "FAMILIES"])
V1STATUS = ns["STATUS"]

REMOVED = {"coffee", "kql", "lookml", "mojo"}
NODES = [n for n in NODES if n[0] not in REMOVED]
for d in (FLAGS, INVENTORS, ORG, SOFTWARE, LOGO_SLUG):
    for k in REMOVED: d.pop(k, None)

def setn(nid, **kw):
    for n in NODES:
        if n[0] == nid:
            for k, v in kw.items(): n[["id", "label", "year", "y", "fam", "info"].index(k)] = v
            return
    raise KeyError(nid)

# renames under the node rule
setn("algol", label="ALGOL 60", info="International committee (ALGOL 58, then ALGOL 60). Block structure and BNF, the grammar notation nearly every later language inherited.")
setn("lisp", label="LISP", info="MIT, John McCarthy. The original LISP (1958) and LISP 1.5: code is data, garbage collection, the REPL. Its living family is drawn as Scheme, Common Lisp and Clojure.")
setn("basic", label="Dartmouth BASIC", info="Dartmouth College, John Kemeny and Thomas Kurtz. The original BASIC for students; its heirs are drawn separately (Visual Basic, VBA).")
setn("ml", info="Edinburgh, Robin Milner. The ML line: LCF ML (1973) and Standard ML. Type inference and pattern matching; framework from Landin's ISWIM.")
setn("rust", year=2010, info="Graydon Hoare's personal project from 2006, announced by Mozilla in 2010; version 1.0 in 2015. Memory safety without a garbage collector, checked by the borrow checker.")
setn("smalltalk", info="Xerox PARC, Alan Kay. Everything is an object that receives messages; also pioneered the GUI. Continues as Squeak and Pharo.")
setn("pli", y=355)
setn("ts", info="Microsoft, Anders Hejlsberg. JavaScript plus a structural type system; GitHub's most used language in 2025.")

NEW = [
 ("cpl", "CPL", 1963, 440, "c", "Cambridge and London, Christopher Strachey's team. An ambitious ALGOL 60 descendant, never fully implemented; BCPL is its stripped-down offspring."),
 ("algol68", "ALGOL 68", 1968, 395, "c", "IFIP Working Group 2.1, Adriaan van Wijngaarden. ALGOL's powerful, complex successor; gave C its type composition, C++ operator overloading and the Bourne shell if…fi."),
 ("iswim", "ISWIM", 1966, 200, "ml", "Peter Landin, 'The Next 700 Programming Languages'. A never-implemented 'paperware' language: expressions, let/where and the off-side rule."),
 ("b", "B", 1969, 560, "c", "Bell Labs, Ken Thompson with Dennis Ritchie. BCPL squeezed onto the PDP-7; Ritchie added types and it became C."),
 ("commonlisp", "Common Lisp", 1984, 140, "lisp", "Guy Steele and the X3J13 committee (ANSI 1994). Unified the Maclisp dialects; CLOS, macros and SBCL."),
 ("cyclone", "Cyclone", 2002, 430, "c", "AT&T Labs and Cornell (Jim, Morrisett and others). A safe dialect of C with region-based memory; named in the Rust Reference."),
 ("newsqueak", "Newsqueak", 1989, 572, "other", "Bell Labs, Rob Pike. A concurrent language with channels as first-class values; its line (Alef, Limbo) led to Go."),
 ("j", "J", 1990, 290, "array", "Kenneth Iverson and Roger Hui. Iverson's ASCII successor to APL: the same array thinking, spelled with ordinary characters."),
 ("kq", "K / q", 1992, 257, "array", "Arthur Whitney; Kx Systems. K (1992) is a terse ASCII array language; q (2003) adds a query layer and runs the kdb+ database."),
 ("vba", "VBA", 1993, 1185, "edu", "Microsoft (Excel 5, 1993). Visual Basic embedded in Office: the macro language behind countless Excel and Access tools."),
]
NODES += [list(n) for n in NEW]

FLAGS.update({"cpl": ("gb", []), "algol68": ("intl", []), "iswim": ("us", ["gb"]), "b": ("us", []),
              "commonlisp": ("us", []), "cyclone": ("us", []), "newsqueak": ("us", ["ca"]), "j": ("ca", ["hk"]),
              "kq": ("us", ["ca"]), "vba": ("us", [])})
COUNTRY["hk"] = "Hong Kong"
INVENTORS.update({
 "cpl": [("Christopher Strachey", "gb"), ("David Barron", "gb"), ("Cambridge–London team", None)],
 "algol68": [("Adriaan van Wijngaarden", "nl"), ("IFIP Working Group 2.1", None), ("", None)],
 "iswim": [("Peter Landin", "gb")],
 "b": [("Ken Thompson", "us"), ("Dennis Ritchie", "us")],
 "commonlisp": [("Guy Steele", "us"), ("Scott Fahlman", "us"), ("X3J13 committee", None)],
 "cyclone": [("Trevor Jim", None), ("Greg Morrisett", None), ("AT&T Labs and Cornell team", None)],
 "newsqueak": [("Rob Pike", "ca")],
 "j": [("Kenneth Iverson", "ca"), ("Roger Hui", "hk")],
 "kq": [("Arthur Whitney", "ca")],
 "vba": [("Microsoft team", None), ("", None), ("", None)],
})
ORG.update({
 "cpl": "University of Cambridge and University of London", "algol68": "IFIP Working Group 2.1 (international)",
 "iswim": "Univac Division of Sperry Rand, New York", "b": "Bell Labs (AT&T)",
 "commonlisp": "X3J13 committee (ANSI); 'Common Lisp the Language' by Guy Steele", "cyclone": "AT&T Labs Research and Cornell University",
 "newsqueak": "Bell Labs (AT&T)", "j": "Iverson Software (later Jsoftware), Toronto", "kq": "Arthur Whitney; Kx Systems (kdb+)",
 "vba": "Microsoft (first in Excel 5)",
})
ORG["rust"] = "Personal project from 2006, then Mozilla Research (announced 2010)"
# software moves: the Common Lisp programs leave the historical LISP node
SOFTWARE["commonlisp"] = [s for s in SOFTWARE.pop("lisp") if s[0] != "Emacs"]
SOFTWARE["kq"] = [("kdb+ tick databases", "time-series databases used by banks and trading firms")]
SOFTWARE["vba"] = [("Excel and Access macros", "automation in countless business workbooks")]
SOFTWARE["vb"] = [s for s in SOFTWARE["vb"] if not s[0].startswith("VBA")]
LOGO_SLUG.pop("lisp", None); LOGO_SLUG["commonlisp"] = "commonlisp"
# Logos dropped after a trademark check (the owner requires permission, or publishes no usage policy);
# these cards show the language's initials instead. See docs/logo-credits.md.
for _k in ("go", "scratch", "delphi", "mathematica", "cypher"):
    assert _k in LOGO_SLUG, _k
    del LOGO_SLUG[_k]

# ---------- status ----------
# maint: active / maintenance-only / dormant ; newproj: broad / niche / rare / none ; base: critical / substantial / niche / historical
# outlook: bull / steady / bear / None ; conf: high / medium / low ; ai: True if the call rests mainly on the AI assumption
# ---- version 3: two widely used intermediates become nodes (see the node rule in the method note) ----
NEW3 = [
 ("turbopascal", "Turbo Pascal", 1983, 1040, "c", "Borland, Anders Hejlsberg. A very fast Pascal compiler with its own editor, sold cheaply; a generation learned programming on it, and it grew into Delphi."),
 ("quickbasic", "QuickBASIC", 1985, 1095, "edu", "Microsoft. Structured BASIC without line numbers, with a compiler and editor; its subset QBasic shipped with MS-DOS, and its language became Visual Basic's."),
]
NODES += [list(n) for n in NEW3]
FLAGS.update({"turbopascal": ("us", ["dk"]), "quickbasic": ("us", [])})
INVENTORS.update({"turbopascal": [("Anders Hejlsberg", "dk")], "quickbasic": [("Microsoft team", None), ("", None), ("", None)]})
ORG.update({"turbopascal": "Borland International (compiler written by Hejlsberg at PolyData, Denmark)", "quickbasic": "Microsoft"})
SOFTWARE["turbopascal"] = [("ZZT", "Tim Sweeney's 1991 game, first developed in Turbo Pascal")]
SOFTWARE["quickbasic"] = [("Gorillas and Nibbles", "the QBasic sample games shipped with MS-DOS 5")]
setn("basic", info="Dartmouth College, John Kemeny and Thomas Kurtz. The original BASIC for students; its heirs are drawn separately (QuickBASIC, Visual Basic, VBA).")
setn("pascal", info="ETH Zurich, Niklaus Wirth. Built to teach structured programming; ancestor of Modula, Oberon and Turbo Pascal.")
S = {}
def st(nid, maint, newproj, base, outlook=None, conf=None, ai=False, ifchange="", note=None):
    S[nid] = dict(maint=maint, newproj=newproj, base=base, ol=outlook, conf=conf, ai=ai, ifchange=ifchange,
                  note=note if note is not None else V1STATUS.get(nid, (None, None, ""))[2])
st("fortran", "active", "niche", "critical", "steady", "high", ifchange="Climate, weather and physics codes were rewritten in C++ or Julia at scale.")
st("lisp", "dormant", "none", "historical", note="McCarthy's LISP and LISP 1.5 are long gone; the family lives on in Common Lisp, Scheme and Clojure.")
st("cobol", "active", "rare", "critical")
st("algol", "dormant", "none", "historical")
st("apl", "active", "niche", "niche", "steady", "medium", ifchange="Dyalog's finance and insurance users moved their array code to Python.", note="A small, devoted niche (Dyalog APL, GNU APL); its ideas live on in J, K/q and NumPy.")
st("pascal", "active", "rare", "niche", note="Free Pascal and Lazarus keep it maintained; it mostly lives on as Delphi.")
st("forth", "active", "rare", "niche", note="Gforth and embedded niches keep it maintained; its idea survives in PostScript. Low confidence: Fading vs. Alive is a close call.")
st("c", "active", "broad", "critical", "steady", "high", ifchange="Rust replaced C in new kernels and embedded code much faster than expected.")
st("smalltalk", "active", "niche", "niche", "bear", "low", ai=True, ifchange="Live, image-based environments became an advantage for AI-assisted development.", note="Pharo, Squeak and commercial Smalltalks keep a small research and finance niche; its image-based tooling sits awkwardly with file-based workflows.")
st("prolog", "active", "niche", "niche", "steady", "low", ai=True, ifchange="LLM-plus-solver systems adopted Prolog widely (upside), or Datalog variants took its place (downside).", note="SWI-Prolog and Scryer are active; used in research, rule engines and teaching.")
st("ml", "active", "rare", "niche", note="Standard ML (SML/NJ, MLton, Poly/ML) survives in teaching and theorem provers such as Isabelle and HOL4; OCaml and F# carry the line.")
st("sql", "active", "broad", "critical", "bull", "low", ai=True, ifchange="Natural-language querying turned SQL into an invisible intermediate rather than written code.")
st("scheme", "active", "niche", "niche", "bear", "low", ai=True, ifchange="A Scheme (Guile, Chez) became a common embedded or teaching default again.", note="Chez, Guile, Gambit and Chicken are maintained; introductory courses in the SICP tradition have mostly moved to Python.")
st("s", "dormant", "none", "historical")
st("matlab", "active", "niche", "substantial", "bear", "medium", ifchange="Simulink-centred engineering toolchains kept universities and industry from moving to Python.")
st("objc", "maintenance-only", "rare", "substantial")
st("cpp", "active", "broad", "critical", "steady", "high", ifchange="Memory-safety regulation pushed new systems code to Rust much faster.")
st("excel", "active", "broad", "critical", "bull", "low", ai=True, ifchange="Python in Excel or AI agents took over advanced spreadsheet logic.")
st("erlang", "active", "niche", "substantial", "steady", "medium", ifchange="The BEAM community moved entirely to Elixir and Gleam.")
st("perl", "active", "rare", "substantial")
st("bash", "active", "broad", "critical", "bull", "low", ai=True, ifchange="Agents' shell use stayed in throwaway commands rather than persistent scripts, or Python and declarative CI absorbed scripting.", note="Assumption: AI agents run shell commands constantly, and part of that persists as scripts (CI, setup, containers). Running commands is not the same as written code.")
st("haskell", "active", "niche", "niche", "bear", "low", ai=True, ifchange="Strong type systems became the preferred target for checking AI-written code.", note="Influential and loved, but small: a steep learning curve and a small job market; strong in compilers and finance.")
st("python", "active", "broad", "critical", "bull", "medium", ifchange="A faster Python-compatible language or TypeScript took over data and AI tooling.")
st("r", "active", "niche", "substantial", "steady", "medium", ifchange="Pharma and academic statistics moved to Python faster (down), or AI made R as easy to write as Python (up).")
st("java", "active", "broad", "critical", "steady", "high", ifchange="Kotlin took over most new JVM work, including back ends.")
st("js", "active", "broad", "critical", "bear", "medium", ifchange="Deployed runtime code were counted instead of newly written source: TypeScript compiles to JavaScript.", note="Still what every browser runs, but new code is increasingly written in TypeScript.")
st("ruby", "active", "niche", "substantial", "bear", "medium", ifchange="Rails regained its place as the default for new web start-ups.")
st("php", "active", "niche", "critical", "steady", "medium", ifchange="WordPress lost its share of the web, or modern PHP (Laravel) won back new projects.")
st("ocaml", "active", "niche", "niche", "bear", "medium", ifchange="OCaml's use for verified and analysis tooling grew beyond its niche.")
st("csharp", "active", "broad", "critical", "bull", "medium", ifchange=".NET lost ground on Linux servers, or Unity lost game developers.")
st("scala", "active", "niche", "substantial", "bear", "medium", ifchange="Spark's Scala API regained ground over PySpark and SQL.")
st("fsharp", "active", "niche", "niche", "bear", "medium", ifchange="Microsoft made F# a first-class choice alongside C#.")
st("clojure", "active", "niche", "niche", "bear", "low", ai=True, ifchange="REPL-driven development became an advantage for AI agents.", note="Loyal users and active releases, but a smaller community than in the mid-2010s; Nubank is its main anchor.")
st("dax", "active", "niche", "substantial", "steady", "medium", ifchange="Power BI and Fabric lost market share, or semantic layers replaced hand-written measures.", note="Power BI and Fabric keep growing, but DAX depends on a single vendor's engine.")
st("go", "active", "broad", "substantial", "bull", "medium", ifchange="Rust or Kotlin took over new cloud infrastructure.")
st("dart", "active", "niche", "niche", "bear", "medium", ifchange="Flutter became the default for cross-platform apps beyond Google.")
st("kotlin", "active", "niche", "substantial", "bull", "medium", ifchange="Kotlin Multiplatform stalled, confining Kotlin to Android.")
st("julia", "active", "niche", "niche", "steady", "low", ai=True, ifchange="AI tools defaulted to Julia for numerical code (up), or Python's compilers (Numba, JAX) closed the speed gap (down).", note="Strong in climate, pharmaceutical and macroeconomic modelling; AI tools default to Python.")
st("ts", "active", "broad", "critical", "bull", "medium", ifchange="Native type annotations in JavaScript made TypeScript's compiler unnecessary.")
st("elixir", "active", "niche", "niche", "bear", "low", ai=True, ifchange="Its gradual type system and Phoenix drew a much larger community.", note="A loved niche for real-time back ends; a small community and public codebase.")
st("m", "active", "niche", "substantial", "steady", "medium", ifchange="Power Query were replaced by Python or SQL in Fabric.")
st("swift", "active", "niche", "substantial", "steady", "medium", ifchange="Swift gained real server-side or cross-platform adoption (up), or Apple shifted to another language (down).", note="Apple's future, but bounded by Apple's platforms.")
st("rust", "active", "broad", "substantial", "bull", "medium", ifchange="Memory-safety requirements relaxed, or C++ safety profiles won back new systems work.")
st("simula", "dormant", "none", "historical")
st("bcpl", "active", "none", "historical", note="Martin Richards still maintains a distribution; no new projects. Lives on through C.")
st("clu", "dormant", "none", "historical")
st("awk", "active", "niche", "substantial", "steady", "high", ifchange="Its one-liner role moved entirely to Python and AI-generated scripts.")
st("sh", "active", "niche", "critical", "steady", "high", ifchange="POSIX sh stopped being the portable default for system scripts.")
st("ada", "active", "niche", "substantial", "steady", "medium", ifchange="Rust displaced Ada in safety certification (avionics, rail).")
st("miranda", "dormant", "none", "historical", note="Superseded by Haskell; its source was released in 2020.")
st("abc", "dormant", "none", "historical")
st("self", "active", "none", "historical", note="Still maintained by its authors, but no new projects; lives on in JavaScript's prototypes and in JIT techniques.")
st("oberon", "dormant", "none", "historical")
st("basic", "dormant", "none", "historical")
st("logo", "active", "none", "historical", note="Implementations survive, but its classroom role passed to Scratch.")
st("vb", "maintenance-only", "rare", "substantial", note="VB6 is long gone and VB.NET has been frozen since 2020; VBA is drawn separately.")
st("delphi", "active", "niche", "substantial", "bear", "medium", ifchange="Embarcadero's cross-platform tooling won new projects.")
st("lua", "active", "niche", "substantial", "steady", "medium", ifchange="Roblox's Luau or game engines moved to another scripting language.")
st("scratch", "active", "niche", "substantial", "steady", "medium", ifchange="AI tutors replaced block-based first steps in schools.")
st("zig", "active", "niche", "niche", "bull", "low", ifchange="Zig stalled before 1.0, or Rust absorbed the 'better C' niche.", note="A simpler 'better C' with growing adoption, but still before version 1.0.")
st("pli", "active", "rare", "substantial")
st("spss", "active", "niche", "substantial", "bear", "medium", ifchange="IBM invested in SPSS syntax again, or point-and-click analysis regained ground.")
st("sas", "active", "niche", "substantial", "bear", "medium", ifchange="Regulators and pharma kept SAS as the default for submissions.")
st("stata", "active", "niche", "substantial", "bear", "medium", ifchange="Applied economics kept teaching Stata as the default.")
st("abap", "active", "niche", "critical", "steady", "high", ifchange="SAP moved custom development off ABAP.")
st("modula3", "dormant", "none", "historical")
st("hack", "active", "niche", "substantial", "bear", "medium", ifchange="Hack spread beyond Meta and a few companies such as Slack.")
st("powershell", "active", "niche", "substantial", "steady", "high", ifchange="Windows and Azure administration moved to another automation language.")
st("mathematica", "active", "niche", "substantial", "steady", "medium", ifchange="AI assistants replaced symbolic computation for researchers.")
st("tex", "active", "niche", "critical", "steady", "high", ifchange="Mathematics and physics publishing moved to another typesetting system (e.g. Typst).")
st("modula2", "active", "rare", "niche")
st("eiffel", "active", "rare", "niche")
st("icon", "dormant", "none", "historical")
st("snobol", "active", "none", "historical", note="SNOBOL4 implementations survive; no new projects. Its pattern matching lives on in AWK, Icon and regular expressions.")
st("tsql", "active", "niche", "critical", "steady", "high", ifchange="SQL Server and Fabric warehouses moved logic out of stored procedures.")
st("plsql", "active", "niche", "critical", "steady", "high", ifchange="Oracle's installed base migrated to other databases.")
st("mdx", "maintenance-only", "rare", "substantial")
st("cypher", "active", "niche", "niche", "steady", "medium", ifchange="GQL fully absorbed Cypher (down), or graph databases became mainstream (up).", note="Graph databases and knowledge graphs grow, but the ISO GQL standard may absorb Cypher itself.")
st("cpl", "dormant", "none", "historical", note="Never fully implemented; BCPL is its legacy.")
st("algol68", "active", "none", "historical", note="Algol 68 Genie keeps it runnable; no new projects. Lives on through C, C++ and the Bourne shell.")
st("iswim", "dormant", "none", "historical", note="A 'paperware' language that was never implemented as such; lives on in ML, Miranda and Haskell.")
st("b", "dormant", "none", "historical", note="Replaced by C within a few years.")
st("commonlisp", "active", "niche", "niche", "bear", "low", ai=True, ifchange="Macro-heavy, interactive Lisp development found new use with AI tooling.", note="SBCL is active and production systems exist (QPX, Grammarly), but the community is small.")
st("cyclone", "dormant", "none", "historical", note="Research project, inactive since 2006; its region ideas live on in Rust.")
st("newsqueak", "dormant", "none", "historical", note="Superseded by Alef, Limbo and finally Go.")
st("j", "active", "niche", "niche", "bear", "medium", ifchange="Array programming in plain ASCII caught on beyond its small community.", note="Jsoftware keeps it maintained and open source; a small community in finance, teaching and research.")
st("kq", "active", "niche", "substantial", "steady", "medium", ifchange="Finance tick-data stacks moved to Python, Polars or DuckDB.", note="kdb+/q is entrenched in banks and trading firms for time-series data.")
st("vba", "maintenance-only", "niche", "critical", "bear", "medium", ifchange="Microsoft retired VBA (down), or Office Scripts and Python in Excel stalled (up).", note="Still behind countless Excel and Access tools, but Microsoft no longer evolves it.")

st("turbopascal", "dormant", "none", "historical", note="Discontinued after version 7 (1992), when Delphi replaced it; Free Pascal keeps a Turbo Pascal compatibility mode.")
st("quickbasic", "dormant", "none", "historical", note="Discontinued after QuickBASIC 4.5 (1988) and QBasic 1.1 (1993); Visual Basic replaced it. QB64 and FreeBASIC are independent successors.")

def health(s):
    if s["newproj"] == "none" or s["maint"] == "dormant": return "dead"
    if s["newproj"] == "rare": return "fading"
    if s["newproj"] == "broad" and s["maint"] == "active" and s["base"] in ("critical", "substantial"): return "thriving"
    return "alive"
for k, s in S.items():
    s["st"] = health(s)
    assert (s["ol"] is None) == (s["st"] in ("dead", "fading")), (k, s)
    assert s["ol"] is None or (s["conf"] and s["ifchange"]), k
    if s["ai"]: assert s["conf"] == "low", k

# what a node covers, where it is more than one language (node rule exceptions)
SCOPE = {
 "smalltalk": ("continuing", "Smalltalk-80 and its descendants Squeak and Pharo (Pharo calls itself 'Smalltalk-inspired')."),
 "scheme": ("continuing", "The Scheme standards (R5RS–R7RS) and implementations such as Chez, Guile, Gambit and Chicken. Racket, which renamed itself from PLT Scheme in 2010, is not included."),
 "ml": ("aggregated", "LCF ML (1973) and Standard ML (1983/1990)."),
 "kq": ("aggregated", "K (1992) and q (2003), Whitney's closely related pair; q is a query layer written in K."),
 "vb": ("aggregated", "Visual Basic 1–6 and VB.NET; VBA is drawn separately."),
 "excel": ("continuing", "The Excel formula language from 1985 to today, including LAMBDA (2020)."),
 "delphi": ("continuing", "Delphi's Object Pascal, from Borland to Embarcadero."),
 "sh": ("continuing", "The Bourne shell and the POSIX sh standard based on it; Bash is drawn separately."),
 "tsql": ("aggregated", "Transact-SQL in Sybase and Microsoft SQL Server."),
 "mathematica": ("continuing", "Mathematica's language, now called the Wolfram Language."),
 "tex": ("continuing", "TeX and the macro packages built on it, such as LaTeX."),
 "lisp": ("historical", "McCarthy's LISP (1958) and LISP 1.5 only; later dialects are drawn separately."),
 "algol": ("historical", "ALGOL 60 (with ALGOL 58 as its precursor); ALGOL 68 is drawn separately."),
 "basic": ("historical", "Dartmouth BASIC and the classic line-numbered BASICs; Visual Basic and VBA are drawn separately."),
 "pascal": ("continuing", "Standard Pascal and Free Pascal; Object Pascal is drawn as Delphi."),
 "fortran": ("continuing", "FORTRAN I to modern Fortran (2023 standard)."),
}

SCOPE.update({
 "turbopascal": ("aggregated", "Turbo Pascal 1 to 7 (1983–1992) and Borland Pascal; Delphi is drawn separately."),
 "quickbasic": ("aggregated", "QuickBASIC 1 to 4.5 (1985–1988) and its interpreter-only subset QBasic (1991)."),
 "basic": ("historical", "Dartmouth BASIC and the classic line-numbered BASICs; QuickBASIC, Visual Basic and VBA are drawn separately."),
 "pascal": ("continuing", "Standard Pascal and Free Pascal; Turbo Pascal and Delphi are drawn separately."),
})

if __name__ == "__main__":
    out = ["# Node data, generated by make_nodes.py (edit there, then re-run)", ""]
    for name, val in [("NODES", [tuple(n) for n in NODES]), ("STATUS", S), ("FLAGS", FLAGS), ("COUNTRY", COUNTRY),
                      ("INVENTORS", INVENTORS), ("ORG", ORG), ("SOFTWARE", SOFTWARE), ("LOGO_SLUG", LOGO_SLUG),
                      ("FAMILIES", FAMILIES), ("SCOPE", SCOPE)]:
        out.append(f"{name} = " + pprint.pformat(us(val), width=140, sort_dicts=False))
        out.append("")
    open(os.path.join(HERE, "nodes.py"), "w").write("\n".join(out))
    from collections import Counter
    print("nodes", len(NODES), Counter(s["st"] for s in S.values()), Counter(s["ol"] for s in S.values()))
    print("low-confidence:", sorted(k for k, s in S.items() if s["conf"] == "low"))
    ids = {n[0] for n in NODES}
    for d, nm in [(S, "STATUS"), (FLAGS, "FLAGS"), (INVENTORS, "INVENTORS"), (ORG, "ORG")]:
        print(nm, "missing", ids - set(d), "extra", set(d) - ids)
