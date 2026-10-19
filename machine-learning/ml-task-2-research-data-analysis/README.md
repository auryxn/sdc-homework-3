# ML Task 2 — Research (Exploratory) Data Analysis

**Subject:** Machine Learning · **Course:** 2026 HR S5 Machine Learning
**Task id:** `ml-task-2-research-data-analysis`
**Status:** Done — all exercises solved, notebook executed end-to-end with outputs.

---

## 1. Task

A 3-hour self-directed seminar on exploratory data analysis (EDA): structure/quality checks,
missing values, distributions, IQR outlier detection, correlations — first on a synthetic
dataset with injected problems, then on the real California Housing dataset.

| Part | Exercises | What was asked |
|---|---|---|
| 1 — Dummy dataset | 1.1 | shape, dtypes, missing counts, % rows with any missing value |
| 1 — Dummy dataset | 1.2 | salary histogram, salary-by-department boxplot + observations |
| 1 — Dummy dataset | 1.3 | `flag_outliers_iqr(series)` + apply to `salary` |
| 1 — Dummy dataset | 1.4 | correlation matrix + heatmap, most correlated pair |
| 2 — California Housing | 2.1 | `.info()` / `.describe()`, missing values, `ocean_proximity` counts |
| 2 — California Housing | 2.2 | histograms of all numeric columns, skew discussion |
| 2 — California Housing | 2.3 | geographic scatter (lat/lon, colour = value, size = population) |
| 2 — California Housing | 2.4 | correlation with target, top-3 features, scatter matrix |
| Wrap-up | — | 3 questions: quality issues, why EDA on train only, feature idea |

---

## 2. Repository layout

```
ml-task-2-research-data-analysis/
├── notebook/
│   ├── task-2-research-data-analysis.ipynb   # solved + executed notebook (deliverable)
│   └── original_task.ipynb                   # the blank seminar notebook as provided
├── data/
│   └── housing.csv                           # California Housing (20 640 rows, Kaggle)
├── scripts/
│   └── fill_notebook.py                      # fills the blank notebook with the solutions
└── requirements.txt
```

## 3. How to run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebook/task-2-research-data-analysis.ipynb
```

The notebook reads `../data/housing.csv`, so it works from `notebook/` after `Run All`.
Reproduce the solved notebook from the blank one:

```bash
python scripts/fill_notebook.py notebook/task-2-research-data-analysis.ipynb
jupyter nbconvert --to notebook --execute --inplace notebook/task-2-research-data-analysis.ipynb
```

**Environment used:** Python 3.14, NumPy 2.5, Pandas 3.0, Matplotlib 3.11, seaborn 0.13.

---

## 4. Results

### Exercise 1.1 — Structural overview

* Shape `(300, 4)`; `department` is categorical, everything else numeric.
* Missing: `salary` 20, `age` 10, `years_exp` 0, `department` 0.
* **9.7 % of rows** (29 / 300) have at least one missing value.

### Exercise 1.2 — Distributions

Salary histogram collapsed to the left edge by five points at ~370k (4× the normal maximum);
boxplot by department shows a normal box around 45k plus a long outlier tail in every
department. Department medians are almost identical — salary was generated independently of
department, so these are injected outliers, not a real effect.

### Exercise 1.3 — IQR outliers

Bounds for `salary`: **11 845 … 80 803**. Flagged **8 outliers**: the five injected ~370k values
plus three ordinary tail values (11.6k, 81.4k, 92.5k). `age`: 5 flagged, `years_exp`: 1.

### Exercise 1.4 — Correlation

No meaningful correlation between the numeric columns (`age`/`salary` −0.08,
`age`/`years_exp` −0.05, `salary`/`years_exp` +0.04). That is expected: the synthetic columns
were drawn independently; the only link is the injected relationship-free outliers.

### Exercise 2.1 — First pass

* 20 640 rows × 10 columns; `ocean_proximity` is the only string column.
* Missing: **`total_bedrooms` 207** (1 %), nothing else.
* `ocean_proximity`: `<1H OCEAN` 9136, `INLAND` 6551, `NEAR OCEAN` 2658, `NEAR BAY` 2290,
  `ISLAND` 5.

### Exercise 2.2 — Distributions and skew

* `median_house_value` is **capped at 500 001** → spike at the edge.
* `median_income` capped at ≈15; `housing_median_age` capped at 52.
* `total_rooms`, `total_bedrooms`, `population`, `households` are strongly right-skewed →
  log (`np.log1p`) helps.
* `latitude` / `longitude` are geographic (bimodal), log would be wrong there.

### Exercise 2.3 — Geography

Classic California map: dense Los Angeles / Bay Area clusters, inland areas cheaper and further
from the coast. Colour scale = house value, size = population.

### Exercise 2.4 — Correlation with the target

| Feature | corr with `median_house_value` |
|---|---|
| `median_income` | **0.688** |
| `total_rooms` | 0.134 |
| `housing_median_age` | 0.106 |
| `households` | 0.066 |
| `total_bedrooms` | 0.050 |
| `population` | −0.025 |
| `longitude` | −0.046 |
| `latitude` | −0.144 |

Top 3 by |corr|: **`median_income`, `latitude`, `total_rooms`**. The scatter matrix shows a clear
upward trend for `median_income`, while `total_rooms` is a weak, fan-shaped relation (district
size, not house size) — a hint that a ratio feature is needed.

---

## 5. Wrap-up answers

1. **Three quality issues.** (a) 207 missing `total_bedrooms` — impute on train only.
   (b) The target is censored at 500 001 (and `median_income` / `housing_median_age` are capped) —
   drop or model explicitly. (c) Heavy right skew and mixed scales in the count features — log
   transform + scaling; plus `ocean_proximity` needs encoding.
2. **EDA on train only.** EDA drives modelling decisions (imputation, clipping, transforms,
   feature choice), i.e. it learns parameters from data. Doing it on the full dataset leaks
   test information into those choices, so the hold-out score stops being an unbiased estimate.
3. **Feature idea.** `rooms_per_household = total_rooms / households` (then `bedrooms_ratio` and
   `population_per_household`): raw `total_rooms` measures district size, the ratio measures the
   dwelling itself and correlates with price much more strongly.
