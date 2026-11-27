import nbformat, sys
nb = nbformat.read(sys.argv[1], as_version=4)
for i, c in enumerate(nb.cells):
    if c.cell_type != "code": continue
    for o in c.get("outputs", []):
        if o.output_type == "stream": print(f"--[{i}] stream\n", o.text[:3000])
        elif o.output_type in ("execute_result", "display_data"):
            d = o.get("data", {})
            if "text/plain" in d and "image/png" not in d: print(f"--[{i}] result\n", d["text/plain"][:4000])
            if "image/png" in d: print(f"--[{i}] [image]")
        elif o.output_type == "error": print(f"--[{i}] ERROR", o.ename, o.evalue)
