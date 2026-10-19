"""Fill Topic02_Research_Data_Analysis.ipynb with solutions (cells replaced by index)."""
import json
import sys

SRC = sys.argv[1]
DST = sys.argv[2]

nb = json.load(open(SRC, encoding="utf-8"))
cells = nb["cells"]


def code(src):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
            "source": src.strip("\n").splitlines(keepends=True)}


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.strip("\n").splitlines(keepends=True)}


def set_cell(i, new):
    cells[i] = new


# --- 7/8 Exercise 1.1 ------------------------------------------------------
set_cell(8, code('''
# 1. shape, dtypes, missing counts
print("Shape:", df.shape)
print()
print(df.dtypes)
print()
print("Missing values per column:")
print(df.isna().sum())

# 2. share of rows with at least one missing value
rows_with_na = df.isna().any(axis=1).sum()
print()
print(f"Rows with at least one missing value: {rows_with_na} / {len(df)}"
      f" ({rows_with_na / len(df):.1%})")
'''))

# --- 9/10 Exercise 1.2 -----------------------------------------------------
set_cell(10, code('''
# 1. histogram of salary
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

sns.histplot(df["salary"].dropna(), bins=30, kde=True, ax=axes[0])
axes[0].set_title("Distribution of salary")
axes[0].set_xlabel("Salary")

# 2. boxplot of salary by department
sns.boxplot(data=df, x="department", y="salary", ax=axes[1])
axes[1].set_title("Salary by department")
axes[1].set_xlabel("Department")

plt.tight_layout()
plt.show()
'''))

set_cell(11, md('''
**Observations.**

* The salary histogram is dominated by a handful of extreme values on the far right: a few
  points sit around 4× the maximum normal salary (~200k+ while the bulk of the distribution is
  between 20k and 70k). The KDE curve is almost flat because of them, and the "real" distribution
  is squashed into the left edge of the plot.
* The boxplot makes the problem obvious: every department has a normal-looking box around
  45k, plus a long tail of outliers above the upper whisker — and in each department a single
  point sits at roughly 200k. These come from the injected `salary.max() * 4` values, not from
  any real department-level effect.
* The department medians are almost identical, which is expected: salary was generated
  independently of department in the synthetic data.
'''))

# --- 13 Exercise 1.3 -------------------------------------------------------
set_cell(13, code('''
def flag_outliers_iqr(series):
    """Boolean mask of values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]."""
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return (series < lower) | (series > upper)


outlier_mask = flag_outliers_iqr(df["salary"])
print("Outliers found (missing salaries excluded):", outlier_mask.sum())
print()
print("Bounds for salary:",
      round(df["salary"].quantile(0.25) - 1.5 * (df["salary"].quantile(0.75) - df["salary"].quantile(0.25)), 2),
      "…",
      round(df["salary"].quantile(0.75) + 1.5 * (df["salary"].quantile(0.75) - df["salary"].quantile(0.25)), 2))
print()
print(df.loc[outlier_mask, ["salary", "department"]].sort_values("salary"))

# same flagging, convenient for any other column:
for col in ["age", "salary", "years_exp"]:
    print(f"{col:>10}: {flag_outliers_iqr(df[col]).sum()} outliers")
'''))

# --- 15 Exercise 1.4 -------------------------------------------------------
set_cell(15, code('''
numeric = df.select_dtypes(include="number")
corr = numeric.corr()

plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, square=True)
plt.title("Correlation matrix — synthetic employee data")
plt.tight_layout()
plt.show()

corr
'''))

# --- Part 2 dataset load ---------------------------------------------------
set_cell(17, code('''
DATA_PATH = "housing.csv"  # adjust if needed
housing = pd.read_csv(DATA_PATH)
housing.head()
'''))

# --- 19 Exercise 2.1 -------------------------------------------------------
set_cell(19, code('''
# 1. info / describe / missing values
housing.info()
print()
print(housing.describe().T)
print()
print("Missing values per column:")
print(housing.isna().sum())

# 2. value counts for ocean_proximity
print()
print(housing["ocean_proximity"].value_counts())
'''))

# --- 21 Exercise 2.2 -------------------------------------------------------
set_cell(21, code('''
housing.hist(bins=50, figsize=(12, 10))
plt.tight_layout()
plt.show()
'''))

set_cell(22, md('''
**Observations on skew.**

* `median_house_value` is **capped** at 500001 — a spike at the right edge. That price ceiling
  is a data artefact, not a real distribution; it has to be removed or handled explicitly
  (the rows above the cap must be dropped or clipped), otherwise the model cannot learn the
  true relationship for expensive districts.
* `median_income` is right-skewed, but note it is already capped at ~15 (15k$/month) and
  expressed in tens of thousands — mostly between 1 and 6.
* `population`, `total_rooms`, `total_bedrooms`, `households` are all strongly right-skewed with
  a long tail: a few districts with tens of thousands of people next to the typical few
  thousand. A **log transform** (`np.log1p`) would make them much closer to normal — helpful
  for distance-based models and for any model assuming roughly symmetric errors.
* `housing_median_age` is roughly uniform with a spike at its own cap of 52 years.
* `latitude` and `longitude` are not skewed (bimodal / geographic, no transformation needed) —
  they should not be log-transformed.

So: log-transform the count-like features, do **not** log-transform age, lat/lon or the target
itself without checking the cap first.
'''))

# --- 23 Exercise 2.3 -------------------------------------------------------
set_cell(23, code('''
plt.figure(figsize=(12, 9))
sc = plt.scatter(
    housing["longitude"], housing["latitude"],
    c=housing["median_house_value"], cmap="jet",
    s=housing["population"] / 60, alpha=0.35, linewidths=0,
)
plt.colorbar(sc, label="Median house value ($)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("California housing map — colour = house value, size = population")
plt.legend(*sc.legend_elements("sizes", num=4, fmt="${x:.0f}"), title="Population",
           loc="upper left", labelspacing=1.2)
plt.tight_layout()
plt.show()
'''))

# --- 25 Exercise 2.4 -------------------------------------------------------
set_cell(25, code('''
# 1. correlation of each numeric feature with the target
corr_target = (housing.select_dtypes(include="number")
               .corr()["median_house_value"]
               .drop("median_house_value")
               .sort_values(ascending=False))
print(corr_target)

# 2. top three features by absolute correlation
top_features = corr_target.abs().sort_values(ascending=False).head(3).index.tolist()
print()
print("Top 3:", top_features)

# 3. scatter matrix of the top features + target
pd.plotting.scatter_matrix(housing[top_features + ["median_house_value"]],
                           figsize=(11, 11), alpha=0.4, diagonal="hist")
plt.suptitle("Scatter matrix — top features vs target", y=1.02)
plt.show()
'''))

# --- Wrap-up: append answers -------------------------------------------------
cells.append(md('''
---
## Wrap-up answers

**1. Three data-quality issues to fix before modeling**

1. **Missing `total_bedrooms`** (207 rows). Impute — e.g. the median *within the same
   `ocean_proximity`* or the median `total_rooms`-ratio — or drop those rows; either way the
   imputer must be fitted on the training set only.
2. **The target cap at `median_house_value == 500001`** (and the `median_income` / `housing_median_age`
   caps). Those rows are censored data: the model learns a flat "ceiling" region that does not
   exist in reality. Either drop those districts or model the value as censored / clip explicitly
   and document the decision.
3. **Heavy right-skew and wildly different scales** in `total_rooms`, `total_bedrooms`,
   `population`, `households`, `median_income`. Fix with log transforms and/or a `StandardScaler`
   — again fitted on train only.
   (Runner-up: `ocean_proximity` is a string — it needs encoding; and there is no unit-consistent
   "household" feature, so room counts are not comparable between districts of different size.)

**2. Why EDA on the training set only?**

EDA is itself a modelling step: every decision it drives (which outliers to clip, which
imputation strategy, which transforms, which features to keep, which correlations to trust) is a
parameter learned from the data. If you inspect the full dataset — including the test set — then
your choices are informed by the test data. That is data leakage: the test set no longer
simulates truly unseen data, the reported score becomes optimistically biased, and the
"hold-out" estimate can no longer be trusted. Practical recipe: split first, run all statistics
and plots on `train`, only transform `test` with the fit-from-train statistics.

**3. A feature to engineer: rooms per household**

```python
housing["rooms_per_household"] = housing["total_rooms"] / housing["households"]
```

Why it might help: raw `total_rooms` measures the **size of the district**, not the size of a
home — a big district trivially has many rooms, which drowns out the information about living
space. Dividing by `households` normalises it into "rooms per dwelling", which is close to the
thing that actually determines the price per house. It usually correlates with the target more
strongly than `total_rooms` and removes much of the population-size confound.

Once that is fixed, continue with the standard ratio features:

```python
housing["bedrooms_ratio"] = housing["total_bedrooms"] / housing["total_rooms"]
housing["population_per_household"] = housing["population"] / housing["households"]
```

Houses with a low bedroom ratio are typically larger/more luxurious per room, and
`population_per_household` captures crowding — both are known to improve California-housing models.
'''))

nb["cells"] = cells
json.dump(nb, open(DST, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", DST, "cells:", len(cells))
