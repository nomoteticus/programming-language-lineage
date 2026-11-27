# Code cells for the version 3 network-analysis notebook, keyed by name.
# The builder (build_nb.py) interleaves them with the markdown cells.
CODE = {}

# ------------------------------------------------------------------ setup
CODE["setup"] = r'''
from pathlib import Path
import heapq
from collections import defaultdict, deque
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib import patheffects
import seaborn as sns
from scipy.stats import rankdata

# The notebook lives in notebooks/; the data in data/.
DATA = next(p for p in [Path("../data"), Path("data")] if (p / "nodes.csv").exists())
FIGURES = DATA.parent / "notebooks" / "figures"
SAVE_FIGURES = True

SEED = 2026          # every random step below is seeded, so results are reproducible
N_DRAWS = 1000       # perturbed copies of the network for the uncertainty intervals
N_PERM = 1000        # label shuffles for the chance baselines

nodes = pd.read_csv(DATA / "nodes.csv")
edges = pd.read_csv(DATA / "edges.csv")
name = nodes.set_index("id")["name"]
year = nodes.set_index("id")["year"]
family = nodes.set_index("id")["family"]
ids = list(nodes.id)
pd.set_option("display.max_colwidth", None)

# The date of each tie: the year of the later version where there is one
# (Python 2.0, pandas 2008 ...), otherwise the year the borrowing language first appeared.
edges["t"] = edges.since_year.fillna(edges.to_id.map(year)).astype(int)
assert (edges.t >= edges.from_id.map(year)).all(), "a tie is dated before its source language existed"
print(f"{len(nodes)} languages, {len(edges)} influence ties "
      f"({(edges.strength == 'strong').sum()} strong, {(edges.strength == 'weak').sum()} weak)")
'''

CODE["style"] = r'''
# Family colors follow the interactive map, in an order checked for color-blind
# separation between neighbors; "Other lineages" is the neutral gray.
FAMILY_COLOR = {
    "Lisp": "#2f8a4f", "Arrays & statistics": "#1f62c4", "JVM & .NET": "#c4373f",
    "ML & Haskell": "#7448c8", "Scripting & web": "#008f8a", "Teaching & visual": "#8a6a12",
    "Data & BI": "#a8327e", "C & systems": "#c05a0c", "Other lineages": "#6b7280",
}
FAMILIES = list(FAMILY_COLOR)
INK, MUTED, GRID, EDGE = "#161a21", "#5a6170", "#e2e5ea", "#a3a9b4"
BLUE, ORANGE, NEUTRAL = "#2a78d6", "#eb6834", "#9aa1ac"
SEQ_BLUE = LinearSegmentedColormap.from_list(
    "seq_blue", ["#ffffff", "#cde2fb", "#86b6ef", "#2a78d6", "#184f95", "#0d366b"])

available = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in ["Inter", "Segoe UI", "Helvetica Neue", "Arial"] if f in available), "DejaVu Sans")
mpl.rcParams.update({
    "font.family": FONT, "font.size": 10, "text.color": INK,
    "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 12.5, "axes.titleweight": "semibold", "axes.titlelocation": "left",
    "axes.titlepad": 10, "axes.grid": False, "grid.color": GRID, "grid.linewidth": 0.8,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": MUTED, "ytick.labelcolor": INK,
    "xtick.major.size": 0, "ytick.major.size": 0, "legend.frameon": False,
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.dpi": 200,
    "savefig.bbox": "tight", "figure.dpi": 110,
})
%config InlineBackend.figure_formats = ["retina"]

def save(fig, stem):
    if SAVE_FIGURES:
        FIGURES.mkdir(parents=True, exist_ok=True)
        fig.savefig(FIGURES / f"{stem}.png")
'''

# ------------------------------------------------------------------ data and graph
CODE["graph"] = r'''
G = nx.DiGraph()
G.add_nodes_from(ids)
G.add_edges_from(zip(edges.from_id, edges.to_id))
U = G.to_undirected()

cross = edges.from_id.map(family) != edges.to_id.map(family)
cycles = [sorted(name[v] for v in c) for c in nx.strongly_connected_components(G) if len(c) > 1]
summary = pd.Series({
    "Languages (nodes)": G.number_of_nodes(),
    "Influence ties": G.number_of_edges(),
    "  strong / weak": f"{(edges.strength == 'strong').sum()} / {(edges.strength == 'weak').sum()}",
    "  design, syntax or type / other mechanisms": f"{edges.kind.isin(['design', 'syntax', 'type']).sum()} / {(~edges.kind.isin(['design', 'syntax', 'type'])).sum()}",
    "  supported / partly supported by the cited source": f"{(edges.verdict == 'supported').sum()} / {(edges.verdict == 'partly').sum()}",
    "  present at first release / added in a later version": f"{edges.since.isna().sum()} / {edges.since.notna().sum()}",
    "Density": round(nx.density(G), 3),
    "Mean ties per language (in + out)": round(2 * G.number_of_edges() / G.number_of_nodes(), 2),
    "Languages with no tie at all": ", ".join(name[v] for v in nx.isolates(G)),
    "Largest connected component": max(len(c) for c in nx.weakly_connected_components(G)),
    "Groups of languages that influence each other in a loop": "; ".join(" / ".join(c) for c in cycles),
}, name="value")
summary.to_frame()
'''

# ------------------------------------------------------------------ measures
CODE["measures_fn"] = r'''
# Influence is followed along ties in time order. A chain A -> B -> C counts only if the
# tie B -> C is no earlier than the tie A -> B: what B passed on to C must already have
# been in B. (Haskell's list comprehensions reached Python in 2.0, in 2000, so they could
# not have traveled on to a language that borrowed from Python in 1995.)
def reach(E):
    """For every language, the set of languages its influence can reach along time-respecting chains."""
    out = defaultdict(list)
    for u, w, t in zip(E.from_id, E.to_id, E.t):
        out[u].append((w, t))
    result = {}
    for s in ids:
        earliest = {s: -10**9}          # earliest moment influence from s can be at each language
        heap = [(-10**9, s)]
        while heap:
            a, u = heapq.heappop(heap)
            if a > earliest[u]:
                continue
            for w, t in out[u]:
                if t >= a and t < earliest.get(w, 10**9):
                    earliest[w] = t
                    heapq.heappush(heap, (t, w))
        result[s] = set(earliest) - {s}
    return result

def betweenness(E):
    """Betweenness (Freeman 1977) over the shortest time-respecting chains between every pair:
    for each pair of languages, the share of their shortest chains that pass through a language."""
    E = E.reset_index(drop=True)
    tail, head, when = E.from_id.tolist(), E.to_id.tolist(), E.t.tolist()
    ties_from = defaultdict(list)
    for i, u in enumerate(tail):
        ties_from[u].append(i)
    follow = [[f for f in ties_from[head[i]] if when[f] >= when[i]] for i in range(len(E))]
    score = defaultdict(float)
    for s in ids:
        first = ties_from[s]
        if not first:
            continue
        dist, paths, order, queue = {}, defaultdict(int), [], deque()
        for e in first:
            dist[e], paths[e] = 1, 1
            queue.append(e)
        while queue:                                   # breadth-first search over ties
            e = queue.popleft(); order.append(e)
            for f in follow[e]:
                if f not in dist:
                    dist[f] = dist[e] + 1; queue.append(f)
                if dist[f] == dist[e] + 1:
                    paths[f] += paths[e]
        nearest = defaultdict(lambda: 10**9)           # shortest chain length from s to each language
        for e in order:
            if head[e] != s and dist[e] < nearest[head[e]]:
                nearest[head[e]] = dist[e]
        n_short = defaultdict(int)                      # number of shortest chains from s to each language
        for e in order:
            if head[e] != s and dist[e] == nearest[head[e]]:
                n_short[head[e]] += paths[e]
        down = {}
        for e in reversed(order):                      # accumulate from the far end back (Brandes 2001)
            onward = sum(down[f] for f in follow[e] if dist[f] == dist[e] + 1)
            if head[e] != s:
                score[head[e]] += paths[e] * onward
            ends_here = head[e] != s and dist[e] == nearest[head[e]]
            down[e] = onward + (1 / n_short[head[e]] if ends_here else 0)
    return pd.Series({v: score.get(v, 0.0) for v in ids})

def measures(E):
    R = reach(E)
    m = pd.DataFrame(index=pd.Index(ids, name="id"))
    m["outdeg"] = E.groupby("from_id").size().reindex(ids).fillna(0)
    m["indeg"] = E.groupby("to_id").size().reindex(ids).fillna(0)
    m["domain"] = pd.Series({v: len(R[v]) for v in ids})
    anc = defaultdict(int)
    for s in ids:
        for v in R[s]:
            anc[v] += 1
    m["ancestry"] = pd.Series({v: anc[v] for v in ids})
    D = nx.DiGraph(); D.add_nodes_from(ids); D.add_edges_from(zip(E.from_id, E.to_id))
    m["status"] = pd.Series(nx.pagerank(D.reverse(copy=True), alpha=0.85))
    m["betweenness"] = betweenness(E)
    return m

LABEL = {
    "outdeg": "Direct influence (outdegree)", "domain": "Influence domain",
    "status": "Status (PageRank)", "indeg": "Direct borrowing (indegree)",
    "ancestry": "Ancestry", "betweenness": "Betweenness",
}
M = measures(edges)

def rank_desc(s):
    return s.rank(ascending=False, method="min").astype(int)    # tied values share a rank
'''

CODE["check"] = r'''
# Check the two time-respecting functions against networkx. On the ties present at first
# release every chain already runs forward in time, so the results must be identical.
orig = edges[edges.since.isna()]
D0 = nx.DiGraph(); D0.add_nodes_from(ids); D0.add_edges_from(zip(orig.from_id, orig.to_id))
assert nx.is_directed_acyclic_graph(D0)
R0 = reach(orig)
assert all(R0[v] == nx.descendants(D0, v) for v in ids)
nxb = pd.Series(nx.betweenness_centrality(D0, normalized=False))
assert np.allclose(betweenness(orig), nxb.reindex(ids))
print(f"Checked on the {len(orig)} first-release ties: reach and betweenness agree with networkx for all {len(ids)} languages.")

# What does time order change on the full network? Compare with ignoring dates.
naive_dom = pd.Series({v: len(nx.descendants(G, v)) for v in ids})
naive_anc = pd.Series({v: len(nx.ancestors(G, v)) for v in ids})
change = pd.DataFrame({
    "Influence domain, dates ignored": naive_dom, "Influence domain, time order": M.domain,
    "Ancestry, dates ignored": naive_anc, "Ancestry, time order": M.ancestry}, index=pd.Index(ids))
print("Rank correlation, dates ignored vs time order: "
      f"influence domain {np.corrcoef(rankdata(naive_dom), rankdata(M.domain))[0, 1]:.3f}, "
      f"ancestry {np.corrcoef(rankdata(naive_anc), rankdata(M.ancestry))[0, 1]:.3f}")
movers = list(dict.fromkeys(
    list((change["Ancestry, dates ignored"] - change["Ancestry, time order"]).sort_values(ascending=False).head(5).index)
    + list((change["Influence domain, dates ignored"] - change["Influence domain, time order"]).sort_values(ascending=False).head(4).index)))
change.loc[movers].rename(index=name).rename_axis("Language")
'''

# ------------------------------------------------------------------ uncertainty
CODE["montecarlo"] = r'''
# The record can be wrong in two directions: a recorded tie may not be a real design
# influence, and real ties may be missing. Each "draw" is a perturbed copy of the network:
#  - every tie is dropped with a probability set by its evidence (supported or partly supported);
#  - a number of extra ties are added between random pairs of languages, the older one as source.
# The probabilities are stated assumptions, not estimates. Two settings: "moderate" (the
# intervals in the tables) and "severe" (a stress test).
SETTINGS = {
    "moderate": dict(drop_supported=0.10, drop_partly=0.50, extra=0.10),
    "severe":   dict(drop_supported=0.20, drop_partly=0.60, extra=0.25),
}
yr = year.to_dict()
tied = set(zip(edges.from_id, edges.to_id)) | set(zip(edges.to_id, edges.from_id))
candidates = [(a, b) for a in ids for b in ids if a != b and yr[a] <= yr[b] and (a, b) not in tied]

def perturbed_draws(setting, seed):
    p = SETTINGS[setting]
    rng = np.random.default_rng(seed)
    keep_prob = np.where(edges.verdict == "supported", 1 - p["drop_supported"], 1 - p["drop_partly"])
    n_extra = round(p["extra"] * len(edges))
    fa = ((edges.from_id == "fortran") & (edges.to_id == "algol")).to_numpy()
    out = []
    for k in range(N_DRAWS):
        keep = rng.random(len(edges)) < keep_prob
        pick = rng.choice(len(candidates), n_extra, replace=False)
        extra = pd.DataFrame([(*candidates[i], yr[candidates[i][1]]) for i in pick],
                             columns=["from_id", "to_id", "t"])
        mk = measures(pd.concat([edges.loc[keep, ["from_id", "to_id", "t"]], extra]))
        mk["draw"], mk["fortran_algol_kept"] = k, bool(keep[fa][0])
        out.append(mk)
    d = pd.concat(out).reset_index()
    for col in LABEL:
        d[col + "_rank"] = d.groupby("draw")[col].rank(ascending=False, method="min")
    return d

MC = {s: perturbed_draws(s, SEED + i) for i, s in enumerate(SETTINGS)}
print(f"{N_DRAWS} draws per setting. Moderate: about "
      f"{(edges.verdict == 'supported').sum() * 0.9 + (edges.verdict == 'partly').sum() * 0.5:.0f} of {len(edges)} ties kept "
      f"and {round(0.10 * len(edges))} random ties added per draw.")
'''

CODE["ranktable_fn"] = r'''
def rank_interval(col, setting="moderate"):
    q = MC[setting].groupby("id")[col + "_rank"].quantile([0.05, 0.5, 0.95]).unstack()
    return q[0.5], q[0.05].astype(int).astype(str) + "–" + q[0.95].astype(int).astype(str)

def rank_table(col, k=10, extra=None):
    """Top k languages on one measure, with the median rank and 90% rank interval over the draws."""
    med, interval = rank_interval(col)
    t = pd.DataFrame({"Language": name, "Year": year, "Family": family})
    v = M[col]
    t[LABEL[col]] = v.round(3) if col == "status" else v.round(1) if col == "betweenness" else v.astype(int)
    for k_, v in (extra or {}).items():
        t[k_] = v
    t["Rank"] = rank_desc(M[col])
    t["Median rank (draws)"] = med.astype(int)
    t["90% rank interval"] = interval
    return t.sort_values(["Rank", "Median rank (draws)"]).head(k).reset_index(drop=True).rename(lambda i: i + 1)

def plot_rank_intervals(cols, k=12, title=None, stem=None):
    fig, axes = plt.subplots(1, len(cols), figsize=(4.3 * len(cols), 0.36 * k + 1.6))
    axes = np.atleast_1d(axes)
    shown = set()
    for ax, col in zip(axes, cols):
        q = MC["moderate"].groupby("id")[col + "_rank"].quantile([0.05, 0.5, 0.95]).unstack()
        obs = rank_desc(M[col])
        top = pd.DataFrame({"obs": obs, "med": q[0.5]}).sort_values(["obs", "med"]).head(k).index
        y = np.arange(len(top))[::-1]
        ax.hlines(y, q.loc[top, 0.05], q.loc[top, 0.95], color="#c9ced6", lw=3.2, capstyle="round", zorder=1)
        ax.scatter(obs[top], y, s=62, c=[FAMILY_COLOR[family[v]] for v in top],
                   edgecolor="white", linewidth=1.6, zorder=3)
        ax.set_yticks(y, [name[v] for v in top])
        ax.set_xlim(0, max(q.loc[top, 0.95].max(), 20) + 2)
        ax.xaxis.grid(True); ax.set_axisbelow(True)
        ax.spines["left"].set_visible(False)
        ax.set_xlabel("rank (1 = highest)")
        ax.set_title(LABEL[col], fontsize=11)
        shown |= {family[v] for v in top}
    handles = [Line2D([], [], marker="o", ls="", ms=7, mfc=FAMILY_COLOR[f], mec="white", label=f)
               for f in FAMILIES if f in shown]
    handles.append(Line2D([], [], color="#c9ced6", lw=3.2, solid_capstyle="round",
                          label="90% interval across 1,000 perturbed networks"))
    fig.legend(handles=handles, loc="lower center", ncol=min(len(handles), 5),
               bbox_to_anchor=(0.5, -0.06 - 0.03 * (len(handles) > 5)), fontsize=9)
    fig.tight_layout()
    if title:
        fig.suptitle(title, x=0.01, ha="left", fontsize=13.5, fontweight="semibold", y=1.0)
        fig.subplots_adjust(top=1 - 0.55 / fig.get_figheight())
    if stem:
        save(fig, stem)
    plt.show()
'''

# ------------------------------------------------------------------ main path
CODE["mainpath_fn"] = r'''
# Main path analysis (Hummon and Doreian 1989). It needs a graph without loops, so it uses the
# ties present at first release: they all run forward in time, which also keeps chains from
# running through a feature added decades later. Each tie gets a search path count (SPC):
# the number of chains from a source (a language with no recorded parent) to a sink (one with
# no recorded heir) that pass through it (Batagelj 2003).
def search_path_counts(D):
    order = list(nx.topological_sort(D))
    n_before, n_after = {}, {}
    for v in order:
        parents = list(D.predecessors(v))
        n_before[v] = sum(n_before[p] for p in parents) if parents else 1
    for v in reversed(order):
        heirs = list(D.successors(v))
        n_after[v] = sum(n_after[h] for h in heirs) if heirs else 1
    total = sum(n_after[v] for v in D if D.in_degree(v) == 0)
    return {(u, v): n_before[u] * n_after[v] for u, v in D.edges}, total

def global_main_paths(D):
    """Every source-to-sink chain with the highest total search path count (Liu and Lu 2012),
    so that an arbitrary tie-break between equally good endings is not hidden."""
    spc, total = search_path_counts(D)
    best = {}
    for v in nx.topological_sort(D):
        best[v] = max((best[u] + spc[(u, v)] for u in D.predecessors(v)), default=0)
    sinks = [v for v in D if D.out_degree(v) == 0]
    top = max(best[v] for v in sinks)
    found = []
    def walk_back(v, tail):
        parents = [u for u in D.predecessors(v) if best[u] + spc[(u, v)] == best[v]]
        if not parents:
            found.append(tail[::-1])
        for u in parents:
            walk_back(u, tail + [u])
    for v in sinks:
        if best[v] == top:
            walk_back(v, [v])
    return found, spc, total

def acyclic(E):
    D = nx.DiGraph(); D.add_edges_from(zip(E.from_id, E.to_id))
    assert nx.is_directed_acyclic_graph(D)
    return D

def show_paths(paths):
    stem = []
    while all(len(p) > len(stem) and p[:len(stem) + 1] == paths[0][:len(stem) + 1] for p in paths):
        stem = paths[0][:len(stem) + 1]
    ends = [name[p[len(stem)]] for p in paths if len(p) > len(stem)]
    text = " → ".join(name[v] for v in stem)
    return text + (" → {" + ", ".join(ends) + "}" if ends else "")

DAG = acyclic(orig)
main_paths, SPC, N_PATHS = global_main_paths(DAG)
rows = []
for label, E in [("All first-release ties", orig),
                 ("Without Fortran → ALGOL 60", orig[~((orig.from_id == "fortran") & (orig.to_id == "algol"))]),
                 ("Strong first-release ties only", orig[orig.strength == "strong"]),
                 ("Design, syntax and type first-release ties", orig[orig.kind.isin(["design", "syntax", "type"])])]:
    Dx = acyclic(E)
    paths, spc, total = global_main_paths(Dx)
    rows.append((label, len(E), total, show_paths(paths)))
pd.DataFrame(rows, columns=["Ties used", "Ties", "Source-to-sink chains", "Main path (equally good endings in braces)"]).set_index("Ties used")
'''

CODE["spc_table"] = r'''
share = SPC[("fortran", "algol")] / N_PATHS
print(f"{N_PATHS} source-to-sink chains in all. Fortran → ALGOL 60 carries {SPC[('fortran', 'algol')]} of them ({share:.0%}).")
spc_table = (pd.DataFrame([(name[u], name[v], s, s / N_PATHS) for (u, v), s in SPC.items()],
                          columns=["From", "To", "Search path count", "Share of all chains"])
             .sort_values("Search path count", ascending=False).head(8).reset_index(drop=True))
spc_table["Share of all chains"] = spc_table["Share of all chains"].map("{:.0%}".format)
spc_table.rename(lambda i: i + 1)
'''

CODE["timeline_plot"] = r'''
def timeline_layout(char_w=0.3, pad=1.4):
    """x = year; each family gets a band, split into lanes so that labels never overlap."""
    pos, ticks, y = {}, [], 0.0
    for f in FAMILIES:
        lanes, lane_of = [], {}
        for r in nodes[nodes.family == f].sort_values("year").itertuples():
            start, end = r.year - 0.6, r.year + pad + char_w * len(r.name)
            for i, free_at in enumerate(lanes):
                if free_at <= start:
                    lanes[i] = end; lane_of[r.id] = i; break
            else:
                lanes.append(end); lane_of[r.id] = len(lanes) - 1
        for v, i in lane_of.items():
            pos[v] = (year[v], -(y + i))
        ticks.append((-(y + (len(lanes) - 1) / 2), f, -(y - 0.5), -(y + len(lanes) - 0.5)))
        y += len(lanes) + 1.0
    return pos, ticks

pos, ticks = timeline_layout()
size = 14 + 5.5 * M["domain"]
on_path = {(u, v) for p in main_paths for u, v in zip(p, p[1:])}
on_path_nodes = {v for p in main_paths for v in p}

fig, ax = plt.subplots(figsize=(15, 11.5))
for i, (_, f, top_, bottom_) in enumerate(ticks):
    if i % 2 == 0:
        ax.axhspan(bottom_ - 0.2, top_ + 0.2, color="#f6f7f9", zorder=0, lw=0)
for _, r in edges.iterrows():
    u, v = r.from_id, r.to_id
    main = (u, v) in on_path
    ax.annotate("", xy=pos[v], xytext=pos[u], zorder=3 if main else 1,
                arrowprops=dict(arrowstyle="-|>", mutation_scale=7 if main else 5,
                                color=INK if main else EDGE,
                                alpha=1 if main else (0.75 if r.strength == "strong" else 0.4),
                                lw=2.2 if main else (0.9 if r.strength == "strong" else 0.6),
                                ls="-" if pd.isna(r.since) else (0, (3, 2)),
                                connectionstyle="arc3,rad=0.12",
                                shrinkA=np.sqrt(size[u]) / 2, shrinkB=np.sqrt(size[v]) / 2 + 1))
xy = np.array([pos[v] for v in nodes.id])
ax.scatter(xy[:, 0], xy[:, 1], s=size[nodes.id], c=[FAMILY_COLOR[f] for f in nodes.family],
           edgecolor="white", linewidth=1.3, zorder=4)
for v in nodes.id:
    x, y_ = pos[v]
    ax.text(x + 0.45 + np.sqrt(size[v]) * 0.035, y_, name[v], va="center", fontsize=7.6,
            color=INK, zorder=5, fontweight="semibold" if v in on_path_nodes else "normal",
            path_effects=[patheffects.withStroke(linewidth=2.6, foreground="white")])
ax.set_yticks([t[0] for t in ticks], [t[1] for t in ticks])
ax.set_xlim(1954, 2024)
ax.set_xticks(range(1960, 2021, 10))
ax.xaxis.grid(True); ax.set_axisbelow(True)
ax.spines[["left", "bottom"]].set_visible(False)
ax.set_title("Figure 1. The influence network on a timeline", fontsize=14, pad=14)
handles = [Line2D([], [], color=EDGE, lw=0.9, alpha=0.75, label="strong tie"),
           Line2D([], [], color=EDGE, lw=0.6, alpha=0.4, label="weak tie"),
           Line2D([], [], color=EDGE, lw=0.9, alpha=0.75, ls=(0, (3, 2)), label="added in a later version"),
           Line2D([], [], color=INK, lw=2.2, label="main path"),
           Line2D([], [], marker="o", ls="", ms=4, mfc=MUTED, mec="white", label="small influence domain"),
           Line2D([], [], marker="o", ls="", ms=13, mfc=MUTED, mec="white", label="large influence domain")]
ax.legend(handles=handles, loc="upper center", fontsize=8.5, ncol=6, bbox_to_anchor=(0.5, -0.04))
ax.text(0.0, -0.085, "Node size: influence domain (languages reachable along time-respecting chains). "
        "Main path: the chain carrying the most source-to-sink paths, on first-release ties.",
        transform=ax.transAxes, fontsize=8.5, color=MUTED)
save(fig, "network-timeline")
plt.show()
'''

# ------------------------------------------------------------------ RQ1 influence
CODE["outdeg_table"] = r'''
rank_table("outdeg")
'''
CODE["influence_table"] = r'''
later = pd.Series({v: int(((year >= year[v]) & (year.index != v)).sum()) for v in ids})   # languages created in or after its year
rank_table("domain", extra={"Later languages": later, "Share of them reached": (M.domain / later).round(2)})
'''
CODE["status_table"] = r'''
rank_table("status")
'''
CODE["influence_plot"] = r'''
plot_rank_intervals(["outdeg", "domain", "status"],
                    title="Figure 2. The most influential languages, with 90% rank intervals",
                    stem="network-influence-ranks")
'''

# ------------------------------------------------------------------ RQ2 borrowing
CODE["borrow_tables"] = r'''
sources = edges.groupby("to_id").url.nunique().reindex(ids).fillna(0).astype(int)
biggest = edges.groupby("to_id").url.agg(lambda s: s.value_counts().iloc[0]).reindex(ids).fillna(0).astype(int)
t = rank_table("indeg", k=12, extra={"Distinct sources": sources, "Ties from its largest source": biggest})
print("Rank correlation between a language's in-degree and the number of its ties that come from one single source: "
      f"{np.corrcoef(rankdata(M.indeg), rankdata(biggest))[0, 1]:.2f}")
t
'''
CODE["ancestry_table"] = r'''
rank_table("ancestry")
'''
CODE["borrow_plot"] = r'''
plot_rank_intervals(["indeg", "ancestry"], k=12,
                    title="Figure 3. The biggest borrowers, with 90% rank intervals",
                    stem="network-borrower-ranks")
'''

# ------------------------------------------------------------------ RQ3 connectors
CODE["broker_tables"] = r'''
rank_table("betweenness", k=12)
'''
CODE["broker_plot"] = r'''
plot_rank_intervals(["betweenness"], k=12,
                    title="Figure 4. The languages that most often sit between others, with 90% rank interval",
                    stem="network-betweenness-ranks")
'''

# ------------------------------------------------------------------ RQ4 weak ties
CODE["weak_ties"] = r'''
# Granovetter (1973): weak ties link circles that would otherwise stay apart, and they are
# not embedded in shared acquaintances. Two checks: does a weak tie cross family lines more
# often, and does it lack common neighbors (the structural idea of a bridge)?
nbrs = {v: set(U[v]) for v in U}
e = edges.assign(across=cross.to_numpy(),
                 no_shared=[len(nbrs[a] & nbrs[b]) == 0 for a, b in zip(edges.from_id, edges.to_id)])
subsets = {
    "All ties": e,
    "Design, syntax and type ties": e[e.kind.isin(["design", "syntax", "type"])],
    "Supported ties": e[e.verdict == "supported"],
    "Design, syntax and type, supported": e[e.kind.isin(["design", "syntax", "type"]) & (e.verdict == "supported")],
}
rng_w = np.random.default_rng(SEED + 5)
def gap_and_chance(d, col):
    obs = d.groupby("strength")[col].mean()
    gap = obs["weak"] - obs["strong"]
    s, x = d.strength.to_numpy(), d[col].to_numpy()
    shuffled = []
    for _ in range(N_PERM * 2):
        p = rng_w.permutation(s)
        shuffled.append(x[p == "weak"].mean() - x[p == "strong"].mean())
    shuffled = np.array(shuffled)
    return gap, (np.abs(shuffled) >= abs(gap)).mean()

rows = []
for label, d in subsets.items():
    g = d.groupby("strength")
    gap_c, p_c = gap_and_chance(d, "across")
    gap_s, p_s = gap_and_chance(d, "no_shared")
    rows.append((label, g.size()["strong"], g.size()["weak"],
                 f"{g.across.mean()['strong']:.0%}", f"{g.across.mean()['weak']:.0%}", f"{p_c * 2 * N_PERM:.0f} of {2 * N_PERM:,}",
                 f"{g.no_shared.mean()['strong']:.0%}", f"{g.no_shared.mean()['weak']:.0%}", f"{p_s * 2 * N_PERM:.0f} of {2 * N_PERM:,}"))
WT = pd.DataFrame(rows, columns=pd.MultiIndex.from_tuples([
    ("", "Ties"), ("Number of ties", "strong"), ("Number of ties", "weak"),
    ("Cross a family line", "strong"), ("Cross a family line", "weak"), ("Cross a family line", "shuffles as extreme"),
    ("No shared neighbor", "strong"), ("No shared neighbor", "weak"), ("No shared neighbor", "shuffles as extreme")]))
WT.set_index(("", "Ties")).rename_axis("")
'''
CODE["weak_plot"] = r'''
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.9), sharey=True)
d = subsets["Design, syntax and type ties"]
labels = ["Cross a family line", "Have no shared neighbor"]
for ax, col, title in zip(axes, ["across", "no_shared"], labels):
    vals = d.groupby("strength")[col].mean().reindex(["strong", "weak"])
    counts = d.groupby("strength").size().reindex(["strong", "weak"])
    ax.bar([0, 1], vals * 100, color=[BLUE, ORANGE], width=0.55)
    for i, (v, n) in enumerate(zip(vals, counts)):
        ax.text(i, v * 100 + 2, f"{v:.0%}", ha="center", fontsize=11, fontweight="semibold")
        ax.text(i, 3, f"n = {n}", ha="center", fontsize=8.5, color="white")
    ax.set_xticks([0, 1], ["strong ties", "weak ties"]); ax.tick_params(axis="x", labelcolor=INK)
    ax.set_title(title, fontsize=11); ax.set_ylim(0, 100)
    ax.yaxis.grid(True); ax.set_axisbelow(True); ax.spines["left"].set_visible(False)
axes[0].set_ylabel("share of ties (%)")
fig.suptitle("Figure 5. Weak ties cross family lines, but they are not bridges (design, syntax and type ties)",
             x=0.01, ha="left", fontsize=13, fontweight="semibold", y=1.02)
fig.tight_layout()
save(fig, "network-weak-ties")
plt.show()
'''

# ------------------------------------------------------------------ RQ5 families
CODE["families"] = r'''
# Do the nine curated families hold together more than chance would produce? Compare with
# the same nine family sizes assigned at random to the languages (1,000 shuffles).
fam_code = {f: i for i, f in enumerate(FAMILIES)}
lab = np.array([fam_code[family[v]] for v in ids])
pos_of = {v: i for i, v in enumerate(ids)}
a_idx = edges.from_id.map(pos_of).to_numpy(); b_idx = edges.to_id.map(pos_of).to_numpy()

def modularity_of(labels):
    parts = [{ids[i] for i in np.flatnonzero(labels == k)} for k in range(len(FAMILIES))]
    return nx.community.modularity(U, [p for p in parts if p])

def ei_index(labels):
    fa, fb = labels[a_idx], labels[b_idx]
    out = []
    for k in range(len(FAMILIES)):
        internal = ((fa == k) & (fb == k)).sum()
        external = (((fa == k) | (fb == k)) & (fa != fb)).sum()
        out.append((external - internal) / (external + internal) if external + internal else np.nan)
    return np.array(out)

rng_f = np.random.default_rng(SEED + 6)
null_q, null_cross, null_ei = [], [], []
for _ in range(N_PERM):
    p = rng_f.permutation(lab)
    null_q.append(modularity_of(p))
    null_cross.append((p[a_idx] != p[b_idx]).mean())
    null_ei.append(ei_index(p))
null_ei = np.array(null_ei)
obs_q, obs_cross, obs_ei = modularity_of(lab), (lab[a_idx] != lab[b_idx]).mean(), ei_index(lab)

fit = pd.DataFrame({
    "Observed": [round(obs_q, 2), f"{obs_cross:.0%}"],
    "Random family labels, mean": [round(np.mean(null_q), 2), f"{np.mean(null_cross):.0%}"],
    "Random family labels, most extreme of 1,000": [f"{max(null_q):.2f} (highest)", f"{min(null_cross):.0%} (lowest)"],
}, index=["Modularity of the families", "Share of ties that cross a family line"])
fit
'''
CODE["families_plot"] = r'''
mix = pd.crosstab(edges.from_id.map(family), edges.to_id.map(family)).reindex(index=FAMILIES, columns=FAMILIES, fill_value=0)
fig, axes = plt.subplots(1, 2, figsize=(16, 6.4), gridspec_kw={"width_ratios": [1.05, 1]})
ax = axes[0]
sns.heatmap(mix, ax=ax, cmap=SEQ_BLUE, annot=mix.where(mix > 0).fillna(0).astype(int).astype(str).replace("0", ""),
            fmt="", cbar=False, linewidths=2, linecolor="white", square=True, annot_kws={"fontsize": 9})
for t in ax.texts:
    t.set_color("white" if t.get_text() and int(t.get_text()) >= 8 else INK)
ax.set_xlabel("borrowing family"); ax.set_ylabel("source family")
ax.tick_params(axis="x", rotation=40, labelcolor=INK)
plt.setp(ax.get_xticklabels(), ha="right")
ax.set_title("Ties between families (diagonal = within a family)")

ax = axes[1]
order = np.argsort(obs_ei)
y = np.arange(len(FAMILIES))
lo, hi = np.nanquantile(null_ei, [0.05, 0.95], axis=0)
ax.hlines(y, lo[order], hi[order], color="#c9ced6", lw=7, capstyle="round", zorder=1)
ax.scatter(obs_ei[order], y, s=70, c=[FAMILY_COLOR[FAMILIES[i]] for i in order], edgecolor="white", linewidth=1.6, zorder=3)
ax.axvline(0, color=MUTED, lw=0.8)
ax.set_yticks(y, [FAMILIES[i] for i in order])
ax.set_xlim(-0.2, 1.05)
ax.xaxis.grid(True); ax.set_axisbelow(True); ax.spines["left"].set_visible(False)
ax.set_xlabel("E-I index: −1 = all ties inside the family, +1 = all ties outside")
ax.set_title("E-I index, against random family labels")
ax.legend(handles=[Line2D([], [], color="#c9ced6", lw=7, label="5th to 95th percentile of 1,000 shuffles")],
          loc="upper left", fontsize=8.5, bbox_to_anchor=(0, 0.93))
fig.suptitle("Figure 6. Families hold together more than chance, but most ties still cross them",
             x=0.01, ha="left", fontsize=13.5, fontweight="semibold", y=1.01)
fig.tight_layout()
save(fig, "network-families")
plt.show()
EI = pd.DataFrame({"Languages": [(family == f).sum() for f in FAMILIES],
                   "E-I index": obs_ei.round(2),
                   "Random labels: median": np.nanmedian(null_ei, axis=0).round(2),
                   "Random labels: 5th–95th percentile": [f"{a:.2f} to {b:.2f}" for a, b in zip(lo, hi)]},
                  index=FAMILIES).sort_values("E-I index")
EI.rename_axis("Family")
'''

# ------------------------------------------------------------------ RQ6 age
CODE["age"] = r'''
# How much of "influence domain" is simply having been early?
ly = np.log1p(M.domain.to_numpy())
def r_squared(X):
    X = np.column_stack([np.ones(len(ids))] + X)
    resid = ly - X @ np.linalg.lstsq(X, ly, rcond=None)[0]
    return 1 - resid.var() / ly.var()
r2_year = r_squared([year.to_numpy() - 1990])
r2_both = r_squared([year.to_numpy() - 1990, np.log1p(M.outdeg.to_numpy())])
rho = np.corrcoef(rankdata(M.domain), rankdata(-year))[0, 1]
print(f"Rank correlation of influence domain with age: {rho:.2f}")
print(f"Share of the variation in log(1 + influence domain) explained by year of creation alone: {r2_year:.0%}; "
      f"by year and number of direct heirs: {r2_both:.0%}")

# Reach relative to the number of later languages that could have borrowed
AGEDF = pd.DataFrame({"Language": name, "Year": year, "Influence domain": M.domain.astype(int),
                      "Later languages": later, "Share of them reached": (M.domain / later).round(2)})
AGEDF = AGEDF[AGEDF["Later languages"] >= 15]
print(f"Among the {len(AGEDF)} languages with at least 15 later languages, the share reached ranges "
      f"from {AGEDF['Share of them reached'].min():.0%} to {AGEDF['Share of them reached'].max():.0%}; "
      f"its rank correlation with age is {np.corrcoef(rankdata(AGEDF['Share of them reached']), rankdata(-AGEDF.Year))[0, 1]:.2f}.")
AGEDF.sort_values("Share of them reached", ascending=False).head(8).reset_index(drop=True).rename(lambda i: i + 1)
'''
CODE["age_plot"] = r'''
fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.6))
ax = axes[0]
ax.scatter(year, M.domain, s=46, c=[FAMILY_COLOR[family[v]] for v in ids], edgecolor="white", linewidth=1.3, zorder=3)
label_ids = list(M.domain.sort_values(ascending=False).index[:6]) + ["python", "swift", "go", "rust", "sql", "apl", "java"]
offsets = {"algol": (6, -10, "left"), "cobol": (6, -10, "left"), "lisp": (-6, 5, "right"), "cpl": (6, -10, "left"),
           "go": (-6, -11, "right"), "rust": (6, -11, "left"), "swift": (-4, 8, "right")}
for v in dict.fromkeys(label_ids):
    dx, dy, ha = offsets.get(v, (6, 4, "left"))
    ax.annotate(name[v], (year[v], M.domain[v]), xytext=(dx, dy), textcoords="offset points",
                fontsize=8.5, color=INK, ha=ha)
ax.set_xlabel("year of creation"); ax.set_ylabel("influence domain (languages reached)")
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.set_title("Reach falls with age")

ax = axes[1]
d = AGEDF.sort_values("Year")
ax.scatter(d.Year, d["Share of them reached"] * 100, s=50, c=[FAMILY_COLOR[family[v]] for v in d.index],
           edgecolor="white", linewidth=1.3, zorder=3)
off2 = {"fortran": (6, -12), "lisp": (6, -12), "apl": (6, -12), "sql": (6, -12)}
for v in d.index:
    if d.loc[v, "Share of them reached"] >= 0.5 or v in ["lisp", "apl", "sql", "python", "smalltalk"]:
        ax.annotate(name[v], (d.loc[v, "Year"], d.loc[v, "Share of them reached"] * 100), xytext=off2.get(v, (6, 4)),
                    textcoords="offset points", fontsize=8.5, color=INK)
ax.set_xlabel("year of creation"); ax.set_ylabel("share of later languages reached (%)")
ax.yaxis.grid(True); ax.set_axisbelow(True)
ax.set_title("Share of later languages reached (languages with 15 or more later ones)")
fig.suptitle("Figure 7. Part of influence is simply being early",
             x=0.01, ha="left", fontsize=13.5, fontweight="semibold", y=1.02)
fig.tight_layout()
save(fig, "network-age")
plt.show()
'''

# ------------------------------------------------------------------ robustness
CODE["specs"] = r'''
# Five ways of drawing the network. The headline uses all ties; the others each remove one
# thing the reviews of version 2 worried about.
SPECS = {
    "All ties": edges,
    "Design, syntax, type": edges[edges.kind.isin(["design", "syntax", "type"])],
    "Strong only": edges[edges.strength == "strong"],
    "First release only": edges[edges.since.isna()],
    "Supported only": edges[edges.verdict == "supported"],
}
SM = {k: (M if k == "All ties" else measures(v)) for k, v in SPECS.items()}
print("Ties in each specification: " + "; ".join(f"{k} {len(v)}" for k, v in SPECS.items()))

agree = pd.DataFrame({k: [np.corrcoef(rankdata(M[c]), rankdata(SM[k][c]))[0, 1] for c in LABEL]
                      for k in list(SPECS)[1:]}, index=[LABEL[c] for c in LABEL]).round(2)
agree.rename_axis("Rank correlation with the headline")
'''
CODE["specs_plot"] = r'''
fig, axes = plt.subplots(2, 3, figsize=(15, 8.2))
cmap = LinearSegmentedColormap.from_list("rk", ["#0d366b", "#2a78d6", "#cde2fb", "#ffffff"])
for ax, c in zip(axes.ravel(), LABEL):
    top = rank_desc(M[c]).sort_values(kind="stable").index[:8]
    grid = pd.DataFrame({k: rank_desc(SM[k][c]).reindex(top) for k in SPECS}).rename(index=name)
    sns.heatmap(grid, ax=ax, cmap=cmap, vmin=1, vmax=25, annot=grid.astype(int).astype(str), fmt="", cbar=False,
                linewidths=1.5, linecolor="white", annot_kws={"fontsize": 9})
    for t in ax.texts:
        t.set_color("white" if int(t.get_text()) <= 4 else INK)
    ax.set_title(LABEL[c], fontsize=11)
    ax.tick_params(axis="x", rotation=30, labelcolor=INK, labelsize=8.5); plt.setp(ax.get_xticklabels(), ha="right")
    ax.tick_params(axis="y", rotation=0)
    ax.set_ylabel("")
fig.suptitle("Figure 8. Rank of the headline top eight under five ways of drawing the network (1 = highest)",
             x=0.01, ha="left", fontsize=13.5, fontweight="semibold", y=1.0)
fig.tight_layout()
save(fig, "network-robustness")
plt.show()
'''
CODE["fortran"] = r'''
no_fa = edges[~((edges.from_id == "fortran") & (edges.to_id == "algol"))]
M_wo = measures(no_fa)
fortran = pd.DataFrame({
    "With the tie": [M.loc["fortran", "domain"], rank_desc(M["domain"])["fortran"], rank_desc(M["status"])["fortran"],
                     M.loc["algol", "domain"], rank_desc(M["domain"])["algol"]],
    "Without the tie": [M_wo.loc["fortran", "domain"], rank_desc(M_wo["domain"])["fortran"], rank_desc(M_wo["status"])["fortran"],
                        M_wo.loc["algol", "domain"], rank_desc(M_wo["domain"])["algol"]],
}, index=["Fortran: influence domain", "Fortran: rank on influence domain", "Fortran: rank on status",
          "ALGOL 60: influence domain", "ALGOL 60: rank on influence domain"]).astype(int)
mc_wo = MC["moderate"][(MC["moderate"].id == "fortran") & (~MC["moderate"].fortran_algol_kept)]
print(f"In the {len(mc_wo)} perturbed networks (of {N_DRAWS}) that lose the tie, Fortran's influence-domain rank has "
      f"median {mc_wo.domain_rank.median():.0f} (90% interval {mc_wo.domain_rank.quantile(0.05):.0f}–{mc_wo.domain_rank.quantile(0.95):.0f}).")
fortran
'''
CODE["stress"] = r'''
# For each measure, the languages in the headline top five. In how many of the five
# specifications do they stay in the top five, and in what share of the perturbed
# networks of each setting?
ranks = {s_: {c: MC[s_].pivot(index="draw", columns="id", values=c + "_rank") for c in LABEL} for s_ in SETTINGS}
rows = []
for c in LABEL:
    head = rank_desc(M[c])
    for v in head[head <= 5].sort_values(kind="stable").index:
        out_of = [k for k in SPECS if rank_desc(SM[k][c])[v] > 5]
        rows.append((LABEL[c], name[v], head[v], f"{len(SPECS) - len(out_of)} of {len(SPECS)}",
                     ", ".join(out_of) if out_of else "—",
                     f"{(ranks['moderate'][c][v] <= 5).mean():.0%}", f"{(ranks['severe'][c][v] <= 5).mean():.0%}"))
STRESS = pd.DataFrame(rows, columns=["Measure", "Language", "Headline rank", "Stays in top 5 in",
                                     "Drops out of the top 5 when only these ties are used",
                                     "Perturbed networks: moderate", "Perturbed networks: severe"])
STRESS.set_index(["Measure", "Language"])
'''

CODE["versions"] = r'''
import sys, matplotlib, seaborn, scipy
print(f"Python {sys.version.split()[0]} · pandas {pd.__version__} · networkx {nx.__version__} · "
      f"numpy {np.__version__} · scipy {scipy.__version__} · "
      f"matplotlib {matplotlib.__version__} · seaborn {seaborn.__version__}")
'''
