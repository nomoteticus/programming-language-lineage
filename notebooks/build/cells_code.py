# Code cells for the network-analysis notebook, keyed by name. The builder
# interleaves them with the markdown cells.
CODE = {}

CODE["setup"] = r'''
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib import patheffects
import seaborn as sns
from scipy.stats import rankdata
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

# The notebook lives in notebooks/; the data in data/.
DATA = next(p for p in [Path("../data"), Path("data")] if (p / "nodes.csv").exists())
FIGURES = DATA.parent / "notebooks" / "figures"
SAVE_FIGURES = True

SEED = 2026          # every random step below is seeded, so results are reproducible
N_DRAWS = 1000       # Monte Carlo draws for the uncertainty intervals
N_NULL = 1000        # randomized networks for the age baseline

nodes = pd.read_csv(DATA / "nodes.csv")
edges = pd.read_csv(DATA / "edges.csv")
name = nodes.set_index("id")["name"]
year = nodes.set_index("id")["year"]
family = nodes.set_index("id")["family"]
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

def family_legend(ax_or_fig, families=FAMILIES, **kw):
    handles = [Line2D([], [], marker="o", ls="", markersize=7, markerfacecolor=FAMILY_COLOR[f],
                      markeredgecolor="white", label=f) for f in families]
    return ax_or_fig.legend(handles=handles, **kw)
'''

CODE["graph"] = r'''
def build_graph(e, weighted=False):
    """Directed graph: a tie runs from the earlier language to the one that borrowed from it."""
    G = nx.DiGraph()
    G.add_nodes_from(nodes.id)
    for r in e.itertuples():
        w = 1.0 if r.strength == "strong" else 0.5
        G.add_edge(r.from_id, r.to_id,
                   weight=w if weighted else 1.0,          # for degree and status
                   distance=1 / w if weighted else 1.0)    # for shortest paths
    return G

G = build_graph(edges)
U = G.to_undirected()

two_paths = closed = 0
for b in G:
    for a in G.predecessors(b):
        for c in G.successors(b):
            if a != c:
                two_paths += 1
                closed += G.has_edge(a, c)

cross = edges.from_id.map(family) != edges.to_id.map(family)
summary = pd.Series({
    "Languages (nodes)": G.number_of_nodes(),
    "Influence ties": G.number_of_edges(),
    "Density": round(nx.density(G), 3),
    "Mean ties per language (in + out)": round(2 * G.number_of_edges() / G.number_of_nodes(), 2),
    "Languages with no tie (isolates)": ", ".join(name[v] for v in nx.isolates(G)),
    "Size of the largest connected component": max(len(c) for c in nx.weakly_connected_components(G)),
    "Mutual (two-way) pairs": sum(1 for u, v in G.edges if G.has_edge(v, u) and u < v),
    "Two-step chains A → B → C": two_paths,
    "… of which A also tied directly to C": f"{closed} ({closed / two_paths:.0%})",
    "Ties that cross family lines": f"{cross.sum()} ({cross.mean():.0%})",
}, name="value")
summary.to_frame()
'''

CODE["measures"] = r'''
ROLES = ["liaison", "gatekeeper", "representative", "itinerant", "coordinator"]

def brokerage_roles(G, groups=family):
    """Gould and Fernandez (1989) roles. For every chain A -> B -> C with no direct
    tie A -> C, B is the broker; its role depends on the families of A, B and C."""
    counts = {v: dict.fromkeys(ROLES, 0) for v in G}
    for b in G:
        for a in G.predecessors(b):
            for c in G.successors(b):
                if a == c or G.has_edge(a, c):
                    continue
                ga, gb, gc = groups[a], groups[b], groups[c]
                if ga == gb == gc:
                    role = "coordinator"      # all three in one family
                elif ga == gc:
                    role = "itinerant"        # an outsider passing ideas within another family
                elif ga == gb:
                    role = "representative"   # exports its own family's ideas
                elif gb == gc:
                    role = "gatekeeper"       # imports outside ideas into its family
                else:
                    role = "liaison"          # links two families it does not belong to
                counts[b][role] += 1
    return pd.DataFrame.from_dict(counts, orient="index")[ROLES]

def measures(G, weighted=False):
    w = "weight" if weighted else None
    m = pd.DataFrame(index=pd.Index(list(G.nodes), name="id"))
    m["outdeg"] = pd.Series(dict(G.out_degree(weight=w)))
    m["domain"] = pd.Series({v: len(nx.descendants(G, v)) for v in G})
    m["status"] = pd.Series(nx.pagerank(G.reverse(copy=True), alpha=0.85, weight=w))
    m["indeg"] = pd.Series(dict(G.in_degree(weight=w)))
    m["ancestry"] = pd.Series({v: len(nx.ancestors(G, v)) for v in G})
    m["betweenness"] = pd.Series(nx.betweenness_centrality(
        G, normalized=False, weight="distance" if weighted else None))
    roles = brokerage_roles(G)
    m["brokerage"] = roles.drop(columns="coordinator").sum(axis=1)
    return m

LABEL = {
    "outdeg": "Direct influence (outdegree)", "domain": "Influence domain",
    "status": "Status (PageRank)", "indeg": "Direct borrowing (indegree)",
    "ancestry": "Ancestry", "betweenness": "Betweenness",
    "brokerage": "Cross-family brokerage",
}
M = measures(G)
roles = brokerage_roles(G)

def rank_desc(s):
    return s.rank(ascending=False, method="min").astype(int)
'''

CODE["montecarlo"] = r'''
# Probability that each tie is kept in a draw, set by the evidence record.
def keep_probability(r):
    if r.strength == "strong":
        return 0.9
    return 0.4 if r.verdict == "partly" else 0.6

edges["p_keep"] = edges.apply(keep_probability, axis=1)
HEALTH_SCORE = {"dead": 0, "fading": 1, "alive": 2, "thriving": 3}
health = nodes.set_index("id").health.map(HEALTH_SCORE)

def spearman(x, y):
    return np.corrcoef(rankdata(x), rankdata(y))[0, 1]

def partial_spearman(x, y, z):
    """Rank correlation of x and y after removing the linear effect of z's ranks from both."""
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    res = lambda r: r - np.polyval(np.polyfit(rz, r, 1), rz)
    return np.corrcoef(res(rx), res(ry))[0, 1]

rng = np.random.default_rng(SEED)
fa = ((edges.from_id == "fortran") & (edges.to_id == "algol")).to_numpy()
ids = list(nodes.id)
fam_labels = [family[v] for v in ids]
draws, corr_rows, nmi = [], [], []
for k in range(N_DRAWS):
    keep = rng.random(len(edges)) < edges.p_keep.to_numpy()
    Gk = build_graph(edges[keep])
    mk = measures(Gk)
    mk["draw"], mk["fortran_algol_kept"] = k, bool(keep[fa][0])
    draws.append(mk)
    for col in LABEL:
        corr_rows.append((k, col, spearman(mk.loc[ids, col], health[ids]),
                          partial_spearman(mk.loc[ids, col], health[ids], year[ids])))
    comms = nx.community.louvain_communities(Gk.to_undirected(), seed=k)
    lab = {v: i for i, c in enumerate(comms) for v in c}
    nmi.append(normalized_mutual_info_score(fam_labels, [lab[v] for v in ids]))

MC = pd.concat(draws).reset_index()
for col in LABEL:
    MC[col + "_rank"] = MC.groupby("draw")[col].rank(ascending=False, method="min")
MC_CORR = pd.DataFrame(corr_rows, columns=["draw", "measure", "rho", "partial_rho"])
print(f"{N_DRAWS} draws; on average {edges.p_keep.sum():.0f} of {len(edges)} ties kept per draw")
'''

CODE["ranktable_fn"] = r'''
def rank_table(col, k=10, by=None):
    """Top k languages on one measure, with the Monte Carlo median rank and 90% rank interval."""
    q = MC.groupby("id")[col + "_rank"].quantile([0.05, 0.5, 0.95]).unstack()
    t = pd.DataFrame({
        "Language": name, "Year": year, "Family": family,
        LABEL[col]: M[col].round(3) if col == "status" else M[col].round(1),
        "Rank": rank_desc(M[col]),
        "Median rank (MC)": q[0.5].astype(int),
        "90% rank interval": q[0.05].astype(int).astype(str) + "–" + q[0.95].astype(int).astype(str),
    })
    return t.sort_values(["Rank", "Median rank (MC)"]).head(k).reset_index(drop=True).rename(lambda i: i + 1)

def plot_rank_intervals(cols, k=12, title=None, stem=None):
    fig, axes = plt.subplots(1, len(cols), figsize=(4.3 * len(cols), 0.36 * k + 1.6), sharex=False)
    axes = np.atleast_1d(axes)
    shown = set()
    for ax, col in zip(axes, cols):
        q = MC.groupby("id")[col + "_rank"].quantile([0.05, 0.5, 0.95]).unstack()
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
                          label="90% interval across 1,000 draws"))
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

CODE["timeline"] = r'''
# Main path (Hummon and Doreian 1989), computed on the 131 original-design ties,
# which form an acyclic graph. Search path count (SPC) = number of
# source-to-sink paths that run through a tie (Batagelj 2003).
def search_path_counts(D):
    order = list(nx.topological_sort(D))
    n_minus, n_plus = {}, {}
    for v in order:
        preds = list(D.predecessors(v))
        n_minus[v] = sum(n_minus[p] for p in preds) if preds else 1
    for v in reversed(order):
        succ = list(D.successors(v))
        n_plus[v] = sum(n_plus[s] for s in succ) if succ else 1
    total = sum(n_plus[v] for v in D if D.in_degree(v) == 0)
    return {(u, v): n_minus[u] * n_plus[v] for u, v in D.edges}, total

def global_main_path(D):
    D = D.copy()
    D.remove_nodes_from(list(nx.isolates(D)))
    spc, total = search_path_counts(D)
    nx.set_edge_attributes(D, spc, "spc")
    return nx.dag_longest_path(D, weight="spc"), spc, total

original = edges[edges.since.isna()]
DAG = build_graph(original)
assert nx.is_directed_acyclic_graph(DAG)
main_path, SPC, N_PATHS = global_main_path(DAG)
print("Main path:", " → ".join(name[v] for v in main_path))

spc_table = (pd.DataFrame([(name[u], name[v], s, s / N_PATHS) for (u, v), s in SPC.items()],
                          columns=["From", "To", "Search path count", "Share of all paths"])
             .sort_values("Search path count", ascending=False).head(8).reset_index(drop=True))
spc_table["Share of all paths"] = spc_table["Share of all paths"].map("{:.0%}".format)
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
size = 14 + 6.5 * M["domain"]
on_path = set(zip(main_path, main_path[1:]))

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
                                connectionstyle="arc3,rad=0.12",
                                shrinkA=np.sqrt(size[u]) / 2, shrinkB=np.sqrt(size[v]) / 2 + 1))
xy = np.array([pos[v] for v in nodes.id])
ax.scatter(xy[:, 0], xy[:, 1], s=size[nodes.id], c=[FAMILY_COLOR[f] for f in nodes.family],
           edgecolor="white", linewidth=1.3, zorder=4)
for v in nodes.id:
    x, y_ = pos[v]
    ax.text(x + 0.45 + np.sqrt(size[v]) * 0.035, y_, name[v], va="center", fontsize=7.6,
            color=INK, zorder=5, fontweight="semibold" if v in main_path else "normal",
            path_effects=[patheffects.withStroke(linewidth=2.6, foreground="white")])
ax.set_yticks([t[0] for t in ticks], [t[1] for t in ticks])
ax.set_xlim(1954, 2024)
ax.set_xticks(range(1960, 2021, 10))
ax.xaxis.grid(True); ax.set_axisbelow(True)
ax.spines[["left", "bottom"]].set_visible(False)
ax.set_title("Figure 1. The influence network on a timeline", fontsize=14, pad=14)
handles = [Line2D([], [], color=EDGE, lw=0.9, alpha=0.75, label="strong tie"),
           Line2D([], [], color=EDGE, lw=0.6, alpha=0.4, label="weak tie"),
           Line2D([], [], color=INK, lw=2.2, label="main path"),
           Line2D([], [], marker="o", ls="", ms=4, mfc=MUTED, mec="white", label="small influence domain"),
           Line2D([], [], marker="o", ls="", ms=13, mfc=MUTED, mec="white", label="large influence domain")]
ax.legend(handles=handles, loc="upper center", fontsize=8.5, ncol=5, bbox_to_anchor=(0.5, -0.04))
ax.text(0.0, -0.085, "Node size: influence domain (number of later languages that descend from it). "
        "Main path: the chain that carries the most source-to-sink paths, on original-design ties.",
        transform=ax.transAxes, fontsize=8.5, color=MUTED)
save(fig, "network-timeline")
plt.show()
'''

CODE["influence_table"] = r'''
rank_table("domain")
'''
CODE["status_table"] = r'''
rank_table("status")
'''
CODE["outdeg_table"] = r'''
rank_table("outdeg")
'''
CODE["influence_plot"] = r'''
plot_rank_intervals(["outdeg", "domain", "status"],
                    title="Figure 2. The most influential languages, with 90% rank intervals",
                    stem="network-influence-ranks")
'''

CODE["borrow_tables"] = r'''
rank_table("indeg")
'''
CODE["ancestry_table"] = r'''
rank_table("ancestry")
'''
CODE["borrow_plot"] = r'''
plot_rank_intervals(["indeg", "ancestry"], k=12,
                    title="Figure 3. The biggest borrowers, with 90% rank intervals",
                    stem="network-borrower-ranks")
'''

CODE["broker_tables"] = r'''
rank_table("betweenness")
'''
CODE["roles_table"] = r'''
R = roles.copy()
R.insert(0, "Language", name)
R.insert(1, "Family", family)
R["Cross-family total"] = M["brokerage"]
R["Rank"] = rank_desc(M["brokerage"])
q = MC.groupby("id")["brokerage_rank"].quantile([0.05, 0.5, 0.95]).unstack()
R["90% rank interval"] = q[0.05].astype(int).astype(str) + "–" + q[0.95].astype(int).astype(str)
R.columns = [c.capitalize() if c in ROLES else c for c in R.columns]
R.sort_values(["Cross-family total", "Liaison"], ascending=False).head(12).reset_index(drop=True).rename(lambda i: i + 1)
'''
CODE["roles_plot"] = r'''
ROLE_COLOR = {"liaison": BLUE, "gatekeeper": ORANGE, "representative": "#1baf7a",
              "itinerant": "#eda100", "coordinator": NEUTRAL}
ROLE_TEXT = {"liaison": "liaison (between two other families)",
             "gatekeeper": "gatekeeper (brings ideas into its family)",
             "representative": "representative (carries its family's ideas out)",
             "itinerant": "itinerant (outsider inside another family)",
             "coordinator": "coordinator (within one family)"}
top = (roles.assign(total=roles.sum(axis=1), cross=M["brokerage"])
       .sort_values(["cross", "total"], ascending=False).head(12))
fig, ax = plt.subplots(figsize=(10, 5.6))
y = np.arange(len(top))[::-1]
left = np.zeros(len(top))
for role in ROLES:
    ax.barh(y, top[role], left=left, height=0.62, color=ROLE_COLOR[role],
            edgecolor="white", linewidth=1.5, label=ROLE_TEXT[role])
    left += top[role].to_numpy()
for yi, tot in zip(y, left):
    ax.text(tot + 0.4, yi, f"{tot:.0f}", va="center", fontsize=9, color=MUTED)
ax.set_yticks(y, [name[v] for v in top.index])
ax.spines["left"].set_visible(False)
ax.xaxis.grid(True); ax.set_axisbelow(True)
ax.set_xlabel("number of brokered chains A → B → C (no direct tie A → C)")
ax.set_title("Figure 4. Brokerage roles of the top cross-family brokers")
ax.legend(loc="lower right", fontsize=8.5)
save(fig, "network-brokerage")
plt.show()
'''

CODE["weak_ties"] = r'''
wt = pd.crosstab(edges.strength, cross.rename("crosses families"), margins=True, margins_name="all ties")
wt.columns = ["within a family", "across families", "all"]
wt["share across"] = (wt["across families"] / wt["all"]).map("{:.0%}".format)
wt
'''

CODE["mixing"] = r'''
mix = pd.crosstab(edges.from_id.map(family), edges.to_id.map(family)).reindex(index=FAMILIES, columns=FAMILIES, fill_value=0)
fig, ax = plt.subplots(figsize=(8.6, 7))
sns.heatmap(mix, ax=ax, cmap=SEQ_BLUE, annot=mix.where(mix > 0).fillna(0).astype(int).astype(str).replace("0", ""),
            fmt="", cbar=False, linewidths=2, linecolor="white", square=True,
            annot_kws={"fontsize": 9})
for t in ax.texts:
    t.set_color("white" if t.get_text() and int(t.get_text()) >= 8 else INK)
ax.set_xlabel("borrowing family"); ax.set_ylabel("source family")
ax.tick_params(axis="x", rotation=40, labelcolor=INK)
plt.setp(ax.get_xticklabels(), ha="right")
ax.set_title("Figure 5. Ties between families (diagonal = within a family)")
save(fig, "network-family-mixing")
plt.show()

ei = []
for f in FAMILIES:
    internal = mix.loc[f, f]
    external = mix.loc[f].sum() + mix[f].sum() - 2 * internal
    ei.append((f, (family == f).sum(), internal, external, (external - internal) / (external + internal)))
EI = pd.DataFrame(ei, columns=["Family", "Languages", "Internal ties", "External ties", "E-I index"]).sort_values("E-I index")
EI["E-I index"] = EI["E-I index"].round(2)
EI.reset_index(drop=True).rename(lambda i: i + 1)
'''

CODE["communities"] = r'''
# Louvain is randomized: keep the best of 200 seeds by modularity.
best = max((nx.community.louvain_communities(U, seed=s) for s in range(200)),
           key=lambda c: nx.community.modularity(U, c))
comm_of = {v: i for i, c in enumerate(sorted(best, key=len, reverse=True)) for v in c}
family_parts = [set(nodes.id[nodes.family == f]) for f in FAMILIES]
fit = pd.Series({
    "Modularity of the curated families": round(nx.community.modularity(U, family_parts), 3),
    "Modularity of the Louvain communities": round(nx.community.modularity(U, best), 3),
    "Number of Louvain communities": len(best),
    "Agreement with families: NMI": round(normalized_mutual_info_score(fam_labels, [comm_of[v] for v in ids]), 2),
    "NMI, 90% interval across draws": f"{np.quantile(nmi, 0.05):.2f}–{np.quantile(nmi, 0.95):.2f}",
    "Agreement with families: adjusted Rand index": round(adjusted_rand_score(fam_labels, [comm_of[v] for v in ids]), 2),
}, name="value")
display(fit.to_frame())

rows = []
for i in sorted(set(comm_of.values())):
    members = sorted((v for v in comm_of if comm_of[v] == i), key=lambda v: year[v])
    fams = family[members].value_counts()
    rows.append((i + 1, len(members), f"{fams.index[0]} ({fams.iloc[0]} of {len(members)})",
                 ", ".join(name[v] for v in members)))
pd.DataFrame(rows, columns=["Community", "Size", "Largest family", "Members (by year)"]).set_index("Community")
'''

CODE["null"] = r'''
def time_respecting_rewire(G, n_swaps, rng):
    """Swap the targets of two ties (a->b, c->d  =>  a->d, c->b). Every language keeps
    its number of incoming and outgoing ties, and no tie may point back in time."""
    H = G.copy()
    E = list(H.edges())
    done = tries = 0
    while done < n_swaps and tries < 50 * n_swaps:
        tries += 1
        i, j = rng.integers(len(E), size=2)
        (a, b), (c, d) = E[i], E[j]
        if len({a, b, c, d}) < 4 or H.has_edge(a, d) or H.has_edge(c, b):
            continue
        if year[a] > year[d] or year[c] > year[b]:
            continue
        H.remove_edges_from([(a, b), (c, d)]); H.add_edges_from([(a, d), (c, b)])
        E[i], E[j] = (a, d), (c, b)
        done += 1
    return H

rng_null = np.random.default_rng(SEED + 1)
null = pd.DataFrame([{v: len(nx.descendants(H, v)) for v in H}
                     for H in (time_respecting_rewire(DAG, 10 * DAG.number_of_edges(), rng_null)
                               for _ in range(N_NULL))])
obs = pd.Series({v: len(nx.descendants(DAG, v)) for v in DAG})
AGE = pd.DataFrame({
    "Language": name, "Year": year, "Outdegree": pd.Series(dict(DAG.out_degree())),
    "Influence domain": obs, "Expected (null mean)": null.mean().round(1),
    "Null 90% range": null.quantile(0.05).astype(int).astype(str) + "–" + null.quantile(0.95).astype(int).astype(str),
    "Percentile": (null.lt(obs, axis=1).mean() + 0.5 * null.eq(obs, axis=1).mean()).round(3),
})
AGE["Observed / expected"] = (AGE["Influence domain"] / null.mean()).round(2)
AGE = AGE[AGE["Outdegree"] > 0]
print(f"{len(AGE)} languages with at least one outgoing tie; "
      f"rank correlation between observed and age-expected domain: {spearman(AGE['Influence domain'], AGE['Expected (null mean)']):.2f}")
above = AGE[AGE.Percentile >= 0.95]
below = AGE[AGE.Percentile <= 0.05]
print(f"Above the null's 95th percentile: {len(above)}; below its 5th percentile: {len(below)}")
print("Highest and lowest percentiles:")
pd.concat([AGE.sort_values("Percentile", ascending=False).head(5),
           AGE.sort_values("Percentile").head(5).iloc[::-1]]).reset_index(drop=True).rename(lambda i: i + 1)
'''

CODE["null_plot"] = r'''
fig, ax = plt.subplots(figsize=(8.6, 7))
cat = np.where(AGE.Percentile >= 0.95, "above", np.where(AGE.Percentile <= 0.05, "below", "within"))
colors = {"above": BLUE, "below": ORANGE, "within": NEUTRAL}
labels = {"above": "larger than its position predicts (top 5% of null)",
          "below": "smaller than its position predicts (bottom 5% of null)",
          "within": "within the null range (5th to 95th percentile)"}
for c in ["within", "above", "below"]:
    s = AGE[cat == c]
    if s.empty:
        continue
    ax.scatter(s["Expected (null mean)"], s["Influence domain"], s=58, color=colors[c],
               edgecolor="white", linewidth=1.5, label=labels[c], zorder=3)
lim = [0.8, 80]
ax.plot(lim, lim, color=MUTED, lw=1, ls=(0, (1, 2)), zorder=1)
ax.text(1.6, 1.25, "observed = expected", rotation=45, fontsize=8.5, color=MUTED, ha="left")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(lim); ax.set_ylim(lim)
for axis in (ax.xaxis, ax.yaxis):
    axis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
ax.grid(True, which="major"); ax.set_axisbelow(True)
label_ids = (list(AGE.sort_values("Percentile", ascending=False).index[:4]) + list(below.index)
             + ["fortran", "lisp", "algol", "c"])
for v in dict.fromkeys(label_ids):
    if v in AGE.index:
        x, y_ = AGE.loc[v, "Expected (null mean)"], AGE.loc[v, "Influence domain"]
        dx, dy, ha = {"b": (-7, 3, "right"), "bcpl": (0, -15, "center"), "cpl": (6, 5, "left")}.get(v, (6, 4, "left"))
        ax.annotate(name[v], (x, y_), xytext=(dx, dy), textcoords="offset points", fontsize=8.5,
                    color=INK, ha=ha)
ax.set_xlabel("expected influence domain, given year and number of ties (mean of 1,000 null networks)")
ax.set_ylabel("observed influence domain")
ax.set_title("Figure 6. Influence beyond what a language's age and ties predict")
ax.legend(loc="upper left", fontsize=8.5)
save(fig, "network-age-baseline")
plt.show()
'''

CODE["health"] = r'''
H = pd.DataFrame({"health": nodes.set_index("id").health, **{c: M[c] for c in LABEL}})
q = MC_CORR.groupby("measure")[["rho", "partial_rho"]].quantile([0.05, 0.5, 0.95]).unstack()
fmt = lambda c, k: f"{q.loc[c, (k, 0.5)]:+.2f} ({q.loc[c, (k, 0.05)]:+.2f} to {q.loc[c, (k, 0.95)]:+.2f})"
HC = pd.DataFrame({
    "All ties": [f"{spearman(M.loc[ids, c], health[ids]):+.2f}" for c in LABEL],
    "Across draws: median (90% interval)": [fmt(c, "rho") for c in LABEL],
    "All ties ": [f"{partial_spearman(M.loc[ids, c], health[ids], year[ids]):+.2f}" for c in LABEL],
    "Across draws: median (90% interval) ": [fmt(c, "partial_rho") for c in LABEL],
}, index=pd.Index([LABEL[c] for c in LABEL], name="Measure"))
HC.columns = pd.MultiIndex.from_tuples([("Rank correlation with health", "All ties"),
                                        ("Rank correlation with health", "Draws: median (90% interval)"),
                                        ("Holding year of creation constant", "All ties"),
                                        ("Holding year of creation constant", "Draws: median (90% interval)")])
print(f"Rank correlation of health with year of creation: {spearman(year[ids], health[ids]):+.2f}")
HC
'''

CODE["health_medians"] = r'''
order = ["dead", "fading", "alive", "thriving"]
med = H.groupby("health")[["outdeg", "domain", "indeg", "ancestry", "betweenness"]].median().reindex(order)
med.insert(0, "Languages", H.health.value_counts().reindex(order))
med.insert(1, "Median year", year.groupby(H.health).median().reindex(order).astype(int))
med.columns = ["Languages", "Median year"] + [LABEL[c] for c in ["outdeg", "domain", "indeg", "ancestry", "betweenness"]]
med.rename_axis("Health (AI judgment)")
'''

CODE["health_plot"] = r'''
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=False)
order = ["dead", "fading", "alive", "thriving"]
counts = H.health.value_counts()
for ax, col in zip(axes, ["domain", "indeg"]):
    sns.stripplot(data=H, x="health", y=col, order=order, ax=ax, color=BLUE, alpha=0.55,
                  size=6, jitter=0.22, edgecolor="white", linewidth=0.8)
    meds = H.groupby("health")[col].median()
    for i, h in enumerate(order):
        ax.hlines(meds[h], i - 0.3, i + 0.3, color=INK, lw=2.2, capstyle="round", zorder=5)
    ax.set_xticks(range(4), [f"{h}\n(n = {counts[h]})" for h in order])
    ax.tick_params(axis="x", labelcolor=INK)
    ax.set_xlabel(""); ax.set_ylabel(LABEL[col].lower())
    ax.yaxis.grid(True); ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
axes[0].set_title("Influence domain by health today")
axes[1].set_title("Direct borrowing by health today")
fig.text(0.01, -0.03, "Each dot is a language; the dark bar is the median. Health is an AI judgment (see caveats).",
         fontsize=8.5, color=MUTED)
fig.tight_layout()
fig.suptitle("Figure 7. Influential languages are often dead; borrowers tend to be alive",
             x=0.01, ha="left", fontsize=13.5, fontweight="semibold", y=1.0)
fig.subplots_adjust(top=0.86)
save(fig, "network-health")
plt.show()
'''

CODE["robust"] = r'''
S = measures(build_graph(edges[edges.strength == "strong"]))
W = measures(build_graph(edges, weighted=True), weighted=True)
rob = pd.DataFrame({
    "Measure": [LABEL[c] for c in LABEL],
    "Strong ties only (104)": [round(spearman(M[c], S[c]), 2) for c in LABEL],
    "Weighted (weak = 0.5)": [round(spearman(M[c], W[c]), 2) for c in LABEL],
}).set_index("Measure")
display(rob)

def top5(m, c):
    return ", ".join(name[v] for v in m[c].sort_values(ascending=False).index[:5])
pd.DataFrame({spec: [top5(m, c) for c in LABEL] for spec, m in
              [("All ties (headline)", M), ("Strong ties only", S), ("Weighted", W)]},
             index=[LABEL[c] for c in LABEL])
'''

CODE["fortran"] = r'''
G_wo = G.copy(); G_wo.remove_edge("fortran", "algol")
M_wo = measures(G_wo)
fortran = pd.DataFrame({
    "With the tie": [M.loc["fortran", "domain"], rank_desc(M["domain"])["fortran"], rank_desc(M["status"])["fortran"]],
    "Without the tie": [M_wo.loc["fortran", "domain"], rank_desc(M_wo["domain"])["fortran"], rank_desc(M_wo["status"])["fortran"]],
}, index=["Fortran's influence domain", "Fortran's rank on influence domain", "Fortran's rank on status"])
mc_wo = MC[(MC.id == "fortran") & (~MC.fortran_algol_kept)]
print(f"In the {len(mc_wo)} Monte Carlo draws without the tie, Fortran's influence-domain rank has "
      f"median {mc_wo.domain_rank.median():.0f} (90% interval {mc_wo.domain_rank.quantile(0.05):.0f}–{mc_wo.domain_rank.quantile(0.95):.0f}).")
DAG_wo = DAG.copy(); DAG_wo.remove_edge("fortran", "algol")
path_wo, _, _ = global_main_path(DAG_wo)
print("Main path without the tie:", " → ".join(name[v] for v in path_wo))
print(f"Share of all source-to-sink paths that run through Fortran → ALGOL 60: {SPC[('fortran', 'algol')] / N_PATHS:.0%}")
fortran
'''

CODE["versions"] = r'''
import sys, matplotlib, seaborn, scipy, sklearn
print(f"Python {sys.version.split()[0]} · pandas {pd.__version__} · networkx {nx.__version__} · "
      f"numpy {np.__version__} · scipy {scipy.__version__} · scikit-learn {sklearn.__version__} · "
      f"matplotlib {matplotlib.__version__} · seaborn {seaborn.__version__}")
'''
