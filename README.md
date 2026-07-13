# GFMs for Metagenomic Taxonomic Classification — BIB manuscript

投稿 **Briefings in Bioinformatics（BIB）** 的獨立 LaTeX 專案，文章類型為
**Problem-solving Protocol**。使用 Oxford University Press 官方版型
`oup-authoring-template`（class 檔已內含於本 repo，Overleaf / GitHub Action 直接可編）。

> 論文核心論點：對 150 bp 短讀序列的分類學分類，**tokenization（overlapping 13-mer）
> 比 backbone pre-training 或資料量更決定效能上限**；並提供 read-level / sample-level
> 雙評估與對 Kraken2 的實用建議。

## 檔案結構

```
main.tex                     主文（OUP class, contemporary, numbered 引用）
sections/                    本文各節（\input 進 main.tex）
  01_introduction.tex
  02_challenges.tex          為何 metagenomic read classification 難倒 GFM
  03_benchmark_design.tex    benchmark 設計 + Fig.1 TikZ 架構圖 + leakage 控制
  04_data_scaling.tex        資料規模與 6-mer 飽和
  05_pretraining_vs_tokenization.tex  核心分解 + 「不是 lookup」分析
  06_read_vs_sample.tex      read-level vs sample-level + Kraken2 比較
  07_recommendations.tex     Practical recommendations（BIB 核心要求）
  08_limitations.tex         limitations（closed-set caveat 主動揭露）
  09_endmatter.tex           Conflicts/Funding/Data/Code availability/CRediT/AI 揭露
supplementary.tex            補充材料（獨立 article，可單獨出 PDF）
cover_letter.tex             投稿信（說明為何適合 BIB + AI 揭露）
references.bib               參考文獻
figures/                     主文 7 張向量圖（PDF，字體已統一 DejaVu Sans）
figures_src/                 繪圖原始碼（figstyle.py 共用樣式 + make_figures.py）
oup-authoring-template.cls   OUP 官方 class（內含，勿改）
oup-plain.bst                OUP numbered 引用樣式
oup-abbrvnat.bst             OUP author–year 引用樣式（備用）
.github/workflows/build.yml  自動編譯出 PDF（push 觸發，Artifacts 下載）
```

## 符合 BIB 規定格式（已對齊項目）

依 [BIB 官方投稿規定](https://academic.oup.com/bib/pages/msprep_submission)：

- **Article type**：Problem-solving Protocol（2,000–5,000 字）— `\appnotes{Problem-solving Protocol}`
- **官方版型**：`\documentclass[unnumsec,webpdf,contemporary,large,numbered]{oup-authoring-template}`
- **Key Points**：`\boxedtext{Key Points}{...}`，5 點（規定至多 5 點）
- **Abstract**：結構式 Background/Methods/Results/Conclusion，且**無任何引用**（規定要求）
- **Keywords**：6 個（規定至多 6 個）
- **引用格式**：numbered，按出現順序（方括號 [1, 3–5]，PubMed/Vancouver 慣例）—
  用 `\bibliographystyle{unsrtnat}` + natbib sort&compress。
  ⚠️ **不要用官方 `oup-plain.bst`**：它輸出裸 `\bibitem{key}`，會讓 class 在
  `numbered` 模式下把 natbib 翻回 author-year，導致內文變空的 `[ , ]`、書目無編號。
  `unsrtnat`（有 `\bibitem[label]{key}`）才正常。
- **必備 endmatter**：Conflicts of interest、Funding、Data availability、Code
  availability、Author contributions（CRediT）、Acknowledgments（含 AI 揭露）

## 如何編譯出 PDF

本機（Nano4）無 TeX，用以下任一：

> ⚠️ **務必用 TeX Live 2024（不要用 2026/latest）**。OUP 官方 class 依賴
> `arydshln`，而它被 TeX Live 2026 的新 LaTeX kernel 弄壞——**連 OUP 自己的
> 範例在 2026 都編不過**。TeX Live 2024 可乾淨編譯（已實測 main/supplementary/
> cover_letter 全部 exit 0、引用與交叉參照全解析），且與 Overleaf 投稿環境一致。

### GitHub Action（推薦，push 後自動出 PDF）
`.github/workflows/build.yml` 已釘 `texlive_version: 2024`。push 到 GitHub 後
Actions 自動編譯三份文件，在該次 run 的 **Artifacts** 下載 `manuscript-pdfs`。

### Overleaf
上傳整個 repo → 主文件設 `main.tex` → 編譯器選 **pdfLaTeX** →
**Menu → Settings → TeX Live version 選 2024**（重要，否則會踩到上面的 bug）。

### 本機 / 有 TeX Live 2024 時
```bash
latexmk -pdf main.tex
latexmk -pdf supplementary.tex
latexmk -pdf cover_letter.tex
```

## 投稿前務必補齊（檔案內以 `[...]` / `First Author` / `0000-...` 標出）

- **作者、單位、ORCID、通訊 email**（`main.tex`：`\author`/`\address`/`\corresp`）
- **CRediT 貢獻、Funding、Acknowledgments、Data DOI**（`sections/09_endmatter.tex`）
- **Supplementary 完整超參數與訓練指令**（`supplementary.tex` 標了 `[Insert ...]`）
- **cover_letter.tex** 地址與署名

## 尚未處理的科學風險（投稿前最好先做）

- **P0 out-of-genome generalization 實驗**：closed-set 98.7% 被質疑是 k-mer lookup
  的最大風險。§8 已主動揭露並說明需補；先做完最穩。
- **更完整的真實群落驗證**：D6331 兩 replicates + Kraken2/Bracken + Spearman /
  filtered $r$ / 修正 detection / per-genus 已入主文與 Supplementary；
  仍缺多個 community、matched read length、Centrifuge 等（§8 follow-up）。

## 圖（統一字體 + 數據核對）

主文除 Fig.1（TikZ 架構圖，LaTeX 直接畫）外，其餘圖全部由
`figures_src/make_figures.py` 以**單一共用樣式** `figures_src/figstyle.py` 生成
（DejaVu Sans、統一字級、向量 PDF、字體內嵌），解決先前各圖字體不一（thesis 用
serif、benchmark PNG 用預設字體）的問題。所有數字取自
`benchmark_results/THESIS_NUMBERS.md`（已逐一核對）。

7 張圖：
- `data_scaling.pdf` — NT-v2 6-mer 資料規模飽和（500K→250M）
- `backbone_ablation.pdf` — pre-training vs tokenization 分解（+13.2 / +20.4 pp）
- `rc_tta_benefit.pdf` — RC-TTA 各設定增益（+0.08–1.54 pp）
- `train_fit.pdf` — **新增**：train vs val（6-mer 連訓練都 fit 不了、13-mer 可）
- `kmer_baselines.pdf` — **新增**：13-mer 非 lookup（NB 74.9% > NT-v2 67%）
- `cross_setting_comparison.pdf` — sample-level 豐度 Pearson r + Bray–Curtis
- `tradeoff_abundance_detection.pdf` — **改**：豐度 vs 偵測權衡（取代原誤導的單模型 ROC）

**兩處圖/數據不一致已修**（沿用 thesis 素材造成）：舊 `cross_setting_comparison.png`
其實是 r/BC 條圖卻被寫成散點；舊 `roc_detection.png` 只有單模型、沒有 Kraken2。
圖說已改成與實際圖一致。

重新生成圖：
```bash
conda activate gfm            # 需 matplotlib
cd figures_src && python make_figures.py   # 覆蓋 ../figures/*.pdf
```

## 數字來源

所有數字取自 `benchmark_results/THESIS_NUMBERS.md`（單頁權威表）與
`gfm-classifier/docs/kmer_lookup_analysis.md`（13-mer 非 lookup 分析）。
實驗程式碼在 <https://github.com/m2lab-ntu/gfm-classifier>。

## 授權

`oup-authoring-template.cls` 與 `*.bst` © Oxford University Press，依 LPPL 授權散布。
稿件文字與圖表著作權屬作者。
