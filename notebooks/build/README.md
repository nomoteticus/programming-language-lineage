# Notebook builder

The network analysis notebook is generated from two files, so that prose and code stay in one place:

- `cells_code.py`: the code cells (`CODE`, keyed by name)
- `cells_md.py`: the text cells (`MD`, keyed by name)
- `build_nb.py`: puts the cells together in the order given by `ORDER`

Edit the cell files, not the `.ipynb`. From the repository root:

```bash
python -X utf8 notebooks/build/build_nb.py notebooks/network-analysis.ipynb
python -m nbconvert --to notebook --execute --inplace notebooks/network-analysis.ipynb
python -m nbconvert --to html --no-input notebooks/network-analysis.ipynb
```

The figures are written to `notebooks/figures/`. `dump.py` prints a notebook's outputs as text, for checking numbers:
`python -X utf8 notebooks/build/dump.py notebooks/network-analysis.ipynb`.

The Python packages are pinned in `requirements.txt` at the repository root.
