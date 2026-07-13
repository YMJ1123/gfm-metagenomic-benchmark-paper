#!/usr/bin/env python3
"""Per-genus mock-community abundance bars (D6331, mean of two replicates)."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import figstyle

figstyle.apply_style()

ROOT = Path("/nas2/gfm-classifier/mock_community")
OUT = Path("/nas2/gfm-metagenomic-benchmark-paper/figures")


def per_genus(path):
    return {g["genus_name"]: g for g in json.load(open(path))["primary"]["per_genus"]}


r1 = {
    "nt": per_genus(ROOT / "out/enhanced_rep1/ntv2.json"),
    "mt": per_genus(ROOT / "out/enhanced_rep1/mt13.json"),
    "k2": per_genus(ROOT / "out/enhanced_rep1/kraken2bracken.json"),
}
r2 = {
    "nt": per_genus(ROOT / "rep2/out/enhanced/ntv2.json"),
    "mt": per_genus(ROOT / "rep2/out/enhanced/mt13.json"),
    "k2": per_genus(ROOT / "rep2/out/enhanced/kraken2bracken.json"),
}

# order by expected descending
gens = sorted(
    r1["nt"].keys(),
    key=lambda g: -r1["nt"][g]["expected_renorm"],
)

exp = np.array([r1["nt"][g]["expected_renorm"] * 100 for g in gens])
nt = np.array([
    (r1["nt"][g]["pred_renorm"] + r2["nt"][g]["pred_renorm"]) / 2 * 100 for g in gens
])
mt = np.array([
    (r1["mt"][g]["pred_renorm"] + r2["mt"][g]["pred_renorm"]) / 2 * 100 for g in gens
])
k2 = np.array([
    (r1["k2"][g]["pred_renorm"] + r2["k2"][g]["pred_renorm"]) / 2 * 100 for g in gens
])

x = np.arange(len(gens))
w = 0.2
fig, ax = plt.subplots(figsize=(7.2, 3.6))
ax.bar(x - 1.5 * w, exp, w, label="Expected", color="#444444")
ax.bar(x - 0.5 * w, nt, w, label="NT-v2", color=figstyle.BLUE)
ax.bar(x + 0.5 * w, mt, w, label="MT 13-mer", color=figstyle.TEAL)
ax.bar(x + 1.5 * w, k2, w, label="Kraken2+Bracken", color=figstyle.GREY)
ax.set_xticks(x)
ax.set_xticklabels(gens, rotation=45, ha="right")
ax.set_ylabel("In-set renormalized abundance (%)")
ax.set_title("D6331 mock community (mean of two replicates)")
ax.legend(frameon=False, ncol=2)
fig.tight_layout()
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "mock_per_genus.pdf")
fig.savefig(OUT / "mock_per_genus.png", dpi=200)
print("wrote", OUT / "mock_per_genus.pdf")
