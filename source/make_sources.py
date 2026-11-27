# Builds sources.json: one evidence record per link, from the research batches
# (research/batch_*.json, written by the research agents) plus the sources verified
# directly against the sources (OWN below).
import json, glob, os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "us_spelling.py"), encoding="utf-8").read())   # us(): US spelling for our own text
exec(open(os.path.join(HERE, "edges_v2.py"), encoding="utf-8").read())   # the version 2 links; version 3 is applied at the end

ALIAS = {
 "lisp": "lisp", "scheme": "scheme", "clojure": "clojure", "java": "java", "ml": "ml", "smalltalk": "smalltalk",
 "common lisp": "commonlisp", "julia": "julia", "iswim": "iswim", "logo": "logo", "mathematica": "mathematica",
 "r": "r", "javascript": "js", "lua": "lua", "apl": "apl", "s": "s", "j": "j", "k/q": "kq", "matlab": "matlab",
 "python": "python", "miranda": "miranda", "haskell": "haskell", "ocaml": "ocaml", "f#": "fsharp",
 "fortran": "fortran", "algol 60": "algol", "cpl": "cpl", "algol 68": "algol68", "bourne shell": "sh",
 "bourne shell (unix shells)": "sh", "simula": "simula", "pascal": "pascal", "modula-2": "modula2",
 "oberon": "oberon", "modula-3": "modula3", "delphi": "delphi", "tex": "tex", "pl/i": "pli", "cobol": "cobol",
 "abap": "abap", "c": "c", "objective-c": "objc", "zig": "zig", "cyclone": "cyclone", "ada": "ada",
 "pl/sql": "plsql", "spss": "spss", "sas": "sas", "stata": "stata", "basic": "basic", "dartmouth basic": "basic",
 "eiffel": "eiffel", "self": "self", "c++": "cpp", "c#": "csharp", "scala": "scala", "kotlin": "kotlin",
 "powershell": "powershell", "typescript": "ts", "bash": "bash", "perl": "perl", "awk": "awk",
 "snobol": "snobol", "icon": "icon", "abc": "abc", "sql": "sql", "php": "php", "hack": "hack", "ruby": "ruby",
 "clu": "clu", "elixir": "elixir", "erlang": "erlang", "visual basic": "vb", "vba": "vba", "scratch": "scratch",
 "t-sql": "tsql", "mdx": "mdx", "cypher": "cypher", "dax": "dax", "power query m": "m", "swift": "swift",
 "rust": "rust",
}
def nid(name):
    k = name.strip().lower()
    k = k.split(" (")[0] if k not in ALIAS else k
    return ALIAS[k]

recs = {}
for f in sorted(glob.glob(os.path.join(HERE, "research", "batch_*.json"))):
    for r in json.load(open(f)):
        key = (nid(r["from"]), nid(r["to"]))
        recs[key] = dict(verdict=r["verdict"], type=r["source_type"], citation=r["citation"], url=r["url"],
                         quote=r["quote"], note=r.get("note") or "", by="research")

C = {
 "GO": ("The Go Authors (n.d.). Frequently Asked Questions: 'What are Go's ancestors?'. go.dev.", "https://go.dev/doc/faq"),
 "RUST": ("The Rust Project (n.d.). The Rust Reference, Appendix 'Influences'. doc.rust-lang.org.", "https://doc.rust-lang.org/reference/influences.html"),
 "KOTLIN": ("JetBrains (n.d.). FAQ. Kotlin Documentation, kotlinlang.org.", "https://kotlinlang.org/docs/faq.html"),
 "ADA": ("US Department of Defense (1983). Reference Manual for the Ada Programming Language (ANSI/MIL-STD-1815A), §1.3 Design Goals and Sources.", "https://pdv.cs.tu-berlin.de/Ada/lrm83/lrm-01-03.html"),
 "DART": ("Bracha, G. (2015). The Dart Programming Language, §1.6. Addison-Wesley (sample pages).", "https://ptgmedia.pearsoncmg.com/images/9780321927705/samplepages/9780321927705.pdf"),
 "MOLER": ("Moler, C. (2015, 15 June). Algol 60, PL/0 and MATLAB. Cleve's Corner, MathWorks blog.", "https://blogs.mathworks.com/cleve/2015/06/15/algol-60-pl0-and-matlab/"),
 "RICH": ("Richards, M. (c. 2012). How BCPL evolved from CPL. Author's version, University of Cambridge Computer Laboratory.", "https://www.cl.cam.ac.uk/~mr10/cpl2bcpl.pdf"),
 "RITCHIE": ("Ritchie, D. M. (1993). The Development of the C Language. ACM SIGPLAN Notices 28(3), HOPL-II.", "https://www.cs.tufts.edu/~nr/cs257/archive/dennis-ritchie/chist.pdf"),
 "STROU": ("Stroustrup, B. (1993). A History of C++: 1979–1991. ACM SIGPLAN Notices 28(3), HOPL-II.", "https://www.stroustrup.com/hopl2.pdf"),
 "MAGR": ("Bache, S. M. & Wickham, H. (n.d.). Introducing magrittr (package vignette), CRAN; and Tierney, L. (n.d.). Native pipe design note (PIPE.md), R Project SVN.", "https://archive.linux.duke.edu/cran/web/packages/magrittr/vignettes/magrittr.html"),
 "VALIM": ("Valim, J. (2018). Post in 'Which language first introduced the pipe operator?'. Elixir Forum.", "https://elixirforum.com/t/which-language-first-introduced-the-pipe-operator/16791"),
 "MSR": ("Microsoft Research Podcast (2021). Advancing Excel as a programming language with Andy Gordon and Simon Peyton Jones.", "https://www.microsoft.com/en-us/research/?p=743248"),
 "DAXMDX": ("Microsoft (2010). Data Analysis Expressions (DAX) and MDX. SQL Server 2008 R2 documentation.", "https://learn.microsoft.com/en-us/previous-versions/sql/sql-server-2008-r2/ff487170(v=sql.105)"),
 "PHPRFC": ("PHP RFC: Nullable Return Types (2016; implemented in PHP 7.1). wiki.php.net.", "https://wiki.php.net/rfc/nullable_return_types"),
 "ARMS": ("Armstrong, J. (2010). Talk slides, Erlang Factory SF Bay Area 2010.", "https://www.erlang-factory.com/upload/presentations/222/ErlangFactorySFBay2010-JoeArmstrong.pdf"),
 "MEER": ("Meertens, L. (2019). On the history of ABC (talk slides, CWI, 21 November 2019).", "https://www.cwi.nl/documents/195216/Meertens-20191121.pdf"),
}
GOQ = "Go is mostly in the C family (basic syntax), with significant input from the Pascal/Modula/Oberon family (declarations, packages), plus some ideas from languages inspired by Tony Hoare's CSP, such as Newsqueak and Limbo (concurrency)."
OWN = {
 ("c", "go"): ("supported", "GO", GOQ, ""),
 ("oberon", "go"): ("supported", "GO", GOQ, ""),
 ("newsqueak", "go"): ("supported", "GO", GOQ, "Alef and Limbo, Pike's intermediate languages, are not drawn as nodes."),
 ("cpp", "rust"): ("supported", "RUST", "C++: references, RAII, smart pointers, move semantics, monomorphization, memory model", ""),
 ("ocaml", "rust"): ("supported", "RUST", "SML, OCaml: algebraic data types, pattern matching, type inference, semicolon statement separation", "OCaml was also the language of Rust's first compiler (implementation)."),
 ("haskell", "rust"): ("supported", "RUST", "Haskell (GHC): typeclasses, type families", ""),
 ("cyclone", "rust"): ("supported", "RUST", "ML Kit, Cyclone: region based memory management", ""),
 ("scala", "kotlin"): ("partly", "KOTLIN", "Kotlin is inspired by existing languages such as Java, C#, JavaScript, Scala, and Groovy.", "The FAQ names Scala as an inspiration; the specific features in the label are not stated there."),
 ("pascal", "ada"): ("supported", "ADA", "…influenced this language in several respects, although to a lesser degree than did the Pascal family.", "The manual names the Pascal family as Ada's main source; ALGOL 68, Simula, Alphard and CLU as lesser ones."),
 ("smalltalk", "dart"): ("supported", "DART", "Dart's approach to type checking is also very close to the one developed for Strongtalk.", "The same section names Smalltalk, Java and JavaScript as Dart's main influences and compares Dart's mixins to Strongtalk's."),
 ("java", "dart"): ("supported", "DART", "Like Smalltalk and Java, Dart is class based and supports single inheritance", ""),
 ("js", "dart"): ("partly", "DART", "The design of Dart has been influenced by earlier languages, in particular Smalltalk, Java and Javascript.", "JavaScript is named as an influence; 'compiles to JavaScript' describes Dart's web platform rather than a borrowed feature."),
 ("csharp", "dart"): ("supported", "DART", "built-in support for asynchrony heavily influenced by C#", "async/await arrived in Dart 1.9 (2015)."),
 ("pascal", "matlab"): ("supported", "MOLER", "Consequently, the syntax of the original MATLAB is that of PL/0.", "PL/0 is the small Pascal-like language in Wirth's 'Algorithms + Data Structures = Programs'."),
 ("fortran", "matlab"): ("supported", "MOLER", "I wanted my students to have access to LINPACK and EISPACK without writing Fortran programs.", "Implementation link: MATLAB was a front-end to Fortran libraries."),
 ("cpl", "bcpl"): ("supported", "RICH", "BCPL is essentially just CPL with all the difficult bits removed and with just a few extensions.", ""),
 ("bcpl", "b"): ("supported", "RICH", "Thompson designed a cut down variant of BCPL he called B which was later extended by Ritchie resulting in C", ""),
 ("b", "c"): ("supported", "RITCHIE", "B can be thought of as C without types; more accurately, it is BCPL squeezed into 8K bytes of memory and filtered through Thompson's brain.", ""),
 ("algol68", "c"): ("supported", "RITCHIE", "The scheme of type composition adopted by C owes considerable debt to Algol 68, although it did not, perhaps, emerge in a form that Algol's adherents would approve of.", ""),
 ("algol68", "cpp"): ("supported", "STROU", "only C, Simula, Algol68, and in one case BCPL left noticeable traces in C++ as released in 1985.", "Stroustrup credits Algol68 for operator overloading and declarations anywhere in a block."),
 ("simula", "cpp"): ("supported", "STROU", "only C, Simula, Algol68, and in one case BCPL left noticeable traces in C++ as released in 1985.", ""),
 ("c", "cpp"): ("supported", "STROU", "only C, Simula, Algol68, and in one case BCPL left noticeable traces in C++ as released in 1985.", ""),
 ("ada", "cpp"): ("partly", "STROU", "The post-1985 evolution of C++ shows the influence of ideas from Ada, Clu, and ML.", "Later feature: the influence is documented, the specific features (templates, exceptions) are our reading."),
 ("clu", "cpp"): ("partly", "STROU", "The post-1985 evolution of C++ shows the influence of ideas from Ada, Clu, and ML.", "Later feature: the influence is documented, the specific features are our reading."),
 ("fsharp", "r"): ("supported", "MAGR", "a prime example is the |> operator used extensively in F# (to say the least) and indeed this – along with Unix pipes – served as a motivation for developing the magrittr package.", "Library link: R core's design note for the native pipe (R 4.1) cites magrittr, not F#."),
 ("fsharp", "elixir"): ("supported", "VALIM", "Almost sure we got it from F# but somebody pointed early on that it existed in ML before that.", "The |> operator itself dates from Isabelle/ML (1994)."),
 ("haskell", "excel"): ("partly", "MSR", "the North Star of mainstream functional programming languages", "Later feature: LAMBDA (2020) came from Microsoft Research's functional-programming work with Haskell co-designer Simon Peyton Jones; Haskell itself is not named as the source."),
 ("mdx", "dax"): ("supported", "DAXMDX", "DAX is not a subset of MDX, but a new formula language that is considered an extension of the formula language in Excel.", "Organisational link: same Analysis Services team; not a design descent."),
 ("excel", "dax"): ("supported", "DAXMDX", "DAX is not a subset of MDX, but a new formula language that is considered an extension of the formula language in Excel.", ""),
 ("hack", "php"): ("supported", "PHPRFC", "I propose to use HHVM compatible syntax to declare nullable return types - ?<type>", "Later feature: PHP 7.1 (2016)."),
 ("prolog", "erlang"): ("supported", "ARMS", "A Prolog interpretor for the telephony algebra … Deterministic prolog with processes", "Slide text; Erlang's syntax and pattern matching are Prolog-derived, its concurrency model is not."),
 ("iswim", "abc"): ("partly", "MEER", "ISWIM (Landin 1966, an expression-oriented 'paperware' language) introduced indentation for grouping", "Meertens adds that readability was the motivation for adopting indentation in ABC: a precedent rather than a documented borrowing."),
}
for key, (verdict, cid, quote, note) in OWN.items():
    cit, url = C[cid]
    recs[key] = dict(verdict=verdict, type="primary", citation=cit, url=url, quote=quote, note=note, by="source check")

edge_keys = [(e[0], e[1]) for e in EDGES]
missing = [k for k in edge_keys if k not in recs]
extra = [k for k in recs if k not in edge_keys]
from collections import Counter
if __name__ == "__main__":
    print("records", len(recs), "missing before the additions below", missing, "extra", extra)

# Links whose label was rewritten to state what the source documents: the evidence now supports the drawn claim.
REVISED = [("lisp","ml"),("lisp","smalltalk"),("lisp","mathematica"),("apl","mathematica"),("matlab","julia"),
           ("algol","pascal"),("ada","plsql"),("smalltalk","java"),("java","csharp"),("cpp","csharp"),("ml","scala"),
           ("csharp","powershell"),("csharp","ts"),("snobol","awk"),("smalltalk","ruby"),("python","swift"),("haskell","swift")]
for k in REVISED:
    r = recs[k]
    if r["verdict"] == "partly":
        r["verdict"] = "supported"
        r["note"] = ("Label revised to match the source. " + r["note"]).strip()

# ---------------- later corrections ----------------
C.update({
 "LUA": ("Ierusalimschy, R., de Figueiredo, L. H. & Celes, W. (2007). The Evolution of Lua. HOPL III, ACM.", "https://www.lua.org/doc/hopl.pdf"),
 "DEBEER": ("de Beer, H. T. (2006). The History of the ALGOL Effort (MSc thesis, TU Eindhoven), citing Perlis (1978) and Bemer (1969); and Perlis, A. J. & Samelson, K. (1958). Preliminary report: International Algebraic Language. CACM 1(12).", "https://heerdebeer.org/ALGOL/The_History_of_ALGOL.pdf"),
})
CORRECTIONS = {
 ("clu", "lua"): ("supported", "LUA", "From CLU we took multiple assignment and multiple returns from function calls.", "Lua 1.0 (1993); the same paper names Modula (control structures), C++ (local declarations), SNOBOL and Awk (tables) and C."),
 ("awk", "lua"): ("supported", "LUA", "From SNOBOL and Awk we took associative arrays, which we called tables", "Lua 1.0 (1993). SNOBOL is credited jointly; the link is drawn from AWK, the language Lua's authors used."),
 ("scheme", "lua"): ("supported", "LUA", "initially, Scheme was just a language in the background, but later it became increasingly important as a source of inspiration", "Later feature: anonymous functions and closures arrived in Lua 3.1 (1998), full lexical scoping in Lua 5.0 (2003)."),
 ("fortran", "algol"): ("partly", "DEBEER", "Choosing FORTRAN as basis for their proposal would only increase the dominant position of IBM.", "Precedent and foil, not a design source: the 1958 report cites 'experience with several successful, working problem oriented languages' without naming FORTRAN, Backus sat on the committee, and the American subcommittee deliberately did not base its proposal on FORTRAN. Drawn dotted; the analysis reports a check without this link."),
}
for key, (verdict, cid, quote, note) in CORRECTIONS.items():
    cit, url = C[cid]
    recs[key] = dict(verdict=verdict, type="primary" if cid != "DEBEER" else "secondary", citation=cit, url=url, quote=quote, note=note, by="source check")
NOTES = {
 ("icon", "python"): "Later feature: generators arrived in Python 2.2 (PEP 255, 2001).",
 ("haskell", "python"): "Later feature: list comprehensions arrived in Python 2.0 (2000).",
 ("c", "stata"): "Later feature: Mata was added in Stata 9 (2005); Stata's command and ado language is not C-like.",
 ("ada", "cpp"): "Label limited to the documented claim; HOPL-II does not tie templates or exceptions to Ada, and traces exception handling to Brian Randell's fault-tolerance work at Newcastle.",
 ("clu", "cpp"): "Label limited to the documented claim.",
 ("delphi", "csharp"): "Label limited to the documented claim: Hejlsberg names Delphi as an influence and lists properties and events among C#'s differences from Java, without attributing them to Delphi.",
 ("scala", "kotlin"): "Label limited to the documented claim; drawn dotted because the FAQ does not indicate how substantial the influence was.",
 ("js", "dart"): "Label limited to the documented claim; 'compiles to JavaScript' is a platform relationship and no longer part of the label.",
 ("csharp", "kotlin"): "Feature evidence is a slide title in Breslav's 2022 talk ('Extensions in C# and Scala'); drawn dotted.",
}
for k, n in NOTES.items():
    recs[k]["note"] = (n + " " + recs[k]["note"]).strip()
# Links whose label was narrowed later: the earlier note discussed the old label, so it is replaced.
NARROWED = {
 ("ada", "cpp"): "Label limited to the documented claim. Stroustrup names Ada, CLU and ML together for C++ after 1985 and does not tie templates or exceptions to Ada; he traces exception handling to Brian Randell's fault-tolerance work at Newcastle. Drawn dotted, like CLU → C++, because the source gives no strength.",
 ("clu", "cpp"): "Label limited to the documented claim (same sentence as Ada → C++). Drawn dotted because the source gives no strength.",
 ("delphi", "csharp"): "Label limited to the documented claim: Hejlsberg names Delphi as an influence and lists properties and events among C#'s differences from Java, without attributing them to Delphi. The Artima interview 'Delegates, Components, and Simplexity' (2003) discusses first-class properties and events but does not mention Delphi. Drawn dotted because the source gives no strength.",
 ("scala", "kotlin"): "Label limited to the documented claim: the FAQ names Scala as an inspiration without naming features. Drawn dotted because the FAQ gives no strength.",
 ("js", "dart"): "Label limited to the documented claim: Bracha names JavaScript as an influence. 'Compiles to JavaScript' describes Dart's web platform rather than a borrowed feature and is no longer part of the label. Drawn dotted because the source gives no strength.",
}
for k, n in NARROWED.items():
    recs[k]["note"] = n
for k in [("ada","cpp"), ("clu","cpp"), ("delphi","csharp"), ("scala","kotlin"), ("js","dart")]:
    recs[k]["verdict"] = "supported"
# Three-part evidence: relationship, specific feature, and strength (the line style itself).
EVID = {
 ("fortran","algol"): ("precedent only; FORTRAN not named", "not documented"),
 ("pli","sas"): ("documented (secondary source)", "n/a (implementation)"),
 ("cobol","abap"): ("secondary source only", "resemblance"),
 ("csharp","kotlin"): ("documented (Kotlin FAQ)", "talk slide only"),
 ("fsharp","m"): ("resemblance ('similar to F#')", "resemblance"),
 ("haskell","excel"): ("functional-programming research; Haskell not named", "LAMBDA documented"),
 ("iswim","abc"): ("precedent", "indentation (precedent)"),
 ("clu","ruby"): ("secondary source only", "iterators (secondary)"),
 ("eiffel","ruby"): ("documented (Eiffel named)", "secondary source only"),
 ("ruby","elixir"): ("designer downplays it", "surface resemblance"),
 ("sql","dax"): ("considered in the design", "relational concepts"),
 ("ada","cpp"): ("documented", "none claimed (label limited to the documented claim)"),
 ("clu","cpp"): ("documented", "none claimed (label limited to the documented claim)"),
 ("delphi","csharp"): ("documented", "none claimed (label limited to the documented claim)"),
 ("scala","kotlin"): ("documented (named inspiration)", "none claimed (label limited to the documented claim)"),
 ("js","dart"): ("documented", "none claimed (label limited to the documented claim)"),
}
STRENGTH = {(e[0], e[1]): e[3] for e in EDGES}
KIND = {(e[0], e[1]): e[4] for e in EDGES}
# Links by another route (implementation, platform, library, product, organizational): the note names the route.
for k in edge_keys:
    if KIND[k] in CONTEXT_KINDS:
        recs[k]["note"] = f"Influence by the {KIND[k]} route. " + recs[k]["note"]
for k in edge_keys:
    r = recs[k]
    if k in EVID: r["rel"], r["feat"] = EVID[k]
    elif KIND[k] in CONTEXT_KINDS:
        # Other-route links: the route (implementation, library, ...) is what the source documents.
        r["rel"], r["feat"] = "documented", ("documented" if STRENGTH[k] == "s" else f"n/a ({KIND[k]} route)")
    else: r["rel"], r["feat"] = "documented", "documented"
# Specific labels for links whose source names the influence but not the feature.
WIDE = {
 ("delphi", "csharp"): ("documented (Hejlsberg names Delphi; same designer)", "widely described, not in the cited source"),
 ("scala", "kotlin"): ("documented (Kotlin FAQ)", "widely described, not in the cited source"),
 ("js", "dart"): ("documented (Bracha)", "widely described, not in the cited source"),
 ("ada", "cpp"): ("documented (Stroustrup)", "widely described (Stroustrup's Design and Evolution of C++), not in the cited source"),
 ("clu", "cpp"): ("documented (Stroustrup)", "widely described, not in the cited source"),
 ("csharp", "ts"): ("same designer (Hejlsberg)", "widely described, not in the cited source"),
 ("mdx", "dax"): ("same team", "widely described, not in the cited source"),
 ("vb", "delphi"): ("documented (rival product)", "widely described, not in the cited source"),
}
for k, (rel, feat) in WIDE.items():
    recs[k]["rel"], recs[k]["feat"] = rel, feat
    recs[k]["note"] = "Label made specific; the features are widely described but not stated in the cited source. " + recs[k]["note"]
# Rule: a solid line needs a supported record in which both the relationship and the feature in the label are documented.
bad = [f"{a}>{b}" for a, b in edge_keys if STRENGTH[(a, b)] == "s" and (recs[(a, b)]["verdict"] != "supported" or not recs[(a, b)]["feat"].startswith(("documented", "widely described")))]
assert not bad, f"solid links without full support: {bad}"
missing = [k for k in edge_keys if k not in recs]; assert not missing, missing
# our own wording goes to US spelling; quotes, citations and URLs stay verbatim
for _r in recs.values():
    for _f in ("note", "rel", "feat"):
        _r[_f] = us(_r[_f])
# ---------------- version 3: apply the audit (v3_evidence.json, written by make_edges.py) ----------------
# Kept links keep their version 2 record unless the audit replaced the quote or the source; new links get a new record.
_E3 = {}
exec(open(os.path.join(HERE, "edges.py"), encoding="utf-8").read(), _E3)
EV = json.load(open(os.path.join(HERE, "v3_evidence.json"), encoding="utf-8"))
BY_URL = {}
for _k in edge_keys:
    BY_URL.setdefault(recs[_k]["url"], recs[_k])
# Corrections from the word-for-word check of every new or changed quote (research/v3_quotematch_*.json).
QUOTE_FIX = {
 ("pascal", "modula2"): ("for system programming", "for system-programming", ""),
 ("lisp", "s"): ("firstclass", "first-class", ""),
 ("fsharp", "csharp"): ("2012--the", "2012—the", ""),
 ("haskell", "csharp"): ("via C to the upcoming versions of C 3.0", "via Cω to the upcoming versions of C# 3.0",
                         "The PDF's text layer drops the characters ω and #; they are restored in the quote."),
}
URL_FIX = {
 "https://pdv.cs.tu-berlin.de/Ada/lrm83/lrm-01-03.html": "https://psc.informatik.uni-jena.de/languages/ada83/LRM-01.txt",
 "https://cs.unm.edu/~Williams/cs491/Evolution-of-Lisp.pdf": "https://www.dreamsongs.com/Files/Hopl2.pdf",
 "https://cacmb4.acm.org/blogs/blog-cacm/274388-lessons-from-pl-i-a-most-ambitious-programming-language/fulltext": "https://cacm.acm.org/blogcacm/lessons-from-pl-i-a-most-ambitious-programming-language/",
}
# Links whose sentence sits on a different page of the same cited work than the one version 2 linked.
TIE_URL = {
 ("objc", "java"): "https://www.oracle.com/java/technologies/object-oriented.html",
}
SECONDARY3 = set()          # new links whose source is not the designers' own: none so far
final = {}
for _e in _E3["EDGES"]:
    k = (_e[0], _e[1]); ev = EV[f"{k[0]}>{k[1]}"]
    kind, strong = _e[4], _e[3] == "s"
    if not ev["new"]:
        r = dict(recs[k])
        if "citation" in ev:
            r.update(citation=ev["citation"], url=ev["url"], quote=ev["quote"], type="primary", by="version 3 audit",
                     note="")
        elif "quote" in ev:
            r.update(quote=ev["quote"], by="version 3 audit")
    else:
        if "citation" in ev:
            cit, url, typ = ev["citation"], ev["url"], "primary"
        else:
            src = BY_URL[ev["src_url"]]; cit, url, typ = src["citation"], src["url"], src["type"]
        r = dict(verdict=ev["verdict"], type="secondary" if k in SECONDARY3 else typ, citation=cit, url=url, quote=ev["quote"], note="", by="version 3 audit")
    r["verdict"] = ev["verdict"]
    r["names_it"] = ev["names_it"]
    r["audit"] = ev["audit"]
    if ev["new"] or "citation" in ev or r["verdict"] != recs.get(k, {}).get("verdict"):
        # three-part evidence, restated for records the audit changed
        r["rel"] = "documented" if r["verdict"] == "supported" else "indirect support only"
        if kind in CONTEXT_KINDS: r["feat"] = f"n/a ({kind} route)"
        else: r["feat"] = "documented" if ev["names_it"] == "yes" else "not stated in the quoted sentence"
    if kind in CONTEXT_KINDS and not r["note"].startswith("Influence by the"):
        r["note"] = (f"Influence by the {kind} route. " + r["note"]).strip()
    if k in QUOTE_FIX:
        old, new, why = QUOTE_FIX[k]
        assert old in r["quote"], k
        r["quote"] = r["quote"].replace(old, new)
        if why: r["note"] = (r["note"] + " " + why).strip()
    if k in TIE_URL:
        r["url"] = TIE_URL[k]
    if r["url"] in URL_FIX:
        r["url"] = URL_FIX[r["url"]]
        r["note"] = (r["note"] + " The URL was replaced in version 3 because the earlier copy went offline.").strip()
    final[k] = r
edge_keys = [(e[0], e[1]) for e in _E3["EDGES"]]
recs = final
json.dump({f"{a}>{b}": recs[(a, b)] for a, b in edge_keys}, open(os.path.join(HERE, "sources.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
if __name__ == "__main__":
    print("links:", Counter(recs[k]["verdict"] for k in edge_keys), Counter(recs[k]["type"] for k in edge_keys), "links", len(edge_keys))
    print("quote names the influence:", Counter(recs[k]["names_it"] for k in edge_keys))
    print("partly:", [f"{a}>{b}" for a, b in edge_keys if recs[(a,b)]["verdict"] == "partly"])
