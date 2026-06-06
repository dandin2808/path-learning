# path-learning

**Personalized learning, in code.** Learn the way you want — at the level of detail you need, along the path you choose.

You hand the skill a topic. It proposes a path — typically 10–14 stages from foundations to frontier — and asks you what to adjust: **depth, scope, stack, where to start, where to end, what to skip**. Once you're happy with the path, it builds a runnable notebook project tailored to *your* version of it.

The skill is opinionated about format (runnable code, paper-linked math, cloned reference repos) and humble about content — every choice that shapes the path is yours.

## Why this exists

You can learn from blog posts. You can learn from textbooks. You can learn from running code. The first two carry an *author's* path through the material; the third makes you assemble the path yourself, usually badly.

This skill writes the *third* for you, on demand and customised — a path **you** choose, expressed in working code, with the math one click away.

## What you get

```
/path-learning <topic>
```

Phase 1 — the skill proposes a path. You edit:

- **Depth.** Full (10–14 stages) or condensed (~7)?
- **Scope.** Add topics. Drop topics. Combine related ones.
- **Where to start and end.** Anchor it in foundations you don't have yet, or jump to the frontier directly.
- **Stack.** PyTorch by default; JAX / TF / pure-NumPy on request.
- **What "frontier" means for you.** Newest papers, a specific production system, a particular sub-area.

Phase 2 — once you approve, the skill generates:

- one Jupyter notebook per stage, **runnable**, with paper-linked math (no derivations buried in code cells),
- a `theory/` folder with concept-reference cards per stage,
- shallow-cloned reference repos in `external/`,
- a single `scripts/build_notebooks.py` that regenerates the entire project,
- `README.md`, `requirements.txt`, `.gitignore`.

Each notebook is a starting point — not a chapter to passively read, but a working piece of code you can fork, break, and rebuild. The accompanying theory card states the equations and points at the papers; the cloned source repo is the canonical implementation to compare your work against.

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
- `/path-learning conformal prediction`

The skill always opens with the proposed path and the open choices before generating any files. **You drive the path; the skill builds it.**

## Conventions (the opinions about *how*)

See [`SKILL.md`](SKILL.md) for the full list. The load-bearing ones:

- **Math in notebooks: link to canonical papers, don't derive inline.** Detail lives in the papers; the notebook explains the *idea*.
- **External code: shallow-cloned, never forked.** You're reading the reference implementation alongside, not maintaining it.
- **Each notebook is independently runnable.** No cross-notebook imports.
- **Variable names: explicit over terse.** `train_idx`, not `tr`.
- **Pin packages only when a known incompatibility exists**, with a comment explaining why.

These are about *form*. *Content* is always yours to shape.

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
