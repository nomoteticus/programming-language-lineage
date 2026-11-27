MD = {}

MD["title"] = r'''
# Who shaped whom? The influence network of programming languages

*A network analysis of 88 programming languages and 147 documented influence ties, from Fortran (1957) to Zig (2016).*

Programming languages are usually drawn as family trees: neat lines of parents and children. Influence does not stay inside families, though. A language may take its type system from one tradition, its syntax from a second and a library idea from a third. Seen this way, the history of programming languages looks less like a pedigree and more like a social network, and the vocabulary of social network analysis fits it well: centrality and status, brokers who join otherwise separate groups, cohesive subgroups, and the question of whether a prominent position reflects anything more than having arrived early.

This notebook asks six questions of the data behind the interactive map:

1. **Influence.** Which languages shaped the most others, directly and through their descendants?
2. **Borrowing.** Which languages drew on the most sources?
3. **Brokerage.** Which languages connect traditions that would otherwise be separate? Do *weak* ties do the bridging, as Granovetter (1973) argued for social ties?
4. **Cohesion.** Do the curated language families match the groups the network forms on its own?
5. **Age.** Is a language's reach more than a matter of having been early?
6. **Influence and health.** Are the most influential languages still alive? Are the biggest borrowers?
'''

MD["howto"] = r'''
> **Reading and running this notebook.** `network-analysis.ipynb` holds the code and its results. `network-analysis.html` is the same notebook rendered without code, for reading. To rerun it, install the packages in `requirements.txt` (at the root of the repository) and run all cells from the `notebooks/` folder; it takes about a minute. Every random step is seeded, so a rerun reproduces the numbers quoted in the text. Figures are also saved to `notebooks/figures/`.
'''

MD["setup"] = r'''
## 1. Setup
'''

MD["data"] = r'''
## 2. The data and the graph

Each **node** is a language. Each **tie** A → B records that B's designers borrowed something from A, backed by a cited source (the evidence record is in `data/edges.csv`). Ties are directed forward in time: from the source to the borrower.

Each tie also carries:

- a **strength**: *strong* (104 ties) for a substantial influence, *weak* (43) for a partial or resemblance-level one;
- a **verdict** on its evidence: *supported* (136) or *partly supported* (11, all of them weak ties);
- for 16 ties, a **later version** (the `since` column) when the borrowing happened after the language's first release, for example Python's list comprehensions from Haskell in Python 2.0.

The headline analysis uses **all 147 ties, unweighted**, which treats every documented influence alike. Two alternative specifications (strong ties only; strong = 1 and weak = 0.5) are reported in section 11.
'''

MD["glance"] = r'''
**The network at a glance.** The network is **sparse**: fewer than 2% of the possible ordered pairs are tied, and the average language has between three and four ties. Apart from Forth, which has no documented tie, all languages form **one connected component**. The graph is almost **acyclic**: the only two-way pair is PHP and Hack, because Hack later fed type features back into PHP 7.1.

Two numbers already say something about how ideas travel. First, only **8% of two-step chains are closed**: when A influenced B and B influenced C, A is rarely recorded as a direct influence on C. Influence mostly travels *through* intermediaries rather than skipping generations, so measures that follow paths, not just direct ties, matter here. Second, **almost half of all ties cross family lines**, so the families are far from closed worlds.
'''

MD["uncertainty"] = r'''
## 3. Measures, and how sure we can be

### Measures

| Question | Measure | What it counts |
|---|---|---|
| Who influenced the most? | **Direct influence** (outdegree) | Languages that borrowed directly from it. |
| | **Influence domain** | All later languages that can be reached from it by following ties forward, however many steps away (Wasserman and Faust 1994, ch. 5). |
| | **Status** (PageRank on reversed ties) | A language has high status when it is borrowed from by languages that are themselves borrowed from. This recursive idea goes back to Katz (1953) and Bonacich (1987); PageRank (Brin and Page 1998) is its best-known form. |
| Who borrowed the most? | **Direct borrowing** (indegree) | Languages it borrowed from directly. |
| | **Ancestry** | All earlier languages it descends from, directly or indirectly. |
| Who connects? | **Betweenness** (Freeman 1977) | The shortest influence paths between other languages that run through it. |
| | **Cross-family brokerage** (Gould and Fernandez 1989) | Chains A → B → C, with no direct tie A → C, in which B joins different families. |

### Uncertainty: why not confidence intervals?

The 88 languages and 147 ties are not a random sample from a larger population. They are a curated record, so the usual sampling-based confidence intervals and p-values do not apply. The real uncertainty is about **which ties belong in the record**: a weak, partly supported tie is less certain than a strong, well-documented one.

The notebook therefore uses one method throughout: an **evidence-weighted Monte Carlo** over ties. In each of 1,000 draws, every tie is kept or dropped at random, with a probability set by its evidence:

| Tie | Probability of keeping it |
|---|---|
| Strong (all supported) | 0.9 |
| Weak, supported | 0.6 |
| Weak, partly supported | 0.4 |

Every measure is recomputed on each of the 1,000 networks. The tables report each language's **rank on the full network**, its **median rank across the draws**, and the **90% interval** of its rank (the 5th to 95th percentile). A narrow interval means the position does not depend on any one uncertain tie; a wide one means it does.

Two points about reading these intervals. The full network is the most generous case, since every tie is present, so an interval need not be centered on the full-network value. And the probabilities are assumptions, not estimates: they encode "strong ties are very likely real, weak ones less so". The conclusions below rely only on large differences, which do not hinge on the exact values.
'''

MD["timeline"] = r'''
## 4. The shape of the network, and its main path

Figure 1 places every language at its year of creation, in a band for its family. Node size shows the influence domain.

The dark line is the network's **main path**. Main path analysis was developed by Hummon and Doreian (1989) to find the backbone of a citation network, the chain of papers through which a field's knowledge flowed. Each tie gets a **search path count**: the number of paths from a source (a language with no recorded parent) to a sink (one with no recorded heir) that pass through it (Batagelj 2003). The **global main path** is the source-to-sink chain with the highest total count (Liu and Lu 2012). It needs an acyclic graph, so it uses the 131 original-design ties, leaving out the 16 later-version ties.
'''

MD["timeline_read"] = r'''
**Reading Figure 1.** The main path runs **Fortran → ALGOL 60 → CPL → BCPL → B → C → C++ → Java → C#**, then on to PowerShell. This is the spine of the network: the ALGOL-to-C line and the object-oriented languages built on C. The last step matters little: C# has four heirs, and the tie to PowerShell carries few paths.

The first tie of the path deserves a warning. **Fortran → ALGOL 60 carries 55% of all source-to-sink paths**, by far the most load-bearing tie in the network, and it is also one of the 11 ties recorded as only partly supported: ALGOL was designed as a machine-independent alternative to Fortran, so Fortran was its precedent and foil more than its design source. Without this tie the main path simply starts at ALGOL 60 (section 11), but every measure of Fortran's reach changes a great deal.
'''

MD["rq1"] = r'''
## 5. RQ1: Which languages were the most influential?

### Direct influence
'''

MD["rq1b"] = r'''
### Influence domain and status
'''

MD["rq1_read"] = r'''
**Reading.** The three measures answer different questions, and they agree only in part.

- **Direct influence** is led by **C** (10 direct heirs), ranked first in every draw, then **LISP** (8), **SQL** (7), **Java** and **Fortran** (6 each). Direct influence rewards languages that many later designers looked at directly.
- **Influence domain** rewards early languages at the head of long chains. **Fortran** has the largest domain on the full network (55 later languages), but its median rank across the draws is only 9 and its interval runs from 1 to 21, because 35 of those 55 languages are reached only through the contested tie to ALGOL 60. **ALGOL 60** (46; ranked 1st or 2nd in 90% of draws) and **LISP** (35; 2nd to 7th) are the robust leaders.
- **CPL, BCPL and B** show a typical artifact of reach measures. Their domains are large (27 to 29), but their intervals stretch to rank 54, since each is a single link in one chain (ALGOL 60 → CPL → BCPL → B → C) and losing any link cuts their reach. Structurally they are conduits rather than sources (the method note makes the same point about drawn intermediaries).
- **Status** gives the clearest answer. **ALGOL 60** and **LISP** rank between 1st and 3rd in 90% of draws, followed by **C** (3rd to 7th).

**Answer to RQ1.** By the network's own measures, **ALGOL 60 and LISP are the most influential languages**, and **C** is the language most often borrowed from directly. Fortran heads the longest lineage only if its tie to ALGOL 60 is accepted as a design influence.
'''

MD["rq2"] = r'''
## 6. RQ2: Which languages borrowed the most?
'''

MD["rq2_read"] = r'''
**Reading.** **Python** has the most direct sources (8) and ranks first in every draw. Its sources span six families: ABC, C, C++, Modula-3, Icon, Haskell, and the R and SQL ideas behind pandas. **C++** follows (5; 2nd to 6th), then a large tie at four sources: Rust, Scala, Dart, JavaScript, Julia, R, Swift and Ruby, whose intervals overlap so much that their order means little.

**Ancestry** grows almost mechanically with date: a recent language inherits the whole ancestry of its parents. TypeScript, Dart, Kotlin and Swift lead (36 to 40 ancestors), but their intervals are wide because their ancestry often hangs on one or two ties. Python's ancestry is smaller (30) but much more secure (2nd to 8th): it is reached by many independent routes.

**Answer to RQ2.** **Python is the network's great synthesizer**, followed by C++. Many of Python's borrowings came after its first release, such as list comprehensions from Haskell, generators from Icon and data frames by way of pandas, so its position reflects a language that kept borrowing.
'''

MD["rq3"] = r'''
## 7. RQ3: Which languages connect separate traditions?

Two complementary views. **Betweenness** counts the shortest influence paths that run through a language: how much of the network's traffic it carries. **Brokerage roles** (Gould and Fernandez 1989) use the families. For every chain A → B → C with no direct tie A → C, the broker B plays one of five roles, depending on the families of the three languages:

| Role | Families | Interpretation |
|---|---|---|
| Liaison | A, B and C all different | links two traditions, neither of them its own |
| Gatekeeper | B and C the same, A different | brings outside ideas into its family |
| Representative | A and B the same, C different | carries its family's ideas out |
| Itinerant | A and C the same, B different | an outsider passing ideas within another family |
| Coordinator | all the same | brokerage within one family (not counted as cross-family) |
'''

MD["rq3_read"] = r'''
**Reading.** **Python** carries the most shortest paths (betweenness 129), ahead of **C** (110) and **C++** (92). Its rank is less secure than C++'s, though: across the draws C++ stays between 1st and 4th, while Python ranges from 1st to 13th, because several of its brokering ties are weak or later-version ties. B again owes its rank to its place in the C line.

The brokerage roles show *how* each language connects:

- **Python** is the network's main **liaison** (15 of its 28 cross-family chains), for instance carrying ideas from Icon and Haskell on to Julia, and from C++ and Modula-3 on to Scala. It is also a gatekeeper, bringing outside ideas into the scripting family.
- **Smalltalk** is a pure bridge between traditions: it carried LISP and Logo ideas into Objective-C, Java, Ruby and Dart.
- **C** and **Haskell** are pure **representatives**: they export their own family's ideas (C to Perl, AWK, PHP, Python and Stata; Haskell to Python, Scala, Swift, Rust and Excel formulas) but never stand between two other families.
- **Java** and **JavaScript** are mainly **gatekeepers**, bringing ideas from C++ and Smalltalk (for Java) and from Scheme and Self (for JavaScript) on to the newer languages of their own families.

**Answer to RQ3.** **Python, C++ and Smalltalk are the main connectors between traditions.** C++ holds its position most firmly; Python's broker role is the largest but leans more on weak ties.
'''

MD["weak"] = r'''
### Do weak ties bridge?

Granovetter (1973) argued that weak ties, not strong ones, link otherwise separate social circles. The data allow a simple check: do weak influence ties cross family lines more often than strong ones?
'''

MD["weak_read"] = r'''
**Reading.** They do, clearly: **two-thirds of weak ties (67%) cross family lines, against two-fifths of strong ties (39%)**. Strong influence mostly runs within a tradition, and weak influence mostly runs between traditions. The robustness check in section 11 points the same way: dropping weak ties changes the brokerage ranking more than any other measure.

Two cautions. "Strength" here describes how substantial the documented borrowing was, not the frequency of contact that Granovetter had in mind, so the parallel is an analogy, not a test of his theory. And part of the pattern may come from coding: an influence across traditions is harder to document in detail, so it may be more often rated weak.
'''

MD["rq4"] = r'''
## 8. RQ4: Do the language families hold together?

The nine families on the map are curated display groups, mostly by domain of use. Here they are compared with the network's own structure in three ways: the **mixing matrix** of ties between families; Krackhardt and Stern's (1988) **E-I index** for each family (external minus internal ties, divided by all ties: −1 means entirely inward-looking, +1 entirely outward-looking); and **community detection** with the Louvain method (Blondel et al. 2008), which finds the partition that maximizes **modularity** (Newman and Girvan 2004), compared with the families using normalized mutual information (NMI) and the adjusted Rand index.
'''

MD["rq4_read"] = r'''
**Reading.** The diagonal of Figure 5 is the heaviest part of the matrix for most families, but the off-diagonal flows are large. The **E-I index** sorts the families into two kinds:

- **Inward-looking:** **Data & BI** is the only family with more internal than external ties (E-I −0.08): SQL and its dialects form a world of their own. **C & systems** (0.10), **Teaching & visual** (0.11) and **Arrays & statistics** (0.13) are close to balanced.
- **Outward-looking:** **Lisp** (0.54) is a small family whose ideas were mostly exported, into ML, arrays, scripting and teaching languages. **ML & Haskell** (0.37), **Scripting & web** (0.40) and **JVM & .NET** (0.44) also trade mostly with other families. (The high value for *Other lineages*, 0.57, is expected: it is a residual group, not a tradition.)

**Communities.** The Louvain communities are considerably more modular than the families (modularity 0.56 against 0.37), and they agree with the families only moderately (NMI 0.45, with a 90% interval of 0.41 to 0.54 across the draws; adjusted Rand index 0.18). The communities follow **lineages** rather than domains of use. Examples: Modula-2, Oberon, Newsqueak, Modula-3 and Go form one group (Wirth's line leading to Go); Prolog, Erlang, F#, Elixir and Power Query M form another; Python sits with ISWIM, ML, Haskell and OCaml rather than with the scripting languages.

**Answer to RQ4.** **The families are only loosely cohesive.** They group languages by what they are used for; the network groups them by whom they learned from. Both are useful, but they are different maps.
'''

MD["rq5"] = r'''
## 9. RQ5: Is influence just a matter of being early?

An early language has more later languages that could borrow from it, so a large influence domain may simply reflect age. To separate the two, the observed network is compared with a **null model**: 1,000 randomized networks in which each language keeps its number of incoming and outgoing ties, and every tie still points forward in time, but who borrows from whom is shuffled. The shuffling uses repeated swaps of tie endpoints (a → b and c → d become a → d and c → b), the standard degree-preserving method (Maslov and Sneppen 2002), with the added rule that no tie may point back in time. As in section 4, it uses the 131 original-design ties, so that all ties respect time order.

For each language with at least one heir, the observed influence domain is compared with the distribution of its domain across the null networks. A language above the 95th percentile reaches further than its date and direct ties predict; one below the 5th reaches less far.
'''

MD["rq5_read"] = r'''
**Reading.** Position in time explains most of the reach: the rank correlation between the observed and the expected influence domain is 0.81, and **no language's reach exceeds what its date and number of direct heirs predict** (none is above the null's 95th percentile). The highest percentiles (about the 90th) belong to CPL, BCPL and B: one heir each, but that heir led to C. ALGOL 60 is also on the high side (82nd percentile).

Two languages fall **short** of their expected reach: **APL** (expected about 30 descendants, observed 6) and **SQL** (expected about 17, observed 5). Both had several direct heirs, but those heirs started few further lines: APL's descendants (J, K / q, S, Mathematica) stayed in the array niche, and SQL's heirs (T-SQL, PL/SQL, MDX, DAX, Cypher) lead almost nowhere: only MDX has an heir of its own. Their influence was broad but shallow: many children, few grandchildren. **LISP** comes close to the same pattern (6th percentile, just inside the null range): it has eight direct heirs but reaches 32 languages, against about 50 expected. Two of its heirs (Clojure and Mathematica) have no heirs of their own in the record, and the lines from the others often lead to the same languages.

**Answer to RQ5.** **Influence domain is largely a matter of when a language appeared and how many direct heirs it had.** Being early is most of what makes a language look far-reaching. That is why the direct and status measures in section 5, and the robust ranks, are better guides than raw reach. Note that the null model keeps each language's number of heirs fixed, so it tests reach *beyond* direct ties, not the direct ties themselves.
'''

MD["rq6"] = r'''
## 10. RQ6: Influence and health today

Each language has a **health** rating (dead, fading, alive, thriving). These ratings are **AI judgments**, each with a stated reason but no citation per rating, so they are weaker evidence than the ties. Health is scored 0 to 3 and compared with each network measure using Spearman rank correlations, first as they are and then **holding the year of creation constant** (a partial rank correlation), because both health and the network measures depend strongly on age. The intervals come from the same Monte Carlo draws and reflect uncertainty about the ties only, not about the health ratings.
'''

MD["rq6_read"] = r'''
**Reading.** At first sight influence and health pull in opposite directions. Languages with a large **influence domain** are more often dead (rank correlation −0.44), while languages that **borrowed** more are more often alive (+0.44 for direct borrowing, +0.46 for ancestry). The medians make the contrast concrete: the dead languages have a median influence domain of 16; the thriving ones, 3.

Most of this is **age**. Newer languages are rated healthier (+0.48 with year), and early languages have the largest domains. Holding the year of creation constant, status no longer relates to health (−0.03), and the link with influence domain shrinks to −0.19. What remains is a modest pattern on the other side: **languages that borrow more and broker more between families are rated somewhat healthier than others of the same age** (partial correlations between +0.17 and +0.26 for direct borrowing, ancestry and cross-family brokerage, depending on the draws), and they stay positive in at least 95% of the draws.

**Answer to RQ6.** **Influence does not secure survival.** ALGOL 60, LISP, CPL, BCPL, ISWIM and Simula are among the most influential languages and are all dead; their ideas live on in their heirs. Once age is taken into account, the languages judged healthiest today tend to be synthesizers and brokers rather than originators. The pattern is modest, and it rests on AI judgments of health, so it is a pointer for further work rather than a finding to lean on.
'''

MD["robust"] = r'''
## 11. Robustness

### Tie strength: three specifications

The headline treats all ties alike. Two alternatives: **strong ties only** (104 ties), and **weighted**, with strong ties counted as 1 and weak ties as 0.5 (for betweenness, a weak tie counts as a distance of 2). The table shows the rank correlation of each measure with the headline version, then the top five under each specification.
'''

MD["fortran"] = r'''
### The Fortran → ALGOL 60 tie

This single tie, recorded as partly supported, shapes several results above. Below: Fortran's position with and without it, and the main path without it.
'''

MD["robust_read"] = r'''
**Reading.** **Weighting makes almost no difference** (rank correlations of 0.96 or more): with only 43 weak ties, halving their weight rarely changes an order. **Dropping weak ties matters more** (0.72 to 0.85). Fortran leaves the top of the reach and status rankings, because its tie to ALGOL 60 is weak, and ALGOL 60 and LISP lead. Python stays the top borrower, but it drops out of the top five brokers, which become C, C++, Smalltalk, Java and Haskell: Python's brokerage rests largely on weak ties, consistent with section 7.

**Fortran** falls from 1st to 10th on influence domain (55 descendants to 20) and from 1st to 6th on status without its tie to ALGOL 60; in the Monte Carlo draws that drop the tie, its median rank on influence domain is 12. The main path keeps the same course from ALGOL 60 onwards.
'''

MD["conclusions"] = r'''
## 12. Conclusions

1. **ALGOL 60 and LISP are the most influential languages in the network**, on every measure of reach and status and across nearly all draws. **C** is the language most often borrowed from directly. Fortran's top place on reach rests on one contested tie, so it is not a safe headline.
2. **Python is the great synthesizer and the leading broker.** It has the most direct sources, the most cross-family brokerage and the highest betweenness, and it kept borrowing long after its first release. C++ and Smalltalk are the other major bridges between traditions, and C++'s position is the most secure.
3. **Weak ties bridge.** Two-thirds of weak ties cross family lines, against two-fifths of strong ones: strong influence mostly stays within a tradition, and weak influence connects traditions.
4. **Families are not communities.** The curated families group languages by use; the network's own communities follow lineages, and they fit the ties better.
5. **Reach is mostly seniority.** A language's influence domain is largely predicted by its date and its number of direct heirs. APL and SQL fall short of that prediction: many children, few grandchildren.
6. **Influence does not secure survival.** The most influential languages are disproportionately dead, mostly because they are old. Holding age constant, languages that borrow and broker more are judged slightly healthier.
'''

MD["caveats"] = r'''
## 13. Caveats

- **Curation.** The 88 languages and 147 ties are a selection. Languages left out (and intermediaries named only in tie labels, such as ALGOL W, SASL or Strongtalk) would change paths and rankings; drawn intermediaries such as CPL, BCPL and B lengthen chains and inflate the reach of early languages.
- **Age and censoring.** Early languages have had decades to gather heirs; recent ones have not. Section 9 addresses this for reach, but every "most influential" list still favors the past.
- **Ties are documented claims.** Each rests on a cited source, but evidence quality varies, and an undocumented influence is simply absent. The Monte Carlo probabilities are assumptions about how likely ties are to be real, not estimates.
- **Families are display categories.** They were drawn for the map, mostly by domain of use, and "Other lineages" is a residual group. Measures that depend on families (E-I index, brokerage roles) should be read with that in mind.
- **Health is an AI judgment**, with a stated reason but no citation for each rating. Section 10's results are indicative only.
- **No sampling inference.** The data are not a sample, so there are no p-values. The intervals describe uncertainty about which ties exist, nothing more.
- **A small network.** With 88 nodes, a few ties can move a rank a long way, which is why ranks are reported with intervals and only large differences are interpreted.
- **Influence is not quality or popularity.** A language can be widely used and rarely borrowed from, or the reverse.
'''

MD["references"] = r'''
## References

- Batagelj, V. (2003). Efficient algorithms for citation network analysis. arXiv:cs/0309023.
- Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. *Journal of Statistical Mechanics: Theory and Experiment*, P10008.
- Bonacich, P. (1987). Power and centrality: A family of measures. *American Journal of Sociology*, 92(5), 1170–1182.
- Brin, S., & Page, L. (1998). The anatomy of a large-scale hypertextual Web search engine. *Computer Networks and ISDN Systems*, 30(1–7), 107–117.
- Freeman, L. C. (1977). A set of measures of centrality based on betweenness. *Sociometry*, 40(1), 35–41.
- Gould, R. V., & Fernandez, R. M. (1989). Structures of mediation: A formal approach to brokerage in transaction networks. *Sociological Methodology*, 19, 89–126.
- Granovetter, M. S. (1973). The strength of weak ties. *American Journal of Sociology*, 78(6), 1360–1380.
- Hummon, N. P., & Doreian, P. (1989). Connectivity in a citation network: The development of DNA theory. *Social Networks*, 11(1), 39–63.
- Katz, L. (1953). A new status index derived from sociometric analysis. *Psychometrika*, 18(1), 39–43.
- Krackhardt, D., & Stern, R. N. (1988). Informal networks and organizational crises: An experimental simulation. *Social Psychology Quarterly*, 51(2), 123–140.
- Liu, J. S., & Lu, L. Y. Y. (2012). An integrated approach for main path analysis: Development of the Hirsch index as an example. *Journal of the American Society for Information Science and Technology*, 63(3), 528–542.
- Maslov, S., & Sneppen, K. (2002). Specificity and stability in topology of protein networks. *Science*, 296(5569), 910–913.
- Newman, M. E. J., & Girvan, M. (2004). Finding and evaluating community structure in networks. *Physical Review E*, 69(2), 026113.
- Wasserman, S., & Faust, K. (1994). *Social Network Analysis: Methods and Applications*. Cambridge University Press.

*Software versions used for the results above:*
'''
