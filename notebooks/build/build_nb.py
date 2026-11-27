import sys, nbformat
from pathlib import Path
here = Path(__file__).parent
sys.path.insert(0, str(here))
from cells_code import CODE
try:
    from cells_md import MD
except ImportError:
    MD = {}

ORDER = [
    "md:title", "md:summary", "md:howto",
    "md:setup", "code:setup", "code:style",
    "md:data", "code:graph", "md:glance",
    "md:measures", "code:measures_fn", "code:check", "md:uncertainty", "code:montecarlo", "code:ranktable_fn",
    "md:timeline", "code:mainpath_fn", "code:spc_table", "code:timeline_plot", "md:timeline_read",
    "md:rq1", "code:outdeg_table", "md:rq1b", "code:influence_table", "code:status_table", "code:influence_plot", "md:rq1_read",
    "md:rq2", "code:borrow_tables", "code:ancestry_table", "code:borrow_plot", "md:rq2_read",
    "md:rq3", "code:broker_tables", "code:broker_plot", "md:rq3_read",
    "md:rq4", "code:weak_ties", "code:weak_plot", "md:rq4_read",
    "md:rq5", "code:families", "code:families_plot", "md:rq5_read",
    "md:rq6", "code:age", "code:age_plot", "md:rq6_read",
    "md:robust", "code:specs", "code:specs_plot", "md:fortran", "code:fortran", "md:stress", "code:stress", "md:robust_read",
    "md:conclusions", "md:caveats", "md:references", "code:versions",
]

cells = []
for item in ORDER:
    kind, key = item.split(":")
    if kind == "code":
        cells.append(nbformat.v4.new_code_cell(CODE[key].strip("\n")))
    else:
        cells.append(nbformat.v4.new_markdown_cell(MD.get(key, f"### [{key}]").strip("\n")))
nb = nbformat.v4.new_notebook(cells=cells)
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
nb.metadata["language_info"] = {"name": "python"}
nb.metadata["title"] = "Who shaped whom? The influence network of programming languages"
out = Path(sys.argv[1])
out.parent.mkdir(parents=True, exist_ok=True)
nbformat.write(nb, out)
print("wrote", out, len(cells), "cells")
