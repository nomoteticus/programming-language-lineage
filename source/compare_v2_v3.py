"""Compares version 2 with version 3 and writes:

  ../data/edges-v2-to-v3.csv       every link of either version, v2 and v3 values side by side, with the reason
  ../data/languages-v2-to-v3.csv   languages added in version 3

Version 2 comes from the frozen edges_v2.py and v2ref/edges.csv (the published version 2 data);
version 3 from nodes.py, edges.py and sources.json. Reasons for links that were dropped or rerouted
come from research/v3_reconcile.csv.
"""
import csv, json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")
STRENGTH = {"s": "strong", "d": "weak"}


def load(name):
    ns = {}
    exec(open(os.path.join(HERE, name), encoding="utf-8").read(), ns)
    return ns


def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


N = load("nodes.py")
E2, E3 = load("edges_v2.py"), load("edges.py")
SRC = json.load(open(os.path.join(HERE, "sources.json"), encoding="utf-8"))
V2ROW = {(r["from_id"], r["to_id"]): r for r in csv.DictReader(open(os.path.join(HERE, "v2ref", "edges.csv"), encoding="utf-8"))}
V2NODES = {r["id"] for r in csv.DictReader(open(os.path.join(HERE, "v2ref", "nodes.csv"), encoding="utf-8"))}
AUDIT = {(r["frm"], r["to"]): r for r in csv.DictReader(open(os.path.join(HERE, "research", "v3_reconcile.csv"), encoding="utf-8"))}
FAMILY = dict(N["FAMILIES"])
name = {n[0]: n[1] for n in N["NODES"]}

# ---------------------------------------------------------------- languages
lang_rows = [[n[0], "added", n[1], n[2], FAMILY[n[4]]] for n in N["NODES"] if n[0] not in V2NODES]
write("languages-v2-to-v3.csv", ["id", "change", "name", "year", "family"], lang_rows)

# ---------------------------------------------------------------- links
e2 = {(a, b): (label, STRENGTH[s], kind, since or "") for a, b, label, s, kind, since in E2["EDGES"]}
e3 = {(a, b): (label, STRENGTH[s], kind, since or "") for a, b, label, s, kind, since in E3["EDGES"]}
order = {k: i for i, k in enumerate(e3)}
rows = []
for key in sorted(set(e2) | set(e3), key=lambda k: (order.get(k, len(order)), k)):
    a, b = key
    old, new = e2.get(key), e3.get(key)
    v2v = V2ROW[key]["verdict"] if key in V2ROW else ""
    v3v = SRC[f"{a}>{b}"]["verdict"] if new else ""
    if old and not new:
        change = "rerouted through a new language" if AUDIT[key]["recommend"] == "reroute" else "removed"
        reason = AUDIT[key]["recommend_why"]
    elif new and not old:
        change = "added (new language)" if (a not in V2NODES or b not in V2NODES) else "added"
        reason = SRC[f"{a}>{b}"]["audit"]
    else:
        parts = []
        if old[1] != new[1]: parts.append("strength changed")
        if old[2] != new[2]: parts.append("kind changed")
        if v2v != v3v: parts.append("verdict changed")
        if old[0] != new[0]: parts.append("label changed")
        if old[3] != new[3]: parts.append("version tag changed")
        if V2ROW[key]["quote"] != SRC[f"{a}>{b}"]["quote"]: parts.append("quote changed")
        change = "; ".join(parts) or "unchanged"
        reason = SRC[f"{a}>{b}"]["audit"]
    rows.append([a, name[a], b, name[b], change,
                 old[0] if old else "", new[0] if new else "", old[1] if old else "", new[1] if new else "",
                 old[2] if old else "", new[2] if new else "", v2v, v3v, new[3] if new else "", reason])
write("edges-v2-to-v3.csv",
      ["from_id", "from_name", "to_id", "to_name", "change", "v2_label", "v3_label", "v2_strength", "v3_strength",
       "v2_kind", "v3_kind", "v2_verdict", "v3_verdict", "v3_since", "reason"], rows)

# ---------------------------------------------------------------- summary
print(f"v2: {len(V2NODES)} languages, {len(e2)} links ({dict(Counter(v[1] for v in e2.values()))})")
print(f"v3: {len(name)} languages, {len(e3)} links ({dict(Counter(v[1] for v in e3.values()))})")
both = [k for k in e2 if k in e3]
print(f"links in both: {len(both)}; added: {sum(k not in e2 for k in e3)}; removed: {sum(r[4] == 'removed' for r in rows)}; "
      f"rerouted: {sum(r[4].startswith('rerouted') for r in rows)}")
print(f"strength changed: {sum(e2[k][1] != e3[k][1] for k in both)} "
      f"(strong to weak {sum(e2[k][1] == 'strong' and e3[k][1] == 'weak' for k in both)}, "
      f"weak to strong {sum(e2[k][1] == 'weak' and e3[k][1] == 'strong' for k in both)}); "
      f"kind changed: {sum(e2[k][2] != e3[k][2] for k in both)}; "
      f"verdict changed: {sum(V2ROW[k]['verdict'] != SRC[f'{k[0]}>{k[1]}']['verdict'] for k in both)}; "
      f"quote changed: {sum(V2ROW[k]['quote'] != SRC[f'{k[0]}>{k[1]}']['quote'] for k in both)}; "
      f"unchanged: {sum(r[4] == 'unchanged' for r in rows)}")
