# Generates desc.py (the card paragraphs) from the v1 text plus the later edits.
import os, pprint
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "us_spelling.py"), encoding="utf-8").read())   # us(): US spelling for our own text
ns = {}; exec(open(os.path.join(HERE, "v1ref", "desc.py")).read(), ns)
D = dict(ns["DESC"])
for k in ("coffee", "kql", "lookml", "mojo"): D.pop(k)

def rep(k, old, new):
    assert old in D[k], (k, old)
    D[k] = D[k].replace(old, new)

D["lisp"] = ("John McCarthy designed LISP at MIT in 1958 as a mathematical notation for computation, aimed at artificial-intelligence research; LISP 1.5 (1962) was the first widely used version. "
 "Programs and data share one form, nested lists in parentheses, so code can easily write and transform other code, and it introduced garbage collection, the REPL and functions as values. "
 "The original language is long gone: this node is the 1958 LISP, and its living family is drawn separately as Scheme, Common Lisp and Clojure (Emacs Lisp is another descendant). "
 "Nearly every modern language borrowed something from it, and Landin's ISWIM began as an attempt to free it from lists and brackets.")
D["algol"] = ("ALGOL 60 was designed by an international committee of European and American computer scientists (ALGOL 58, then the 1960 report) as a clean, machine-independent language for describing algorithms. "
 "It introduced block structure, nested scopes, recursion as standard and the BNF notation still used to define languages. "
 "It never became commercially dominant: IBM pushed Fortran, and ALGOL 60 had no standard input and output. "
 "It was used mainly in academia and for publishing algorithms, yet CPL, Simula, Pascal and ALGOL 68 descend directly from it, and through them C and Java.")
rep("basic", "created BASIC (Beginner's", "created Dartmouth BASIC (Beginner's")
rep("basic", "was Microsoft's first product and evolved into Visual Basic.", "was Microsoft's first product, and its heirs Visual Basic and VBA are drawn separately.")
rep("ml", "It introduced type inference", "It took its basic framework from Peter Landin's ISWIM and was first implemented in Lisp. It introduced type inference")
rep("ml", "Standard ML is used in teaching and proof assistants", "This node covers LCF ML and Standard ML (1983, defined 1990), which is used in teaching and proof assistants such as Isabelle and HOL4")
rep("smalltalk", "Pharo and Squeak serve enthusiasts and some finance systems, and its ideas shaped Objective-C, Java, Ruby and Python.", "Squeak and Pharo, its direct descendants, serve research, teaching and some finance systems, and its ideas shaped Objective-C, Java, Ruby, Self and Dart.")
rep("scheme", "It is used in teaching, research and as an embedded scripting language (Guile, Racket), and its design shaped JavaScript, R and Lua.", "It is used in teaching, research and as an embedded scripting language (Guile, Chez), and its design shaped JavaScript, R and Lua. Racket, which began as PLT Scheme and renamed itself in 2010, is not part of this node.")
rep("apl", "its descendants k and q power kdb+ trading databases, and its array thinking shaped S, R, MATLAB and NumPy.", "its descendants J and K/q (the kdb+ trading databases) are drawn on the map, and its array thinking shaped S, R and NumPy.")
rep("r", "Its pipe, first %>% in the magrittr package (2014) that dplyr made famous and since R 4.1 the native |>, was borrowed from F#, while dplyr's verbs mirror SQL.",
 "Its pipe began as %>% in the magrittr package (2014), which credits F#'s |> and Unix pipes; R 4.1 (2021) made |> native syntax, and R core's design note cites magrittr. dplyr's verbs mirror SQL.")
rep("fsharp", "and its pipe operator |>, which passes a value into the next function, spread to R (via magrittr and dplyr), Elixir, OCaml and others.",
 "and its pipe operator |>, which passes a value into the next function (first seen in Isabelle/ML in 1994), spread from F# to Elixir, OCaml and, through the magrittr package, R.")
rep("js", "It runs every interactive website", "Its ES2015 arrow functions and classes owed much to CoffeeScript (2009), a cleaner syntax that compiled to JavaScript. It runs every interactive website")
rep("rust", "Graydon Hoare started Rust as a personal project in 2006; Mozilla sponsored it from 2009 and version 1.0 arrived in 2015.",
 "Graydon Hoare started Rust as a personal project in 2006; Mozilla sponsored it from 2009, announced it in 2010 and version 1.0 arrived in 2015. The Rust Reference lists its influences: SML and OCaml, C++, Cyclone, Haskell, Newsqueak, Alef and Limbo, Erlang, Swift, Scheme, C# and Ruby; its first compiler was written in OCaml.")
rep("swift", "It is used for iPhone", "Lattner names Objective-C, Rust, Haskell, Ruby, Python, C# and CLU as sources of ideas; the map draws links only where a transfer can be identified. Its later ownership features (Swift 5.9) follow Rust, and Rust in turn took optional bindings from Swift. It is used for iPhone")
rep("kotlin", "It is used for most new Android apps", "The Kotlin FAQ names Java, C#, JavaScript, Scala and Groovy as inspirations; JavaScript and Groovy are not drawn because no specific transfer has been documented. It is used for most new Android apps")
rep("dart", "Outside Flutter", "Gilad Bracha's book on Dart names Smalltalk, Java and JavaScript as its main influences: its type checking and mixins follow Strongtalk, its isolates the Erlang actor model, and its async/await C#. Outside Flutter")
rep("ada", "It is used in avionics", "Its manual names the Pascal family as Ada's main source, with ALGOL 68, Simula, Alphard and CLU as lesser influences. It is used in avionics")
rep("ocaml", "It is used at Jane Street", "Its module system follows Standard ML's. It is used at Jane Street")
rep("elixir", "It is used for real-time systems", "José Valim says its pipe operator came from F#. It is used for real-time systems")
rep("excel", "LAMBDA (2020) finally lets users define their own reusable functions.", "LAMBDA (2020), developed with Microsoft Research's functional-programming team including Haskell co-designer Simon Peyton Jones, finally lets users define their own reusable functions and makes the formula language Turing-complete.")
rep("dax", "It looks like Excel formulas", "Microsoft describes it as a new formula language extending Excel's, not a subset of MDX, and Jeffrey Wang, its lead developer, says Excel formulas, SQL and MDX were all considered in its design. It looks like Excel formulas")
rep("m", "It is a functional, lazily evaluated language", "Microsoft describes it as 'similar to F#': a functional, partly lazy language")
rep("pli", "and its syntax shaped SAS.", "and early SAS was written partly in it.")
rep("ts", "Its type system is complex", "Its type system is structural and erased at runtime, unlike C#'s, although both were designed under Hejlsberg. It is complex")
rep("pascal", "It was the dominant teaching language", "Wirth called ALGOL 60 its precursor, by way of his ALGOL W. Free Pascal and Lazarus keep standard Pascal maintained today. It was the dominant teaching language")
rep("mathematica", "Everything is a symbolic expression", "Wolfram says his early sketches for SMP, its predecessor, looked like LISP and APL before he invented his own design. Everything is a symbolic expression")
rep("self", "It never left the research lab.", "It never left the research lab, although its authors still maintain it.")
rep("c", "It gives direct control over memory", "It grew out of Ken Thompson's B, to which Ritchie added types, and its type composition owes much to ALGOL 68. It gives direct control over memory")
rep("cpp", "Templates, classes and automatic resource management", "Stroustrup names C, Simula and ALGOL 68 as the only languages that left clear traces in C++ as released in 1985; Ada, CLU and ML shaped its later templates and exceptions. Templates, classes and automatic resource management")
rep("python", "Indentation-based syntax", "It drew on ABC, C, Modula-3 and C++ for its core design, Icon for generators and Haskell for list comprehensions, while the pandas library later brought R-style data frames and SQL-style joins. Mojo (2023) is a Python superset for AI hardware. Indentation-based syntax")
rep("vb", "It lives on mainly as VBA, the macro language of Excel, Access and Office.", "VBA, drawn separately, carries it on in Office.")
rep("sas", "Its DATA steps", "Early SAS was written partly in PL/I. Its DATA steps")
rep("matlab", "Everything is a matrix", "Moler took its syntax from PL/0, the small Pascal-like language in Wirth's textbook, while the numerics were Fortran's. Everything is a matrix")
rep("tex", "It produces superb typography", "Knuth wrote it in WEB, his literate-programming system built on Pascal. It produces superb typography")
rep("spss", "Its syntax is a sequence", "It was first written in Fortran. Its syntax is a sequence")

NEW = {
"cpl": "Christopher Strachey's teams at the University of Cambridge and the University of London designed CPL (Combined Programming Language) from 1962 as a powerful successor to ALGOL 60 for both scientific and systems work. It was ambitious, with a rich type system and many features, and it proved very hard to implement: the project ran until 1966 without a complete compiler. Martin Richards removed 'all the difficult bits' to make BCPL, which is how CPL's ideas reached B and C. Its other legacy is vocabulary: the terms l-value and r-value come from Strachey's work around CPL.",
"algol68": "IFIP Working Group 2.1, led by Adriaan van Wijngaarden, designed ALGOL 68 as the successor to ALGOL 60 and defined it with a new two-level grammar. It was orthogonal and powerful, with user-defined operators, references, unions and declarations anywhere in a block. Its report was famously hard to read, several committee members signed a minority report against it, and implementations were slow to arrive, so it never displaced ALGOL 60 or Pascal. Its ideas travelled further than the language: C's type composition, C++'s operator overloading and the Bourne shell's if…fi and case…esac all come from it.",
"iswim": "Peter Landin described ISWIM ('If you See What I Mean') in his 1966 paper 'The Next 700 Programming Languages', written at Univac in New York. It was a family of languages built on the lambda calculus: everything is an expression, definitions use let and where, and indentation can show structure (Landin's 'off-side rule'). Landin presented it as an attempt to free LISP from its commitment to lists and its heavy bracketing. ISWIM itself was never implemented, but ML took its framework, David Turner's SASL, KRC and Miranda carried it to Haskell, and the off-side rule reappears in ABC and Python.",
"b": "Ken Thompson created B at Bell Labs around 1969 for the first Unix on the PDP-7, with Dennis Ritchie's help. Ritchie described it as 'BCPL squeezed into 8K bytes of memory and filtered through Thompson's brain': typeless, with the machine word as its only data type, and with compact operators such as ++ and --. On the byte-addressed PDP-11 the lack of types became a problem, so Ritchie added types and structures, and the result was C (1972). B was replaced within a few years, but much of C's look comes from it.",
"commonlisp": "Common Lisp was designed from 1981 to unify the dialects that had grown out of Maclisp, with Guy Steele's book 'Common Lisp the Language' (1984) as its first reference and an ANSI standard following in 1994. It is a large, multi-paradigm language with powerful macros, a condition system and CLOS, an object system built on generic functions and multiple dispatch. Its size, its parentheses and a small job market limit adoption, and part of the Lisp community moved to Clojure. SBCL keeps it fast and active, and it runs ITA's airfare search (QPX, behind Google Flights), Grammarly's core engine and the first version of Reddit.",
"cyclone": "Trevor Jim, Greg Morrisett and colleagues at AT&T Labs Research and Cornell University created Cyclone (2002) as a safe dialect of C. It kept C's syntax and low-level control but prevented buffer overflows, dangling pointers and format-string attacks, using fat pointers, tagged unions and region-based memory management checked by the compiler. It was a research language, harder to use than C, and development stopped around 2006. Its regions are a direct ancestor of Rust's lifetimes, and the Rust Reference lists it among Rust's influences.",
"newsqueak": "Rob Pike designed Newsqueak at Bell Labs (published in 1989) to write interactive graphical programs, such as window systems, as sets of concurrent processes. Channels were first-class values: processes communicated by sending and receiving on them, in the style of Tony Hoare's CSP. It was an interpreted research language used mainly by Pike and his colleagues. Its ideas went into Alef and Limbo, Pike's later languages for Plan 9 and Inferno, and then into Go's goroutines and channels.",
"j": "Kenneth Iverson and Roger Hui created J (1990, work beginning in 1989) as a successor to APL that uses ordinary ASCII characters instead of APL's special symbols. It keeps APL's array thinking and adds tacit programming, where functions are combined without naming their arguments. It is extremely concise but hard for outsiders to read, and its community is small. It is used in finance, teaching and research, and Jsoftware has made it open source.",
"kq": "Arthur Whitney, who had built APL systems at Morgan Stanley, created K in 1992 as a terse array language that replaces APL's special characters with ASCII. q (2003) adds readable keywords and a SQL-like query layer on top of K, and with it the kdb+ column-store database of Kx Systems, which Whitney co-founded. It is extremely fast on time-series data but famously cryptic, proprietary and expensive, with a small, highly paid talent pool. It runs tick-data and trading analytics at many banks and trading firms.",
"vba": "Microsoft introduced Visual Basic for Applications in Excel 5 (1993) to give Office a common macro language based on Visual Basic. Users can record macros and then edit the code behind them, automating workbooks, Access databases and other Office applications. It is old, Windows-centric and a common security risk, and Microsoft has stopped evolving it in favour of Office Scripts (TypeScript) and Python in Excel. It still runs countless business tools, reports and financial models.",
}
D.update(NEW)

# ---- later edits: card text follows the corrected link rows ----
rep("lua", "the table. ", "the table. Its authors name Modula, CLU, C++, SNOBOL and Awk, and C as the sources of Lua 1.0; Scheme came later, with closures in Lua 3.1 (1998) and full lexical scoping in Lua 5.0 (2003). ")
rep("cpp", "in 1985; Ada, CLU and ML shaped its later templates and exceptions.", "in 1985. Its evolution after 1985, including templates (Release 3.0, 1991), drew on ideas from Ada, CLU and ML, and its exception handling on Brian Randell's fault-tolerance work at Newcastle.")
rep("algol", "for describing algorithms. ", "for describing algorithms. FORTRAN's success was its precedent and John Backus sat on the committee, but the American members deliberately did not base their proposal on IBM's language. ")
rep("fortran", "Its strengths are", "Its success was the precedent for ALGOL, which was designed as a machine-independent alternative to it. Its strengths are")
rep("stata", "with Mata as a full matrix language", "with Mata, a C-like matrix language added in Stata 9 (2005)")
rep("python", "for its core design, Icon for generators and Haskell for list comprehensions, while the pandas library later brought", "for its core design, and later took list comprehensions from Haskell (Python 2.0) and generators from Icon (Python 2.2), while the pandas library brought")
if __name__ == "__main__":
    open(os.path.join(HERE, "desc.py"), "w").write("DESC = " + pprint.pformat(us(D), width=200, sort_dicts=False) + "\n")
    ns2 = {}; exec(open(os.path.join(HERE, "nodes.py")).read(), ns2)
    ids = {n[0] for n in ns2["NODES"]}
    print("desc", len(D), "missing", ids - set(D), "extra", set(D) - ids)
    import re
    print("mentions of removed:", [k for k, v in D.items() if re.search(r"\b(KQL|LookML|Kusto)\b", v)])
