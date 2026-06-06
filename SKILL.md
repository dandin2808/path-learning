---
name: path-learning
description: Personalized-learning project generator. The user picks the topic, depth, stack, scope, and where to start / end; the skill builds a runnable Jupyter notebook walk tailored to how they want to study it — 10–14 stages with paper-linked theory and cloned reference repos, all regenerable from one builder script. Invoke as `/path-learning <topic>`.
argument-hint: <topic to learn — the user will shape the path in Phase 1>
---

# path-learning skill

When invoked with a topic, generate a self-contained learning project at
`~/Documents/GitHub/<topic-slug>-lineage/` (override with `--at <path>` if given).

## Two-phase contract

### Phase 1 — Propose (always do this first)

Output a markdown table proposing the lineage. Do **not** create any files yet.

Columns: `# | Stage | Key idea | Anchor paper(s) | Candidate repo (cloned, not forked)`.

Guidelines:
- 10–14 stages. Order by genuine conceptual dependency — each stage builds on the previous.
- Anchor papers should be the canonical reference, with direct URLs (arxiv preferred, journal/book otherwise).
- Candidate repos should be shallow-clonable, well-maintained, and the closest thing to a reference implementation. If only a research-quality repo exists, use it; otherwise pick the best community implementation.

After the table, list open choices and ask for agreement:

- **Depth:** full (10–14 stages) or condensed (~7)
- **Scope:** any topics to add or exclude
- **Stack:** default PyTorch + topic-specific libraries; override if the user prefers JAX/Flax/etc.
- **Location:** `~/Documents/GitHub/<topic-slug>-lineage/` (default) or user-supplied path

**Wait for the user's reply before Phase 2.** Don't pre-emptively build.

### Phase 2 — Build (only after the user agrees)

Execute these steps in order. Steps 3 and 4 can run in parallel.

1. **Create the directory tree** under the project root:

   ```
   notebooks/  theory/  external/  data/  scripts/
   ```

2. **Write base files at the project root:**
   - `LICENSE` — MIT (current year, git user name)
   - `.gitignore` — Python + Jupyter + venv + `external/*/` ignored
   - `requirements.txt` — base + topic-specific deps; comments explaining any pins
   - `README.md` — using the structure from `templates/project_readme.md`
   - `start.sh` — **mandatory, executable** one-shot launcher. Idempotent: creates `.venv` on first run, reuses it after; installs requirements; launches `jupyter lab`. After writing, run `chmod +x start.sh`. The README's Quickstart must show `./start.sh` as option 1 (the manual `python -m venv ...` sequence is option 2).

   Template `start.sh`:

   ```bash
   #!/usr/bin/env bash
   # start.sh — one-shot launcher for this lineage project.
   # Idempotent: creates the venv on first run, reuses it after.
   set -euo pipefail
   cd "$(dirname "$0")"

   VENV=".venv"
   if [ ! -d "$VENV" ]; then
       echo "[start] creating venv at $VENV"
       python3 -m venv "$VENV"
   fi
   # shellcheck disable=SC1091
   source "$VENV/bin/activate"

   echo "[start] syncing requirements"
   pip install --quiet --upgrade pip
   pip install --quiet -r requirements.txt

   echo "[start] launching JupyterLab — open notebooks/01_*.ipynb first"
   exec jupyter lab
   ```

3. **Pre-flight: validate repo URLs** before mass cloning. For each candidate repo, run `git ls-remote <url> HEAD` (fast, no clone). For any URL that fails (404, renamed, archived), propose a substitute *before* committing to the build — e.g., `Stability-AI/stablediffusion` → `Stability-AI/generative-models`, `CompVis/latent-diffusion` → `CompVis/stable-diffusion`. Update Phase 1's table with the substitutes, surface them to the user, then proceed.

   **Clone external repos in the background** (use `git clone --depth 1`, write output to a log file you can check after the rest of the build):

   ```bash
   cd external && for url in "${URLS[@]}"; do
       name=$(basename "$url" .git)
       git clone --quiet --depth 1 "$url" "$name"
   done
   ```

   **Tolerate single-clone failures.** If any clone fails after the pre-flight (transient network, rate limit, sudden archive), log the failure to a build log, propose a substitute, and continue with the remaining clones. Do not abort the build.

4. **Write `scripts/build_notebooks.py`** — one `nb_NN()` function per notebook, each constructs the notebook via `nbformat`. The script is the **single source of truth**. See `templates/builder_skeleton.py` for the structure.

5. **Write theory cards** in `theory/`:
   - `theory/00_overview.md` — the lineage thread, ~150 lines, including a "what gets added / changed at each stage" table.
   - `theory/<NN>_<slug>.md` for each notebook — 60–120 lines each, structured per `templates/theory_card.md`.

6. **Generate the notebooks:** `python scripts/build_notebooks.py`.

7. **Validate.** For every generated notebook: run `nbformat.validate(...)` and `ast.parse(...)` on each code cell. Report any failures.

8. **Verify the external clones completed** (read the clone log). If any failed, retry serially or log the error and continue with the rest.

9. **Report to the user:**
   - Project tree
   - Notebook count, theory-card count, cloned-repo list (with HEAD commits)
   - Suggest opening `notebooks/01_*.ipynb` first
   - Offer to create a venv and `pip install -r requirements.txt`

## Non-negotiable conventions

These have been load-bearing in practice; don't compromise on them without explicit user request:

- **Math: link, don't derive.** Each notebook's header has a "Read" block with canonical paper URLs. The notebook explains the *idea* and states the key equations; full derivations live in the linked papers. Theory cards follow the same rule.
- **Cloned, not forked.** Always `git clone --depth 1`. Never instruct the user to fork.
- **Builder is source of truth.** Notebooks are generated artifacts. Don't hand-edit them; edit the builder and regenerate.
- **Each notebook is independently runnable.** Repeat imports; no `from notebooks.03_x import foo`. Each notebook should fully execute from a fresh kernel.
- **Variable names: explicit over terse.** `train_idx`, not `tr`. `q_hat`, not `q`. `cal_scores`, not `cs`.
- **Plain ASCII math** where LaTeX rendering is uncertain (e.g., the body of a markdown cell that might be read in a terminal). In notebook markdown, LaTeX via `$...$` is fine because Jupyter renders it.
- **Don't pre-emptively pin packages.** Use a clean `requirements.txt`. Add pins via comments only when a known incompatibility exists, e.g.:

  ```
  laplace-torch
  # laplace-torch 0.2.2.2 imports from curvlinops._base which was removed in
  # curvlinops-for-pytorch 3.x. Pin until upstream is fixed.
  curvlinops-for-pytorch<3
  ```

- **Native-compiled packages must be optional, not required.** Any package that builds C/C++ extensions on `pip install` (e.g., `signatory`, `triton`, custom CUDA wheels) frequently fails on newer Python / torch combinations. Such packages must be:
  1. Listed in a separate `requirements-extras.txt`, not the core `requirements.txt`.
  2. Gated behind a `try / except ImportError` in any notebook that uses them, with a NumPy / pure-Python fallback path or a clear "install this and re-run" message.
  3. Documented in the project README under a clear "optional" heading.

  The reason: a failed native build aborts the entire `pip install -r requirements.txt` and blocks the whole project setup. The user can no longer even open the unrelated 90% of notebooks. Always gate.

## Notebook anatomy

Each notebook has 5–10 cells in this order:

1. **Title + Read block** (markdown): topic, "why this stage in the lineage," 4–6 references with direct URLs. **Include book chapters / textbook sections for math-heavy stages**, not just arxiv papers — for foundational topics (SDEs, optimisation, information theory, etc.) a textbook chapter is often more useful than the original journal paper. If a stage needs a **GPU to run usefully**, add a one-line `**Runtime.** GPU recommended; CPU works but is slow on cells X, Y.` note in the header so the reader knows what to skip.
2. **Imports** (code).
3. **Setup / data** (code) — synthetic data preferred where possible; if a dataset is needed, use sklearn / torchvision / huggingface that downloads on first run.
4. **Core idea** (code, often 2–4 cells, with brief markdown between).
5. **Visualization** (code, if applicable — usually matplotlib).
6. **What to notice / discussion** (markdown).
7. **Exercises** (markdown, 2–3 short prompts).

Total: 5–10 cells, mostly code with concise markdown.

## Theory card anatomy

Each `theory/<NN>_<stage>.md`:

```markdown
# NN — <Stage name>

## The key idea
(1 paragraph in plain language — what this stage adds)

## Key equations (stated, not derived)
- ...
- ...

## How it connects to neighbouring stages
- previous → here
- here → next

## Caveats / failure modes
...

## References
- [Anchor paper (Authors, Year)](https://arxiv.org/abs/...)
- ...
```

## Stack defaults

- **PyTorch 2.x** as the base for any ML topic.
- Domain-specific libraries as appropriate:
  - Bayesian methods: numpyro, pymc, arviz
  - Gaussian processes: gpytorch
  - Sequence models: einops, transformers (HuggingFace)
  - Speech: torchaudio
  - Diffusion: diffusers (HF), accelerate
  - Conformal: mapie
  - State-space: mamba-ssm (only if installable; have a torch-only fallback)
- **Jupyter + nbformat** for notebook generation.

## Finding canonical papers and repos

For each stage:

1. The paper everyone in the field cites (the "anchor") — verify the arxiv ID with a one-shot web search if uncertain.
2. A reference implementation: official > best-maintained community > research-quality.
3. If the area is recent (last 18 months), include a survey/tutorial paper as a secondary reference.

Avoid stale or unmaintained repos. Prefer pip-installable canonical packages where they exist, and use the cloned repo as the *reading material* (the user inspects the source) rather than as the import target.

## On building the project deterministically

The build must be reproducible. Re-running `python scripts/build_notebooks.py` on the same source must produce identical notebooks. This means:

- No timestamps, random seeds, or environment-dependent values baked into the source cells.
- All randomness in the notebook *bodies* should use explicit seeds.
- The cell IDs and execution counts may differ between runs — that's fine, but the cell *sources* must be byte-identical.

## On the user's machine assumptions

- macOS or Linux. Python 3.10+. Git installed. Internet access for clones + dataset downloads.
- No GPU assumed by default — keep code CPU-runnable for the small notebooks. If a stage genuinely needs GPU, mark it clearly in the notebook header.
- If `gh` is available and the user wants a public github repo, offer `gh repo create` after the build. Don't push without explicit user consent.

## Variants this skill can produce

The lineage form applies to almost any deep-technical topic:

- ML/AI: diffusion, state-space models, MoE, long context, RLHF/RL, retrieval, multimodal, reasoning, speech, vision FMs, agents
- Systems: distributed training, inference optimization, CUDA / TPU stacks
- Theory: optimization, information theory, learning theory, statistical mechanics of ML
- Outside ML: any field with a paper trail (e.g., quantitative finance methods, computational physics)

The conventions adapt; the structure is constant.
