"""Shared matplotlib style for all manuscript figures (unified fonts/sizes).
Import and call apply_style() at the top of every figure script."""
import matplotlib as mpl
import matplotlib.pyplot as plt

# Palette (paper accent = OUP bibblue 0,63,114)
BLUE   = "#003f72"   # primary / NT-v2
TEAL   = "#2a9d8f"   # MT 13-mer
ORANGE = "#e07a2f"   # MT 6-mer / secondary
GREY   = "#8a8f98"   # Kraken2 / neutral
LGREY  = "#c9ccd1"
RED    = "#c1432e"   # negative / genus-balanced
GREEN  = "#4c956c"
PALETTE = [BLUE, TEAL, ORANGE, GREY, RED, GREEN]

def apply_style():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "mathtext.fontset": "dejavusans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.titleweight": "bold",
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.titlesize": 11,
        "axes.linewidth": 0.8,
        "axes.edgecolor": "#444444",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#dddddd",
        "grid.linewidth": 0.6,
        "grid.alpha": 1.0,
        "xtick.color": "#444444",
        "ytick.color": "#444444",
        "xtick.labelcolor": "black",
        "ytick.labelcolor": "black",
        "lines.linewidth": 1.8,
        "lines.markersize": 6,
        "legend.frameon": False,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,   # embed as TrueType (no Type-3), journal-safe
        "ps.fonttype": 42,
    })

if __name__ == "__main__":
    apply_style()
    import numpy as np
    fig, ax = plt.subplots(figsize=(3.2, 2.4))
    ax.plot([1,2,3],[1,4,9], marker="o", color=BLUE, label="test $r=0.99$")
    ax.set_xlabel("x label"); ax.set_ylabel("y label"); ax.set_title("Font test")
    ax.legend()
    fig.savefig("/tmp/claude-27474/-home-ymj1123ntu/bc482539-0db5-47b0-8470-5c579748a179/scratchpad/fonttest.pdf")
    print("wrote fonttest.pdf")
