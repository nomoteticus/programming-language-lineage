"""Compares the pre-review version (v1) with the published version (v2) and writes:

  ../data/edges-v1-to-v2.csv       every link of either version, v1 and v2 values side by side
  ../data/languages-v1-to-v2.csv   languages added, removed, renamed or re-dated

v1 comes from the frozen v1 generator (v1ref/build.py); v2 from nodes.py (without the two languages
added in version 3) and the frozen edges_v2.py.
v1 links had a label and a strength only; link kinds and later-version tags were introduced afterwards.
"""
import ast, csv, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "us_spelling.py"), encoding="utf-8").read())   # us(): US spelling for our own text
OUT = os.path.join(HERE, "..", "data")
STRENGTH = {"s": "strong", "d": "weak"}
V3_NEW = {"turbopascal", "quickbasic"}


def v1_data():
    tree = ast.parse(open(os.path.join(HERE, "v1ref", "build.py"), encoding="utf-8").read())
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ("NODES", "EDGES"):
            found[node.targets[0].id] = ast.literal_eval(node.value)
    return found["NODES"], found["EDGES"]


def v2_data():
    ns = {}
    for name in ("nodes.py", "edges_v2.py"):          # edges_v2.py: the version 2 links, frozen
        exec(open(os.path.join(HERE, name), encoding="utf-8").read(), ns)
    nodes = [n for n in ns["NODES"] if n[0] not in V3_NEW]   # languages added in version 3 are not part of version 2
    return nodes, ns["EDGES"], dict(ns["FAMILIES"])


def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


N1, E1 = v1_data()
N2, E2, FAMILY = v2_data()
n1 = {n[0]: n for n in N1}
n2 = {n[0]: n for n in N2}
name = {i: n[1] for i, n in n1.items()}
name.update({i: n[1] for i, n in n2.items()})          # v2 names win where both exist

# ---------------------------------------------------------------- languages
lang_rows = []
for i in sorted(set(n1) | set(n2), key=lambda i: ((n2.get(i) or n1[i])[2], i)):
    a, b = n1.get(i), n2.get(i)
    if a and not b:
        change = "removed"
    elif b and not a:
        change = "added"
    else:
        parts = []
        if a[1] != b[1]: parts.append("renamed")
        if a[2] != b[2]: parts.append("year changed")
        if a[4] != b[4]: parts.append("family changed")
        change = "; ".join(parts)
    if change:
        lang_rows.append([i, change, a[1] if a else "", b[1] if b else "", a[2] if a else "", b[2] if b else "",
                          FAMILY[(b or a)[4]]])
write("languages-v1-to-v2.csv", ["id", "change", "v1_name", "v2_name", "v1_year", "v2_year", "family"], lang_rows)

# ---------------------------------------------------------------- links
e1 = {(a, b): (us(label), STRENGTH[s]) for a, b, label, s in E1}   # v1 labels in US spelling, so only real rewording counts
e2 = {(a, b): (label, STRENGTH[s], kind, since or "") for a, b, label, s, kind, since in E2}
assert len(e1) == len(E1) and len(e2) == len(E2), "duplicate link"

order = {k: i for i, k in enumerate(e2)}
edge_rows = []
for key in sorted(set(e1) | set(e2), key=lambda k: (order.get(k, len(order)), k)):
    a, b = key
    old, new = e1.get(key), e2.get(key)
    if old and not new:
        gone = [x for x in key if x not in n2]
        change = "removed (language removed)" if gone else "removed"
    elif new and not old:
        fresh = [x for x in key if x not in n1]
        change = "added (new language)" if fresh else "added"
    else:
        parts = []
        if old[1] != new[1]: parts.append("strength changed")
        if old[0] != new[0]: parts.append("label changed")
        if new[3]: parts.append("version tag added")
        change = "; ".join(parts) or "unchanged"
    edge_rows.append([
        a, name[a], b, name[b], change,
        old[0] if old else "", new[0] if new else "",
        old[1] if old else "", new[1] if new else "",
        new[2] if new else "", new[3] if new else "",
    ])
write("edges-v1-to-v2.csv",
      ["from_id", "from_name", "to_id", "to_name", "change",
       "v1_label", "v2_label", "v1_strength", "v2_strength", "v2_kind", "v2_since"], edge_rows)

# ---------------------------------------------------------------- summary
print(f"v1: {len(n1)} languages, {len(e1)} links ({Counter(v[1] for v in e1.values())})")
print(f"v2: {len(n2)} languages, {len(e2)} links ({Counter(v[1] for v in e2.values())})")
print("languages:", dict(Counter(r[1] for r in lang_rows)))
for change, count in sorted(Counter(r[4] for r in edge_rows).items(), key=lambda kv: -kv[1]):
    print(f"  {count:4d}  {change}")
in_both = [k for k in e1 if k in e2]
print(f"links in both versions: {len(in_both)}; "
      f"strength changed: {sum(e1[k][1] != e2[k][1] for k in in_both)} "
      f"(strong to weak {sum(e1[k][1] == 'strong' and e2[k][1] == 'weak' for k in in_both)}, "
      f"weak to strong {sum(e1[k][1] == 'weak' and e2[k][1] == 'strong' for k in in_both)}); "
      f"label changed: {sum(e1[k][0] != e2[k][0] for k in in_both)}")
