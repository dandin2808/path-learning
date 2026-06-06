# path-learning

A Claude Code skill that turns any topic into a multi-notebook **lineage learning project**.

You ask:

```
/path-learning diffusion models
```

The skill proposes a 10–14 stage path from foundations to the current frontier, with paper links and candidate repos. Once you approve the plan, it generates:

- one Jupyter notebook per stage — each runnable, with paper-linked math (no derivations buried in cells),
- a `theory/` folder with concept-reference cards per stage,
- shallow-cloned reference repos in `external/`,
- a single `scripts/build_notebooks.py` that regenerates the entire project,
- `README.md`, `requirements.txt`, `.gitignore`.

The result is a self-contained learning artifact that walks the reader from "what is the basic problem" to "what is the current frontier," with each step a runnable starting point rather than a chapter to read.

## Install

Requires [Claude Code](https://claude.com/claude-code) with skills support.

```bash
git clone https://github.com/dandin2808/path-learning ~/Documents/GitHub/path-learning
mkdir -p ~/.claude/skills
ln -s ~/Documents/GitHub/path-learning ~/.claude/skills/path-learning
```

That's it. Restart Claude Code (or open a new session) and `/path-learning` becomes available.

## Use

```
/path-learning <topic>
```

Examples:

- `/path-learning diffusion models`
- `/path-learning state-space sequence models`
- `/path-learning speech foundation models`
- `/path-learning mixture of experts`

The skill is **opinionated about two things**:

1. **Propose before building.** It always returns a lineage table first; you edit / approve before any files are written.
2. **Single source of truth.** Notebooks are *generated* from one builder script, not hand-edited. To change a notebook, edit the script and regenerate.

## Conventions

See [`SKILL.md`](SKILL.md) for the full list. The load-bearing ones:

- Math in notebooks: **link to canonical papers, don't derive inline.**
- External code: **shallow-cloned, never forked.**
- Each notebook is **independently runnable** (no cross-notebook imports).
- Variable names: **explicit over terse** (`train_idx`, not `tr`).
- Pin packages **only when a known incompatibility exists**, with a comment explaining why.

## What gets generated

```
<topic>-lineage/
├── notebooks/        the lineage notebooks (e.g. 01_…, 02_…, …)
├── theory/           one concept-reference card per stage + 00_overview.md
├── external/         cloned reference repos (shallow, gitignored)
├── data/             local datasets (gitignored)
├── scripts/
│   └── build_notebooks.py   single source of truth — regenerates notebooks
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## License

MIT.
