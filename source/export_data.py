"""Exports the map's data as two plain CSV files, for analysis and for readers:

  ../data/nodes.csv   one row per language
  ../data/edges.csv   one row per influence link, with its evidence record

Reads nodes.py, desc.py, edges.py and sources.json (run make_nodes.py, make_desc.py and
make_sources.py first if those are stale). Changes nothing else.
"""
import csv, json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")


def load(name):
    ns = {}
    exec(open(os.path.join(HERE, name), encoding="utf-8").read(), ns)
    return ns


N = load("nodes.py")
E = load("edges.py")
DESC = load("desc.py")["DESC"]
SRC = json.load(open(os.path.join(HERE, "sources.json"), encoding="utf-8"))

NODES, STATUS, FLAGS, COUNTRY = N["NODES"], N["STATUS"], N["FLAGS"], N["COUNTRY"]
INVENTORS, ORG, SOFTWARE, LOGO_SLUG, SCOPE = N["INVENTORS"], N["ORG"], N["SOFTWARE"], N["LOGO_SLUG"], N["SCOPE"]
FAMILY = dict(N["FAMILIES"])
EDGES, SHORT, SINCE_YEAR = E["EDGES"], E["SHORT"], E["SINCE_YEAR"]

NAME = {n[0]: n[1] for n in NODES}
OUTLOOK = {"bull": "bullish", "steady": "steady", "bear": "bearish", None: ""}
STRENGTH = {"s": "strong", "d": "weak"}


def country(code):
    return COUNTRY.get(code, code)


def write(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows, {len(header)} columns")


# ---------------------------------------------------------------- nodes
node_header = [
    "id", "name", "year", "family_id", "family",
    "country_built_code", "country_built", "organization",
    "designers", "designer_countries",
    "health", "maintenance", "new_projects", "installed_base",
    "outlook_2046", "outlook_confidence", "outlook_rests_on_ai_assumption", "outlook_would_change_if",
    "status_note", "scope_kind", "scope_text",
    "logo_slug", "blurb", "description", "famous_software",
]
node_rows = []
for nid, label, year, _y, fam, blurb in NODES:
    s = STATUS[nid]
    built = FLAGS[nid][0]
    inv = [(name, c) for name, c in INVENTORS.get(nid, []) if name]
    scope_kind, scope_text = SCOPE.get(nid, ("", ""))
    has_outlook = s["ol"] is not None
    node_rows.append([
        nid, label, year, fam, FAMILY[fam],
        built, country(built), ORG.get(nid, ""),
        "; ".join(name for name, _ in inv),
        # birth country where recorded; otherwise the country where the designer or team worked on the language
        "; ".join(country(c) if c else ("International" if built == "intl" else f"{country(built)} (worked in)") for _, c in inv),
        s["st"], s["maint"], s["newproj"], s["base"],
        OUTLOOK[s["ol"]], s["conf"] or "", ("yes" if s["ai"] else "no") if has_outlook else "", s["ifchange"],
        s["note"], scope_kind, scope_text,
        LOGO_SLUG.get(nid, ""), blurb, DESC[nid],
        "; ".join(f"{sw} ({what})" for sw, what in SOFTWARE.get(nid, [])),
    ])

# ---------------------------------------------------------------- edges
edge_header = [
    "from_id", "from_name", "to_id", "to_name",
    "label", "map_label", "strength", "kind", "since", "since_year",
    "verdict", "source_type", "relationship_evidence", "feature_evidence",
    "citation", "url", "quote", "source_names_it", "note", "audit_note",
]
edge_rows = []
for a, b, label, strength, kind, since in EDGES:
    r = SRC[f"{a}>{b}"]
    edge_rows.append([
        a, NAME[a], b, NAME[b],
        label, SHORT.get((a, b), label), STRENGTH[strength], kind, since or "", SINCE_YEAR.get((a, b), ""),
        r["verdict"], r["type"], r["rel"], r["feat"],
        r["citation"], r["url"], r["quote"], r["names_it"], r["note"], r["audit"],
    ])

# ---------------------------------------------------------------- checks
assert len({r[0] for r in node_rows}) == len(node_rows), "duplicate node id"
assert len({(r[0], r[2]) for r in edge_rows}) == len(edge_rows), "duplicate link"
assert all(r[0] in NAME and r[2] in NAME for r in edge_rows), "link to unknown language"
assert set(SRC) == {f"{a}>{b}" for a, b, *_ in EDGES}, "links and evidence records differ"
assert all(r[edge_header.index("citation")] and r[edge_header.index("url")] for r in edge_rows), "link without citation or url"
assert all(r[edge_header.index("strength")] == "weak" for r in edge_rows if r[edge_header.index("kind")] not in ("design", "syntax", "type")), "a link by another route must be weak"
assert all(bool(r[edge_header.index("since")]) == bool(r[edge_header.index("since_year")]) for r in edge_rows), "later-version link without a year"

write("nodes.csv", node_header, node_rows)
write("edges.csv", edge_header, edge_rows)

col = lambda rows, header, name: Counter(r[header.index(name)] for r in rows)
print("health:     ", dict(col(node_rows, node_header, "health")))
print("outlook:    ", dict(col(node_rows, node_header, "outlook_2046")))
print("confidence: ", dict(col(node_rows, node_header, "outlook_confidence")))
print("strength:   ", dict(col(edge_rows, edge_header, "strength")))
print("verdict:    ", dict(col(edge_rows, edge_header, "verdict")))
print("source type:", dict(col(edge_rows, edge_header, "source_type")))
print("tagged with a later version:", sum(1 for r in edge_rows if r[edge_header.index("since")]))
linked = {r[0] for r in edge_rows} | {r[2] for r in edge_rows}
print("languages with no link:", sorted(set(NAME) - linked))
