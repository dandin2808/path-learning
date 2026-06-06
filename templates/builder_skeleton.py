#!/usr/bin/env python3
"""Build the lineage notebooks.

Each nb_NN() function constructs one notebook via nbformat. This script is the
**single source of truth** — notebooks are generated artifacts, not
hand-edited. Re-running this script should reproduce identical notebooks.

Usage:
    python scripts/build_notebooks.py
"""
from __future__ import annotations
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent
NBDIR = ROOT / "notebooks"
NBDIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def md(text: str):
    return nbf.v4.new_markdown_cell(text.strip("\n"))


def code(src: str):
    return nbf.v4.new_code_cell(src.strip("\n"))


def write_nb(name: str, cells: list):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python"}
    nbf.write(nb, NBDIR / name)
    print(f"wrote {name}  ({len(cells)} cells)")


# ---------------------------------------------------------------------------
# Per-notebook builders. Add one per stage in the lineage.
# ---------------------------------------------------------------------------

def nb_01():
    cells = [
        md(r"""
# 01 — <stage title>

**Why this is the first stage.** (1–2 sentences anchoring it in the lineage.)

**Read.**
- [Paper Title (Authors, Year)](https://arxiv.org/abs/XXXX.YYYYY)
- [Another canonical reference](https://...)
- [Reference implementation](https://github.com/...)
"""),
        code(r"""
import torch
import numpy as np
import matplotlib.pyplot as plt
torch.manual_seed(0)
"""),
        md(r"""
## Core idea

(1 paragraph — the conceptual point, not the math derivation.)
"""),
        code(r"""
# Minimal runnable example demonstrating the concept.
# Keep CPU-friendly; small N; use synthetic data where possible.
pass
"""),
        md(r"""
## What to notice

(1–2 short paragraphs on what the output shows and why it matters.)

## Exercises
1. Vary <parameter> and observe how <quantity> changes.
2. Replace <component> with <alternative> and compare.
3. (Optional, deeper) Read <paper §X> and reproduce <result>.
"""),
    ]
    write_nb("01_<slug>.ipynb", cells)


# def nb_02():
#     cells = [
#         md(r"""
# # 02 — <next stage>
# ...
# """),
#         ...
#     ]
#     write_nb("02_<slug>.ipynb", cells)


# Add nb_03, nb_04, ..., nb_NN as required.


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    builders = [nb_01]  # extend: [nb_01, nb_02, nb_03, ...]
    for fn in builders:
        fn()
    print("done.")
