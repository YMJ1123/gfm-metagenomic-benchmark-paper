# AGENTS.md

This repository is a **standalone LaTeX manuscript** (plus a small Python figure
pipeline) for a submission to *Briefings in Bioinformatics* (BIB). There is no
web app, server, or database — the "application" is the compiled PDF.

For file layout, submission-format rules, and standard build commands, see
`README.md` (authoritative). Don't duplicate that here.

## Cursor Cloud specific instructions

### What "running the app" means
- Build the three documents from source with `latexmk`:
  - `latexmk -pdf main.tex` → `main.pdf` (the manuscript)
  - `latexmk -pdf supplementary.tex` → `supplementary.pdf`
  - `latexmk -pdf cover_letter.tex` → `cover_letter.pdf`
- `latexmkrc` pins pdfLaTeX + bibtex, so `latexmk -pdf` handles the
  `pdflatex → bibtex → pdflatex×2` order automatically.
- There is **no test suite and no configured linter**; a clean `latexmk` build
  with no undefined citations/references is the success check. `chktex` (bundled
  with TeX Live) is available as an *advisory* LaTeX linter only.

### TeX distribution caveat (important)
- The cloud VM snapshot has **TeX Live 2023** (installed via `apt texlive-full`),
  which compiles the bundled OUP class and this manuscript cleanly.
- **Do NOT upgrade to TeX Live 2026 / "latest".** The OUP
  `oup-authoring-template` class depends on `arydshln`, which is broken by the
  TeX Live 2026 LaTeX kernel (even OUP's own sample fails there). See `README.md`
  and `.github/workflows/build.yml` (CI is pinned to `texlive_version: 2024`).

### Build gotchas (already handled in the source — don't "fix")
- `main.tex` uses `\bibliographystyle{unsrtnat}`, **not** the bundled
  `oup-plain.bst`; the latter emits bare `\bibitem{key}` and breaks numbered
  citations. This is intentional (commented in `main.tex`).
- A clean `main.log` still shows a few `LaTeX Font Warning: Font shape
  'OT1/cmss/...' undefined` lines — these are harmless font substitutions, not
  build errors.

### Figures (Python side)
- Committed vector figures live in `figures/*.pdf` and are consumed by the LaTeX
  build. Regenerate them only when the data/plots change:
  `cd figures_src && python3 make_figures.py` (overwrites `../figures/*.pdf`).
- Requires `matplotlib` + `numpy`. On Ubuntu 24.04 these must be installed with
  `pip install --break-system-packages` (PEP 668 externally-managed env); the
  startup update script already does this.
- Newer matplotlib re-embeds fonts, so regenerated PDFs differ byte-for-byte
  from the committed ones even with identical data. Don't commit regenerated
  figures unless the plotted numbers actually changed.

### Git note
- Built PDFs (`main.pdf`, `supplementary.pdf`, `cover_letter.pdf`) and LaTeX
  aux files are `.gitignore`d — do not commit them.
