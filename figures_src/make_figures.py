#!/usr/bin/env python
"""
Regenerate all main-text manuscript figures with a single unified style
(DejaVu Sans, consistent sizes, embedded fonts, vector PDF).

Numbers are the locked values from benchmark_results/THESIS_NUMBERS.md
(genus = 120 classes; NT-v2 = RC-TTA per-read; MT = forward-only Top-1).

Usage:  conda activate gfm && python make_figures.py
Outputs -> ../figures/*.pdf
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from figstyle import apply_style, BLUE, TEAL, ORANGE, GREY, RED, GREEN, LGREY

apply_style()
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p)
    plt.close(fig)
    print("wrote", os.path.relpath(p))


# ----------------------------------------------------------------------
# Fig. data_scaling : NT-v2 6-mer genus Top-1 vs training reads (saturation)
# ----------------------------------------------------------------------
def fig_data_scaling():
    reads = np.array([0.5, 5, 50, 250])          # millions (incl. repeats)
    acc   = np.array([55.29, 63.05, 67.07, 67.29])
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    ax.plot(reads, acc, marker="o", color=BLUE, zorder=3)
    for x, y in zip(reads, acc):
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=7.5, color=BLUE)
    # saturation bracket 50M -> 250M
    ax.annotate("", xy=(250, 67.29), xytext=(50, 67.07),
                arrowprops=dict(arrowstyle="<->", color=GREY, lw=0.9))
    ax.text(112, 64.7, "+0.22 pp\n(saturates)", ha="center", va="top",
            fontsize=7.5, color=GREY)
    ax.set_xscale("log")
    ax.set_xticks(reads)
    ax.set_xticklabels(["500K", "5M", "50M", "250M"])
    ax.set_xlabel("Training reads (including repeats)")
    ax.set_ylabel("Genus Top-1 accuracy (%)")
    ax.set_title("Data scaling within NT-v2 (6-mer)")
    ax.set_ylim(52, 72)
    save(fig, "data_scaling.pdf")


# ----------------------------------------------------------------------
# Fig. backbone_ablation : decomposition at fixed 50M reads
#   shallow-random(6mer)  ->  NT-v2 pretrained(6mer)  ->  MT 13-mer(scratch)
# ----------------------------------------------------------------------
def fig_backbone_ablation():
    labels = ["Random init\n(1-layer, 6-mer)",
              "NT-v2 pre-trained\n(6-mer)",
              "MT from scratch\n(overlap 13-mer)"]
    vals   = [53.88, 67.07, 87.42]
    colors = [LGREY, BLUE, TEAL]
    fig, ax = plt.subplots(figsize=(3.7, 2.9))
    x = np.arange(3)
    bars = ax.bar(x, vals, color=colors, width=0.62, zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x()+b.get_width()/2, v+1, f"{v:.1f}", ha="center",
                va="bottom", fontsize=8)
    # delta arrows
    ax.annotate("", xy=(1, 67.07), xytext=(0, 53.88),
                arrowprops=dict(arrowstyle="->", color="#333", lw=1.0))
    ax.text(0.5, 61.5, "+13.2 pp\npre-training", ha="center", fontsize=7.5)
    ax.annotate("", xy=(2, 87.42), xytext=(1, 67.07),
                arrowprops=dict(arrowstyle="->", color="#333", lw=1.0))
    ax.text(1.5, 78.5, "+20.4 pp\ntokenization", ha="center", fontsize=7.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=7.5)
    ax.set_ylabel("Genus Top-1 accuracy (%)")
    ax.set_title("Sources of accuracy at fixed 50M reads")
    ax.set_ylim(0, 100)
    save(fig, "backbone_ablation.pdf")


# ----------------------------------------------------------------------
# Fig. kmer_baselines (NEW) : is 13-mer just lookup?  non-neural baselines
# ----------------------------------------------------------------------
def fig_kmer_baselines():
    # Same-method isolation: fix classifier, vary k (6-mer vs 13-mer);
    # fix k, vary method (parameter-free naive Bayes vs neural net).
    groups = ["6-mer\n(NT-v2 tokenization)", "13-mer\n(overlapping)"]
    nb     = [25.9, 74.9]          # multinomial k-mer naive Bayes (no NN)
    neural = [67.0, 87.5]          # NT-v2 498M (6-mer) / MetaTransformer (13-mer)
    x = np.arange(2); w = 0.36
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    b1 = ax.bar(x-w/2, nb,     w, color=ORANGE, zorder=3, label="Naive Bayes (no NN)")
    b2 = ax.bar(x+w/2, neural, w, color=[BLUE, TEAL], zorder=3)
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x()+b.get_width()/2, b.get_height()+1.4,
                    f"{b.get_height():.1f}", ha="center", va="bottom", fontsize=8)
    # neural gain shown over the white space above each NB bar (bigger on weaker k)
    ax.annotate("", xy=(x[0]-0.06, 67.0), xytext=(x[0]-0.06, 25.9),
                arrowprops=dict(arrowstyle="<->", color="#333", lw=0.9))
    ax.text(x[0]-0.11, 46, "+41 pp", fontsize=7.5, color="#333",
            ha="right", va="center")
    ax.annotate("", xy=(x[1]-0.06, 87.5), xytext=(x[1]-0.06, 74.9),
                arrowprops=dict(arrowstyle="<->", color="#333", lw=0.9))
    ax.text(x[1]-0.11, 81.2, "+13 pp", fontsize=7.5, color="#333",
            ha="right", va="center")
    # crossing line: 13-mer NB already beats 6-mer neural
    ax.axhline(74.9, color=ORANGE, lw=0.8, ls="--", zorder=1)
    ax.text(-0.42, 76.3, "13-mer naive Bayes $>$ 6-mer 498M NT-v2",
            color=ORANGE, fontsize=7, ha="left", va="bottom")
    # legend: NB (orange) + neural (blue/teal)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ORANGE, label="Naive Bayes (no NN)"),
                       Patch(color=BLUE, label="NT-v2 6-mer (498M)"),
                       Patch(color=TEAL, label="MetaTransformer 13-mer")],
              fontsize=6.8, loc="upper left", borderpad=0.3, labelspacing=0.3)
    ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=8)
    ax.set_ylabel("Genus Top-1 accuracy (%)")
    ax.set_title("Tokenization dominates the model")
    ax.set_ylim(0, 100)
    save(fig, "kmer_baselines.pdf")


# ----------------------------------------------------------------------
# Fig. rc_tta_benefit : reverse-complement TTA gain (pp) per setting
# ----------------------------------------------------------------------
def fig_rc_tta():
    exps = ["v3 (500K)", "v4 (500K)", "v5b (500K, LA)", "v7 (500K, RC-cons.)",
            "v8 (5M)", "v9 (50M, NT-v2)", "DNABERT (5M)", "DNABERT-2 (5M)",
            "v11 (50M, shallow)"]
    fwd    = np.array([53.92, 53.75, 52.29, 54.10, 62.02, 66.29, 61.20, 57.35, 53.80])
    rc_tta = np.array([55.36, 55.29, 53.58, 55.18, 63.05, 67.07, 61.78, 58.88, 53.88])
    gain = rc_tta - fwd
    order = np.argsort(gain)
    exps = [exps[i] for i in order]; gain = gain[order]
    fig, ax = plt.subplots(figsize=(3.9, 3.0))
    y = np.arange(len(exps))
    ax.barh(y, gain, color=BLUE, height=0.66, zorder=3)
    for yi, g in zip(y, gain):
        ax.text(g+0.02, yi, f"+{g:.2f}", va="center", fontsize=7, color=BLUE)
    ax.set_yticks(y); ax.set_yticklabels(exps, fontsize=7)
    ax.set_xlabel("RC-TTA gain (percentage points)")
    ax.set_title("Reverse-complement TTA: consistent gain")
    ax.set_xlim(0, 1.8)
    ax.grid(axis="y", visible=False)
    save(fig, "rc_tta_benefit.pdf")


# ----------------------------------------------------------------------
# Fig. cross_setting_comparison : sample-level abundance fidelity by setting
#   (Pearson r + Bray-Curtis), natural pool clean_common (9x10K)
# ----------------------------------------------------------------------
def fig_cross_setting():
    # (label, read_acc, pearson_r, bray_curtis, color)
    rows = [
        ("MT 13-mer 250M",        0.987, 1.0000, 0.0045, TEAL),
        ("MT 13-mer 50M",         0.875, 0.9991, 0.0318, TEAL),
        ("NT-v2 50M",             0.671, 0.9930, 0.0979, BLUE),
        ("NT-v2 250M warm",       0.673, 0.9929, 0.0980, BLUE),
        ("NT-v2 250M scratch",    0.648, 0.9930, 0.1133, BLUE),
        ("NT-v2 17.6M species-bal",0.604,0.9927, 0.1392, GREEN),
        ("NT-v2 17.6M genus-bal", 0.372, 0.8615, 0.4196, RED),
    ]
    rows = sorted(rows, key=lambda r: r[2])       # by Pearson r
    labels = [r[0] for r in rows]; acc=[r[1] for r in rows]
    rr = [r[2] for r in rows]; bc = [r[3] for r in rows]; cols=[r[4] for r in rows]
    y = np.arange(len(rows))
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    a.barh(y, rr, color=cols, zorder=3)
    for yi, r, ac in zip(y, rr, acc):
        a.text(min(r+0.004, 1.015), yi, f"{r:.3f} ({ac*100:.0f}%)",
               va="center", fontsize=6.8)
    a.set_yticks(y); a.set_yticklabels(labels, fontsize=7.5)
    a.set_xlim(0.83, 1.09); a.set_xticks([0.85, 0.90, 0.95, 1.00])
    a.set_xlabel("Pearson $r$ (higher better)")
    a.set_title("Abundance accuracy")
    a.axvline(1.0, color=GREY, ls=":", lw=0.8)
    a.grid(axis="y", visible=False)
    b.barh(y, bc, color=cols, zorder=3)
    for yi, v in zip(y, bc):
        b.text(v+0.008, yi, f"{v:.3f}", va="center", fontsize=6.8)
    b.set_xlim(0, 0.52); b.set_xlabel("Bray--Curtis (lower better)")
    b.set_title("Composition error")
    b.grid(axis="y", visible=False)
    fig.suptitle("Sample-level abundance across settings "
                 "(natural pool, 9$\\times$10K reads)", fontsize=9.5, y=1.02)
    save(fig, "cross_setting_comparison.pdf")


# ----------------------------------------------------------------------
# Fig. tradeoff (replaces single-model ROC) : abundance vs detection
#   coverage-matched in-DB genus pool (85,819 reads)
# ----------------------------------------------------------------------
def fig_tradeoff():
    # (model, pearson_r, sens@95spec %, roc_auc, color)
    pts = [
        ("MT 13-mer",         0.9993, 66.5, 0.905, TEAL),
        ("NT-v2 6-mer",       0.9920, 17.5, 0.681, BLUE),
        ("Kraken2 (raw)",     0.8230, 93.5, 0.966, GREY),
        ("Kraken2 + Bracken", 0.9970, 93.5, 0.966, GREEN),
        ("MT 6-mer",          0.9830,  9.2, 0.576, ORANGE),
    ]
    fig, ax = plt.subplots(figsize=(4.7, 3.7))
    # Bracken correction arrow (raw Kraken2 -> +Bracken, along detection=93.5)
    ax.annotate("", xy=(0.997, 93.5), xytext=(0.823, 93.5),
                arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.3,
                                linestyle="--"), zorder=2)
    ax.text(0.905, 95.5, "+ Bracken", color=GREEN, fontsize=7,
            ha="center", va="bottom", style="italic")
    for name, r, sens, auc, col in pts:
        s = 90 + (auc-0.55)*520           # marker area ~ ROC AUC
        mk = "*" if name == "Kraken2 + Bracken" else "o"
        ax.scatter(r, sens, s=s*(2.1 if mk == "*" else 1), color=col,
                   marker=mk, edgecolor="white", linewidth=1.0, zorder=4)
    # (dx_pts, dy_pts, ha, va) manual label offsets to avoid collisions
    off = {"MT 13-mer":         (-14,  0, "right", "center"),
           "Kraken2 (raw)":     (  0,-15, "center", "top"),
           "Kraken2 + Bracken": (  6, 14, "left", "bottom"),
           "NT-v2 6-mer":       ( 12,  8, "left", "bottom"),
           "MT 6-mer":          ( 12, -8, "left", "top")}
    for name, r, sens, auc, col in pts:
        dx, dy, ha, va = off[name]
        ax.annotate(f"{name} (AUC {auc:.2f})", (r, sens),
                    textcoords="offset points", xytext=(dx, dy),
                    ha=ha, va=va, fontsize=7, color=col)
    ax.set_xlabel("Abundance fidelity: Pearson $r$  $\\rightarrow$")
    ax.set_ylabel("Detection: sensitivity @ 95% spec. (%)  $\\rightarrow$")
    ax.set_title("Abundance vs detection (in-database pool)")
    ax.set_xlim(0.78, 1.05); ax.set_ylim(-3, 116)
    ax.text(1.045, 112, "best at both", fontsize=7, color="#777",
            ha="right", va="top", style="italic")
    # marker-size legend (left side, away from all points)
    for auc_ref, yy in [(0.60, 45), (0.95, 33)]:
        ax.scatter(0.80, yy, s=90+(auc_ref-0.55)*520, color=LGREY,
                   edgecolor="white", zorder=2)
        ax.text(0.822, yy, f"ROC AUC {auc_ref:.2f}", fontsize=6.5,
                va="center", color="#666")
    save(fig, "tradeoff_abundance_detection.pdf")


# ----------------------------------------------------------------------
# Fig. train_fit (NEW) : train vs validation accuracy (representational ceiling)
# ----------------------------------------------------------------------
def fig_train_fit():
    models = ["NT-v2 6-mer\n(250M scratch)",
              "NT-v2 6-mer\n(250M warm)",
              "MT 13-mer\n(250M)"]
    train = [63.2, 65.8, 98.9]
    val   = [64.1, 66.6, 97.5]
    x = np.arange(len(models)); w = 0.36
    fig, ax = plt.subplots(figsize=(3.9, 2.9))
    b1 = ax.bar(x-w/2, train, w, label="Train", color=BLUE, zorder=3)
    b2 = ax.bar(x+w/2, val,   w, label="Validation", color=TEAL, zorder=3)
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x()+b.get_width()/2, b.get_height()+1,
                    f"{b.get_height():.1f}", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x); ax.set_xticklabels(models, fontsize=7.5)
    ax.set_ylabel("Genus accuracy (%)")
    ax.set_title("6-mer cannot fit training; 13-mer can")
    ax.set_ylim(0, 108)
    ax.legend(loc="upper left", ncol=2)
    save(fig, "train_fit.pdf")


if __name__ == "__main__":
    fig_data_scaling()
    fig_backbone_ablation()
    fig_kmer_baselines()
    fig_train_fit()
    fig_rc_tta()
    fig_cross_setting()
    fig_tradeoff()
    print("done")
