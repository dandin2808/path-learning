# &lt;topic&gt;-lineage

A guided &lt;N&gt;-notebook walk from &lt;foundational concept&gt; to &lt;current frontier&gt; in &lt;topic&gt;. Each notebook is a self-contained station on the lineage; together they trace the conceptual path from "what is the basic problem" to "what is the state of the art today."

Every stage has a companion **concept-reference card** in [`theory/`](theory/00_overview.md): the notebook gives you something to run, the theory card something to recall, and the linked papers something to learn from.

## The lineage

| # | Notebook | What it teaches | Anchor paper(s) |
|---|---|---|---|
| 01 | [&lt;title&gt;](notebooks/01_&lt;slug&gt;.ipynb) | &lt;1-line summary&gt; | [&lt;paper&gt;](https://arxiv.org/abs/...) |
| 02 | … | … | … |
| … | … | … | … |

## Concept reference cards (`theory/`)

Short, paper-linked distillations — one per stage, plus a thread overview. The cards state the key equations and ideas without re-deriving them.

- [**00 — Overview**](theory/00_overview.md): the lineage thread; what each stage adds.
- [01 &lt;stage&gt;](theory/01_&lt;slug&gt;.md) · [02 &lt;stage&gt;](theory/02_&lt;slug&gt;.md) · …

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Layout

```
&lt;topic&gt;-lineage/
├── notebooks/        the lineage notebooks
├── theory/           one concept-reference card per stage + 00_overview.md
├── external/         cloned reference repos (shallow; gitignored)
├── data/             local datasets (gitignored)
└── scripts/          notebook builder + utilities
```

## External repos (cloned, not forked)

Each is a shallow clone used as a *reference* — the notebooks import from them or read alongside them.

| Path | Source | Used by |
|---|---|---|
| `external/&lt;name&gt;/` | [&lt;org/repo&gt;](https://github.com/&lt;org&gt;/&lt;repo&gt;) | NN |
| … | … | … |

## Conventions

- Math: link to papers, no inline derivations.
- External code: shallow-cloned, never forked.
- Notebooks: generated from `scripts/build_notebooks.py` — don't hand-edit; edit the builder and regenerate.

Generated with [`path-learning`](https://github.com/dandin2808/path-learning) — a Claude Code skill.
