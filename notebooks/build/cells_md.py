MD = {}

MD["title"] = r'''
# Who shaped whom? The influence network of programming languages

*A network analysis of 90 programming languages and 218 documented influence ties, from Fortran (1957) to Zig (2016). Version 3 of the data.*

Programming languages are usually drawn as family trees: neat lines of parents and children. Influence does not stay inside families, though. A language may take its type system from one tradition, its syntax from a second and a library idea from a third. Seen this way, the history of programming languages looks less like a pedigree and more like a social network, and the vocabulary of social network analysis fits it well: centrality and status, brokers who sit between groups, weak ties, cohesive subgroups, and the question of whether a prominent position reflects anything more than having arrived early.

This notebook asks six questions of the data behind the interactive map:

1. **Influence.** Which languages shaped the most others, directly and through their descendants?
2. **Borrowing.** Which languages drew on the most sources?
3. **Connectors.** Which languages sit between others, so that influence passes through them?
4. **Weak ties.** Do weak ties connect separate traditions, as Granovetter (1973) argued for social ties?
5. **Families.** Do the curated language families hold together more than chance would produce?
6. **Age.** How much of a language's reach is simply a matter of having been early?

Every result is tested against alternative ways of drawing the network (section 12), and the conclusions (section 13) say which ones survive. The aim is a set of claims that can be defended, not a set of rankings.
'''

MD["summary"] = r'''
## Summary

**Goal.** To see what network analysis can add to the history of programming languages: which languages shaped others, who connects traditions, and whether the family trees we draw match the actual flow of ideas. Because the data are a curated record built from cited sources, the second goal was to say which findings can be trusted. The analysis is therefore built around checks: influence is followed in time order, the network is redrawn five ways, the record is perturbed in both directions (wrong ties and missing ties), and every comparison has a chance baseline.

**In short.**

- **A small group of early languages dominates.** Fortran, ALGOL 60 and LISP reach the most languages, and the result holds however the network is drawn. C and LISP are borrowed from directly most often. Part of this is simply being early, but not all of it.
- **"Who borrowed most" is the least reliable question.** Rust, Python and Julia come out on top, but the ranking depends on how well each language documents its own heritage, so the usual story of Python as the great synthesizer does not hold up.
- **The connectors are the big, long-lived languages of the C line.** C++ and C sit between others in every version of the network; Python and C# do only when weak or later-version ties are counted.
- **Weak ties cross traditions without bridging them.** They link languages of different families, as the theory of weak ties suggests, but between languages that already share neighbors. They are secondary borrowings, not first links.
- **Families are real, and porous.** The curated families hold together far more than chance would produce, yet most ties still cross them.
- **Much rests on a few ties.** Half of all source-to-sink chains pass through Fortran → ALGOL 60, so the notebook shows what changes without it.

The sections below give the method, the evidence for each question, and a full list of what is robust and what is not.
'''

MD["howto"] = r'''
> **Reading and running this notebook.** `network-analysis.ipynb` holds the code and its results. `network-analysis.html` is the same notebook rendered without code, for reading. To rerun it, install the packages in `requirements.txt` (at the root of the repository) and run all cells from the `notebooks/` folder; it takes about a minute. Every random step is seeded, so a rerun reproduces the numbers quoted in the text. Figures are also saved to `notebooks/figures/`.
>
> **What is new compared with the analysis of version 2.** The data were rebuilt (every cited source re-read against a written inclusion rule), and the analysis was redesigned with them: influence is followed in time order; ties of different kinds and different evidence are tested separately instead of being pooled; uncertainty covers missing ties as well as wrong ones; every comparison with the families has a chance baseline; and the analysis of health, which depended on AI-assigned ratings, was dropped.
'''

MD["setup"] = r'''
## 1. Setup
'''

MD["data"] = r'''
## 2. The data and the graph

Each **node** is a language. Each **tie** A → B records that B's designers drew on something from A, backed by a cited source (the evidence record is in `data/edges.csv`). Ties point from the source to the borrower. Each tie carries:

- a **strength**: *strong* for a main or substantial influence, *weak* for a partial one (a single feature, a stated aim, a shared designer, a library);
- a **kind**: design, syntax, type, or one of four other mechanisms (library, implementation, platform, organizational). By rule, every tie of an "other" kind is weak;
- a **verdict** on the evidence: *supported* by the quoted sentence, or *partly supported*. This is kept apart from strength, so a strong tie can be partly supported and a weak one fully supported;
- for 32 ties, a **later version** (for example Python 2.0 or pandas 2008) and its year, when the borrowing happened after the language's first release.

The headline analysis uses **all 218 ties, unweighted**, so that every documented influence counts once. Section 12 repeats the analysis on four reduced versions of the network.
'''

MD["glance"] = r'''
**The network at a glance.** The network is sparse: under 3% of the possible ordered pairs are tied, and the average language has between four and five ties. All languages but two (Forth and SAS, which have no documented tie) form one connected component. The graph has three small loops, all caused by later-version ties: a younger language that fed something back into an older one (for example Swift into Rust 0.12, or Java into Ada 2005). Loops are what time order, introduced next, takes care of.
'''

MD["measures"] = r'''
## 3. Measures

| Question | Measure | What it counts |
|---|---|---|
| Who influenced the most? | **Direct influence** (outdegree) | Languages that borrowed directly from it. |
| | **Influence domain** | All languages that its influence can reach along chains of ties, however many steps away (Wasserman and Faust 1994, ch. 5). |
| | **Status** (PageRank on reversed ties) | A language has high status when it is borrowed from by languages that are themselves borrowed from; this recursive idea goes back to Katz (1953) and Bonacich (1987), and PageRank (Brin and Page 1998) is its best-known form. |
| Who borrowed the most? | **Direct borrowing** (indegree) | Languages it borrowed from directly. |
| | **Ancestry** | All languages that can reach it along chains of ties. |
| Who connects? | **Betweenness** (Freeman 1977) | For every pair of languages, the share of their shortest chains of influence that pass through it. |

### Chains must respect time

A measure that follows chains (influence domain, ancestry, betweenness) normally assumes that anything can travel along any path. Here that would be wrong. A tie A → B records a particular feature at a particular date. If B took a feature from A in 2008 (as pandas took ideas from R), that feature cannot have passed on from B to a language that borrowed from B in 1995.

So a chain A → B → C counts **only if the tie B → C is no earlier than the tie A → B**. A tie is dated by the later version it records (Python 2.0 is 2000) or, if it has none, by the year the borrowing language first appeared. This also removes the loops of section 2: chains never run backward. The functions below implement this. They are checked against networkx on the ties present at first release, where every chain already runs forward in time and the results must agree exactly. (They were also checked against a brute-force enumeration of all chains on 300 random small graphs with loops, outside this notebook; there were no differences.)

The effect on this data is modest overall (the rank correlation with ignoring dates is 0.99 for both reach measures) but it matters for particular languages: PowerShell's ancestry falls from 42 to 28, PL/SQL's from 23 to 10, and Java's influence domain from 26 to 17.
'''

MD["uncertainty"] = r'''
## 4. Uncertainty: what if the record is wrong?

The 90 languages and 218 ties are not a random sample from a larger population. They are a curated record, so sampling-based confidence intervals and p-values do not apply to the rankings. The real uncertainty is about **the record itself**, and it runs in two directions:

- a recorded tie may not be a real design influence (a source can be misread, and 18 ties are only partly supported by their quoted sentence);
- real ties may be missing, because nobody wrote them down or the sources do not mention them. The sources of version 3 were re-read in full, but an influence that no source states is invisible.

The notebook therefore re-runs every measure on **1,000 perturbed copies** of the network. In each copy, every tie is dropped with a probability set by its evidence, and extra ties are added between random pairs of languages (the older one as the source). The tables report each language's **rank on the full network**, its **median rank across the copies**, and the **90% interval** of its rank (5th to 95th percentile). A narrow interval means the position does not depend on any one uncertain tie.

| | Drop a supported tie | Drop a partly supported tie | Random ties added |
|---|---|---|---|
| **Moderate** (the intervals in the tables) | 10% | 50% | 10% of the number of ties (22) |
| **Severe** (a stress test, section 12) | 20% | 60% | 25% of the number of ties (54) |

These are assumptions, not estimates; nothing in the data calibrates them. They are chosen to be clearly pessimistic, and the conclusions rest on results that hold under the severe setting as well. Two further points about reading the intervals: languages with the same value share a rank, and the full network is the most generous case, so an interval need not be centered on the observed rank.
'''

MD["timeline"] = r'''
## 5. The shape of the network, and its main path

Figure 1 places every language at its year of creation, in a band for its family. Node size shows the influence domain.

The dark line is the network's **main path**. Main path analysis was developed by Hummon and Doreian (1989) to find the backbone of a citation network, the chain of papers through which a field's knowledge flowed. Each tie gets a **search path count**: the number of chains from a source (a language with no recorded parent) to a sink (one with no recorded heir) that pass through it (Batagelj 2003). The **global main path** is the source-to-sink chain with the highest total count (Liu and Lu 2012).

The method needs a graph without loops, so it uses the 186 ties present at first release. They all run forward in time, which also keeps the path from running through a feature added decades later. When several chains tie for the best, all of them are shown, so that no ending is chosen arbitrarily.
'''

MD["timeline_read"] = r'''
**Reading Figure 1.** The main path runs **Fortran → ALGOL 60 → CPL → BCPL → B → C → C++ → Java → C# → F#**, and then ends in either Elixir or Power Query M (equally good). This is the spine of the network: the ALGOL-to-C line, and the object-oriented languages built on it. The last steps matter little, since several languages hang off C# and F# with equal weight.

Two cautions. First, main paths favor **long unbranched stretches**: the ALGOL 60 → CPL → BCPL → B → C stretch scores well because it is long, not because each tie in it is busy. The table of the busiest individual ties is a better guide to where the traffic is. Second, **Fortran → ALGOL 60 carries half of all source-to-sink chains** (421 of 835), and **PL/I → C**, a weak tie, is the second busiest (26%). Much of the structure rests on these two single ties. Removing Fortran → ALGOL 60 leaves the main path unchanged from ALGOL 60 onward, and so does keeping only design, syntax and type ties. With strong ties only the spine is the same as far as Java, where four heirs (C#, Scala, Kotlin, Dart) tie.
'''

MD["rq1"] = r'''
## 6. RQ1: Which languages were the most influential?

### Direct influence
'''

MD["rq1b"] = r'''
### Influence domain and status

"Share of them reached" divides the influence domain by the number of languages created in or after the same year, so that a language is not credited simply for having had more time.
'''

MD["rq1_read"] = r'''
**Reading.** The three measures answer different questions.

- **Direct influence** is led by **LISP** and **C** (12 direct heirs each), then **ALGOL 60** (9) and a group at 8 (Java, Smalltalk, C#, Haskell). LISP's rank interval is the narrowest (1st to 2nd); C ranges from 1st to 3rd. Beyond the top three, the order is a matter of one or two ties, and the intervals overlap widely.
- **Influence domain** is led by **Fortran** (62 languages) and **ALGOL 60** (60), then **COBOL** (44) and **LISP** (43). Both leaders reach about 70% of the languages that came after them. ALGOL 60's rank is 1st or 2nd in 90% of the perturbed copies; Fortran's runs from 1st to 3rd. COBOL's reach runs mostly through PL/I and then C, a weak tie, which is why it is the least secure of the four.
- **CPL, BCPL and B** have large domains (35 to 37) but very wide intervals (up to 64th), because each is one link in a single chain (ALGOL 60 → CPL → BCPL → B → C) and losing one link cuts the reach of those before it. Structurally they are conduits, not sources.
- **Status** puts **Fortran, ALGOL 60 and LISP** in the first three places. ALGOL 60 and LISP stay in the top three in 90% or more of the copies.

**Answer to RQ1.** **Fortran, ALGOL 60 and LISP** are the most influential languages by reach and status, and **LISP and C** are the most often borrowed from directly. Fortran's lead over ALGOL 60 rests on its tie to ALGOL 60 (section 12): without it, Fortran falls to third on reach and seventh on status, and ALGOL 60 leads.
'''

MD["rq2"] = r'''
## 7. RQ2: Which languages borrowed the most?

Borrowing is where the quality of the record matters most. A language's in-degree counts the ties that someone wrote down, and some languages document their own heritage far more thoroughly than others (the Rust Reference lists its influences on one page). The table therefore shows how many distinct sources lie behind a language's ties, and how many come from its single largest source.
'''

MD["rq2_read"] = r'''
**Reading.** **Rust, Python and Julia** tie at the top with 10 direct sources each, followed by **S** (9) and, at 8, **Swift** and **Scala**. The three leaders are not alike. All 10 of Rust's ties come from a single page (the Rust Reference); Julia's come from three sources (8 from its own founding essay); Python's come from five, which makes its number the best documented. Across all languages, the rank correlation between in-degree and the number of ties from a single source is 0.94: **in-degree measures, to a large degree, how thoroughly a language documents its own influences**, and S, C++ and Rust show it most clearly. Python and Rust stay in the top five under all five specifications of section 12; Julia does in four.

**Ancestry** grows with how recent a language is, since a recent language can inherit the whole ancestry of its parents. Swift and Rust (50 ancestors each) lead, followed by Dart, Kotlin and TypeScript. The rankings are less secure than for direct borrowing: TypeScript's ancestry rests on few ties and drops out of the top five under four of five specifications.

**Answer to RQ2.** **Rust, Python and Julia are the three biggest borrowers of the record**, but their order is not meaningful, and the ranking says as much about documentation as about design. The claim that a single language is the network's great synthesizer does not survive the checks: Python is first (tied) in the full network, but it falls to fourth when only design, syntax and type ties are counted.
'''

MD["rq3"] = r'''
## 8. RQ3: Which languages sit between others?

**Betweenness** counts, for every pair of languages with a chain of influence between them, the share of their shortest chains that pass through a given language. A high score means that influence between other languages often travels through it. With time order respected, a chain through a language counts only if what it passed on was already there. This is a statement about position in the record, not about importance: a language can sit on many chains simply because it has many ties on both sides.
'''

MD["rq3_read"] = r'''
**Reading.** **Python** (181.8) comes first, followed by **C++** (168.5), **C#** (145.0), **C** (129.1) and **Java** (99.3). The positions of the five differ in how secure they are. **C++, C and Java** stay in the top five under every specification of section 12, and C++ and C in at least 90% of the perturbed copies. **C#** stays in four specifications of five. **Python** does in three: its betweenness rests heavily on its weak and later-version ties (library ties through pandas, features added in Python 2.0, and the ties from Python to C#, JavaScript, F# and Scala that were added in later versions). Counting only strong ties, Python falls from first to 39th; counting only ties present at first release, to 10th.

**Answer to RQ3.** **C++ and C are the languages that most reliably sit between others**, with Java close behind. Python's position as a connector is real in the full record but depends on ties that are weak or date from later versions, so it should not be stated without that qualification. The sociological reading is simple: the languages that connect are those with many ancestors and many heirs, which are the large, long-lived languages of the C line and of the object-oriented tradition.
'''

MD["rq4"] = r'''
## 9. RQ4: Do weak ties connect separate traditions?

Granovetter (1973) argued that weak ties, not strong ones, link otherwise separate social circles, because strong ties tend to form among people who already share contacts. Two checks translate the idea to this data:

- **Crossing family lines.** Does a weak tie more often join two different families than a strong tie does?
- **Structural bridging.** Granovetter's own idea is structural: a bridge is a tie whose two ends have no contacts in common. Does a weak tie more often have *no shared neighbor* (in the undirected graph) than a strong one?

Because every tie of a non-design kind is coded weak, and partly supported ties are more often weak, the comparison is repeated on design, syntax and type ties only, on supported ties only, and on both. "Shuffles as extreme" says how often shuffling the strength labels among ties at random gave a difference as large as the observed one, out of 2,000 shuffles. It is a baseline for the size of the difference, not a test on a sample.
'''

MD["rq4_read"] = r'''
**Reading.** The two checks give different answers.

- **Weak ties do cross family lines**: 78% of weak ties against 37% of strong ones, in all four versions of the comparison, and none of 2,000 shuffles gets close. Strong influence mostly stays within a tradition; weak influence mostly connects traditions.
- **Weak ties are not bridges in the structural sense.** They are *less* often without a shared neighbor than strong ties (31% against 53% among design, syntax and type ties; 5 of 2,000 shuffles are as extreme). A weak tie typically goes from a language to one that is already close to it in the network. A plausible mechanism: a language borrows its main idea from one parent (a strong tie) and a single feature from a relative of that parent or of its other sources (a weak tie), which closes a triangle. Strong ties form chains of descent (A → B → C), which contain no triangles.

**Answer to RQ4.** In this network, **weak ties cross traditions but do not bridge them**: they carry secondary borrowings between languages that are already connected, not the first link between separate parts of the network. The cross-family result is partly a coding pattern (an influence from outside a language's own tradition is, almost by definition, a secondary one), and the structural result is the opposite of what Granovetter's analogy would predict, so the analogy to his theory should be kept loose.
'''

MD["rq5"] = r'''
## 10. RQ5: Do the language families hold together?

The nine families on the map are curated display groups, mostly by domain of use, not groups found by the network. Do they still hold together more than chance would produce? Two baselines answer it, both from 1,000 random reassignments of the family labels to the languages (keeping the family sizes):

- the **share of ties that cross a family line**, which is high by construction when labels are random;
- **modularity** (Newman and Girvan 2004), which compares the share of ties inside families with the share expected if ties ignored family membership.

For each family, Krackhardt and Stern's (1988) **E-I index** compares ties to other families with ties inside: −1 means all ties stay inside the family, +1 means all go outside. The reference range is what the same family would show under random labels, which for small families is close to +1, so raw E-I values must not be read on their own.

The comparison is deliberately limited to the curated families. Algorithms that look for communities in the network (such as Louvain) would find groups of languages that borrow from each other, but those groups would follow lineages by construction, since lineages are what the ties are made of. A better fit than the families would say little.
'''

MD["rq5_read"] = r'''
**Reading.** **The families are more cohesive than chance would produce, but most of the influence still crosses them.**

- 58% of ties cross a family line; with random labels it would be about 87% (and never below 78% in 1,000 shuffles).
- The families' modularity is 0.26; random labels give −0.01 on average and never more than 0.06.
- **Eight of the nine families are more inward-looking than 95% of the random reassignments** (Figure 6, right). The ninth, "Other lineages", is a residual group, not a tradition, and sits inside the range, as it should. The most inward-looking are **Data & BI** (E-I 0.17, SQL and its dialects), **Teaching & visual** (0.20) and **C & systems** (0.27, with 32 ties inside the family, the heaviest cell in the matrix).

**Answer to RQ5.** The curated families are real groupings in the network: they hold together far more than random groups would. They are not closed worlds, however: even the C family, the largest and most self-contained, sends 11 ties to scripting and 6 to arrays and statistics.
'''

MD["rq6"] = r'''
## 11. RQ6: Is influence just a matter of being early?

An early language has more later languages that could borrow from it, so a large influence domain may simply reflect age. Two descriptive checks: how much of the variation in reach is explained by the year of creation alone (a regression of log(1 + influence domain) on year, then also on the number of direct heirs), and the **share of later languages reached**, which divides reach by the number of languages that could have been reached. These are descriptions of this record, not tests.
'''

MD["rq6_read"] = r'''
**Reading.** Age explains much of the reach: the rank correlation of influence domain with age is 0.69, and **the year of creation alone explains 46% of the variation** in log(1 + influence domain), rising to **80% once the number of direct heirs is added**. This is the sense in which "most influential" lists favor the past.

Looking at the *share* of later languages reached removes much of that advantage (its rank correlation with age falls to 0.29). **Fortran and ALGOL 60 still lead (70% each)**, ahead of **Java** (65%) and **C#** (58%), then COBOL, F#, Haskell and ALGOL 68 (about 50%). Java's and C#'s shares are high partly because few languages came after them (26 and 19), so a handful of heirs make a large share. At the other end, **APL** and **SQL** are old and have several direct heirs but reach a smaller share of the later languages than most languages of their era; their heirs stayed in their own niches.

**Answer to RQ6.** **Part of a language's reach is simply being early, but not all of it.** Fortran and ALGOL 60 lead on reach even after adjusting for time, while the apparent reach of young languages such as Java and C# comes largely from a small denominator.
'''

MD["robust"] = r'''
## 12. Robustness: do the results depend on how the network is drawn?

### Five ways of drawing the network

The headline uses all ties. Each alternative removes something that might distort the picture:

| Specification | Ties | What it removes |
|---|---|---|
| **All ties** (headline) | 218 | nothing |
| **Design, syntax, type** | 206 | library, implementation, platform and organizational ties, which are not design borrowing |
| **Strong only** | 104 | every weak tie |
| **First release only** | 186 | ties added in later versions, which are the ones that make chains run through features added decades later |
| **Supported only** | 200 | ties whose quoted sentence only partly supports them |

Figure 8 shows how the headline top eight on each measure fare under each version. Dark cells are high ranks. Languages with no ties at all in a version share a very low rank, hence large numbers.
'''

MD["fortran"] = r'''
### The Fortran → ALGOL 60 tie

This tie is the busiest in the network (half of all source-to-sink chains). In version 3 it is coded strong and supported, resting on Perlis's statement in the HOPL history of ALGOL that "ALGOL 58 was based on a model strongly derived from FORTRAN and its contemporaries". That sentence is about ALGOL 58 and names Fortran together with its contemporaries; Perlis also says that Fortran itself was unacceptable as a universal language. The tie is therefore well supported but not unambiguous, and it is worth knowing what depends on it. Below: Fortran's and ALGOL 60's positions with and without it.
'''

MD["stress"] = r'''
### Which results hold everywhere?

For every measure, the table takes the languages in the headline top five and records:

- in how many of the five specifications they stay in the top five (and which ones drop them);
- in what share of the perturbed copies they are in the top five, under the moderate and the severe setting of section 4.

A result is treated as **robust** when it holds in all five specifications and in at least 90% of the copies under the moderate setting.
'''

MD["robust_read"] = r'''
**Reading.** Three groups of results emerge.

**Robust (all five specifications, 90% or more of the moderate copies):**
- **LISP, C and ALGOL 60** in the top five for direct influence;
- **Fortran, ALGOL 60 and LISP** in the top five for influence domain and for status (Fortran's position is the least stable of the three: it falls to third on reach and seventh on status if its tie to ALGOL 60 is removed);
- **Python and Rust** in the top five for direct borrowing, and **Rust** in the top five by ancestry;
- **C++ and C** in the top five for betweenness.

**Close, but short of the rule:** Smalltalk (direct influence), Java (betweenness) and Kotlin (ancestry) hold in all five specifications but in fewer than 90% of the copies. Julia (borrowing), COBOL and ALGOL 68 (reach), and Swift and Dart (ancestry) each drop out under one specification; S and Swift (borrowing) under two; Scala under three.

**Fragile:**
- **Python and C#** among the top connectors: both drop out when only strong ties are used, and Python also when later-version ties are left out.
- **TypeScript** by ancestry, in the top five in only one specification.
- Any ranking *within* the groups above. The leading groups are stable; the order inside them is not.

**Which specification matters most.** Counting strong ties only changes the rankings most (rank correlation with the headline between 0.66 and 0.81, lowest for betweenness), while the other three versions stay between 0.89 and 1.00. The weak ties matter, but the leaders on the influence measures are strong-tie languages.

The severe setting (twice as many wrong ties and two and a half times as many missing ones) widens the intervals but does not move the robust results out of the top five in most copies; the last two columns of the table give the shares.
'''

MD["conclusions"] = r'''
## 13. Conclusions

1. **Fortran, ALGOL 60 and LISP are the most far-reaching languages**, by influence domain and by status, in every specification and in nearly every perturbed network. **LISP and C are the most often borrowed from directly.** Fortran's top place rests on its tie to ALGOL 60 (strong, supported by a historian's statement about ALGOL 58 and "its contemporaries"); without it, ALGOL 60 leads and Fortran falls to third.
2. **Biggest borrowers: Rust, Python and Julia, in no meaningful order.** The ranking partly reflects how thoroughly each language documents its own influences, so it cannot be read as a ranking of how much each language really borrowed. The claim that Python is the network's single great synthesizer does not survive.
3. **C++ and C are the most reliable connectors** (Java is close). Python and C# connect more in the full record than they do when weak ties or later-version ties are set aside.
4. **Weak ties cross traditions but are not bridges.** 78% of weak ties cross a family line, against 37% of strong ones; but weak ties are *more* embedded among shared neighbors than strong ties, not less. They are secondary borrowings between languages that already lie close to each other.
5. **The curated families hold together, but most influence crosses them.** Their modularity (0.26) is well above chance (−0.01), and eight of nine are more inward-looking than random labels would be; still, 58% of ties cross a family line.
6. **Part of reach is simply being early.** Year alone explains 46% of the variation in influence domain (80% with the number of direct heirs); relative to the number of later languages, Fortran and ALGOL 60 still lead, while Java's and C#'s high shares come from a small denominator.

**What changed from the analysis of version 2.** Fortran → ALGOL 60 is now documented rather than contested, so the caution that kept Fortran from being named as a top influence is relaxed, though it remains the single tie that most results hang on. Python's position as the top borrower and connector is weaker than it looked. And the earlier conclusion that families "are not communities" is reversed once chance is taken into account.
'''

MD["caveats"] = r'''
## 14. Caveats

- **Curation.** The 90 languages and 218 ties are a selection, made by a written rule. Languages left out, and intermediaries not drawn as nodes (ALGOL W, SASL, Alef), would change paths and rankings. Drawn intermediaries such as CPL, BCPL and B lengthen chains and add to the reach of early languages.
- **Ties are documented claims, and documentation is uneven.** Each tie rests on a cited source, but languages whose designers wrote detailed histories (Rust, Julia, C++, Python) have more recorded ties than languages that did not. In-degree and anything computed from it should be read with that in mind (section 7).
- **Languages change, nodes do not.** A language is one node over its whole life. Later-version ties and time order go a long way toward handling this, but a language's position is still the position of a language of 20 or 30 years, not of its first release.
- **Strength is a judgment about how substantial a borrowing was**, made with AI assistance, checked against the quoted sources, and with disputed cases decided by a human, plus a fixed rule for non-design ties. It is not frequency of contact, as in Granovetter's theory.
- **Uncertainty settings are assumptions.** The probabilities of wrong and missing ties are stated, not estimated. Missing ties are added at random between older and younger languages; real missing ties are not random (they are more likely among languages with sparse documentation).
- **Families are display categories**, drawn for the map, mostly by domain of use. "Other lineages" is a residual group.
- **No sampling inference.** The data are a record, not a sample; the shuffles describe what chance alone would produce, and the intervals describe uncertainty about which ties exist.
- **A small network.** With 90 nodes, one tie can move a rank a long way; only large and repeated differences are interpreted.
- **Influence is not quality or popularity.** A language can be widely used and rarely borrowed from, or the reverse. The health and outlook ratings that the map also shows are AI judgments and are deliberately not part of this analysis.
'''

MD["references"] = r'''
## References

- Batagelj, V. (2003). Efficient algorithms for citation network analysis. arXiv:cs/0309023.
- Bonacich, P. (1987). Power and centrality: A family of measures. *American Journal of Sociology*, 92(5), 1170–1182.
- Brandes, U. (2001). A faster algorithm for betweenness centrality. *Journal of Mathematical Sociology*, 25(2), 163–177.
- Brin, S., & Page, L. (1998). The anatomy of a large-scale hypertextual Web search engine. *Computer Networks and ISDN Systems*, 30(1–7), 107–117.
- Freeman, L. C. (1977). A set of measures of centrality based on betweenness. *Sociometry*, 40(1), 35–41.
- Granovetter, M. S. (1973). The strength of weak ties. *American Journal of Sociology*, 78(6), 1360–1380.
- Hummon, N. P., & Doreian, P. (1989). Connectivity in a citation network: The development of DNA theory. *Social Networks*, 11(1), 39–63.
- Katz, L. (1953). A new status index derived from sociometric analysis. *Psychometrika*, 18(1), 39–43.
- Krackhardt, D., & Stern, R. N. (1988). Informal networks and organizational crises: An experimental simulation. *Social Psychology Quarterly*, 51(2), 123–140.
- Liu, J. S., & Lu, L. Y. Y. (2012). An integrated approach for main path analysis: Development of the Hirsch index as an example. *Journal of the American Society for Information Science and Technology*, 63(3), 528–542.
- Newman, M. E. J., & Girvan, M. (2004). Finding and evaluating community structure in networks. *Physical Review E*, 69(2), 026113.
- Perlis, A. J. (1981). The American side of the development of ALGOL. In R. L. Wexelblat (Ed.), *History of Programming Languages* (pp. 75–91). Academic Press.
- Wasserman, S., & Faust, K. (1994). *Social Network Analysis: Methods and Applications*. Cambridge University Press.

*Software versions used for the results above:*
'''
