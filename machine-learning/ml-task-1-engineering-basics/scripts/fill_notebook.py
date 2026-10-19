import json, sys

path = sys.argv[1]
nb = json.load(open(path))

def code(lines):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": lines}

def md(lines):
    return {"cell_type": "markdown", "metadata": {}, "source": lines}

cells = nb["cells"]

# Cell 4: modern sklearn dropped squared=False -> use np.sqrt(...)
cells[4] = code([
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.linear_model import LinearRegression, LogisticRegression\n",
    "from sklearn.metrics import mean_squared_error, r2_score, accuracy_score\n",
    "\n",
    "np.random.seed(42)\n",
    'print("NumPy:", np.__version__, "| Pandas:", pd.__version__)\n',
])

# Exercise 1.1
cells[8] = code([
    "# 1. mean and median price\n",
    'print("Mean price:", df["price_k_eur"].mean())\n',
    'print("Median price:", df["price_k_eur"].median())\n',
    "\n",
    "# 2. count of houses > 100 sqm\n",
    'print("Houses > 100 sqm:", (df["size_sqm"] > 100).sum())\n',
    "\n",
    "# 3. add price_per_sqm column\n",
    'df["price_per_sqm"] = df["price_k_eur"] / df["size_sqm"]\n',
    "\n",
    "# 4. top 5 most expensive houses (sorted)\n",
    'df.sort_values("price_k_eur", ascending=False).head(5)\n',
])

# Exercise 1.2
cells[10] = code([
    "import seaborn as sns\n",
    "sns.set_theme(style=\"whitegrid\")\n",
    "\n",
    'sns.scatterplot(data=df, x="size_sqm", y="price_k_eur", alpha=0.7)\n',
    'plt.xlabel("House size (sqm)")\n',
    'plt.ylabel("Price (thousand EUR)")\n',
    'plt.title("House size vs price")\n',
    "plt.show()\n",
])

# Worked example RMSE fix
cells[12] = code([
    'X = df[["size_sqm"]].values\n',
    'y = df["price_k_eur"].values\n',
    "\n",
    "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
    "\n",
    "model = LinearRegression()\n",
    "model.fit(X_train, y_train)\n",
    "preds = model.predict(X_test)\n",
    "\n",
    'print("R^2:", r2_score(y_test, preds))\n',
    'print("RMSE:", np.sqrt(mean_squared_error(y_test, preds)))\n',
    'print("Learned coefficient:", model.coef_[0], "Intercept:", model.intercept_)\n',
])

# Exercise 2.1
cells[16] = code([
    "# 1. .info() and .describe()\n",
    "titanic.info()\n",
    "titanic.describe(include=\"all\")\n",
    "\n",
    "# 2. missing values per column\n",
    "missing = titanic.isna().sum()\n",
    "missing[missing > 0].sort_values(ascending=False)\n",
    "\n",
    "# 3. overall survival rate\n",
    'print("Survival rate:", titanic["Survived"].mean())\n',
])

# Exercise 2.2
cells[18] = code([
    "t = titanic.copy()\n",
    "\n",
    "# 1. fill Age with median\n",
    't["Age"] = t["Age"].fillna(t["Age"].median())\n',
    "\n",
    "# 2. fill Embarked with most frequent value\n",
    't["Embarked"] = t["Embarked"].fillna(t["Embarked"].mode()[0])\n',
    "\n",
    "# 3. drop Cabin\n",
    't = t.drop(columns=["Cabin"])\n',
    "\n",
    "# 4. one-hot encode Sex and Embarked\n",
    't = pd.get_dummies(t, columns=["Sex", "Embarked"], drop_first=False)\n',
    "\n",
    "t.head()\n",
])

# Exercise 2.3
cells[20] = code([
    "features = [\"Pclass\", \"Age\", \"SibSp\", \"Parch\", \"Fare\",\n",
    "            \"Sex_male\", \"Embarked_C\", \"Embarked_Q\", \"Embarked_S\"]\n",
    "X = t[features].astype(float)\n",
    'y = t["Survived"]\n',
    "\n",
    "X_train, X_test, y_train, y_test = train_test_split(\n",
    "    X, y, test_size=0.2, random_state=42, stratify=y)\n",
    "\n",
    "clf = LogisticRegression(max_iter=1000)\n",
    "clf.fit(X_train, y_train)\n",
    "preds = clf.predict(X_test)\n",
    "\n",
    'print("LogReg accuracy:", accuracy_score(y_test, preds))\n',
    "\n",
    "# majority-class baseline (always predict the most common training label)\n",
    "majority = y_train.mode()[0]\n",
    "baseline = np.full(len(y_test), majority)\n",
    'print("Baseline (always", majority, ") accuracy:", accuracy_score(y_test, baseline))\n',
    "\n",
    "pd.Series(clf.coef_[0], index=features).sort_values(key=abs, ascending=False)\n",
])

# Wrap-up answers
cells.append(md([
    "---\n",
    "## Wrap-up answers\n",
    "\n",
    "1. **Split before fitting** so the test set is truly unseen. Any step that learns from data\n",
    "   (scaling, imputation, feature selection, model fit) must be fitted on train only; otherwise\n",
    "   information from the test set leaks in and the score is optimistically biased — it no longer\n",
    "   estimates performance on new data.\n",
    "2. **Filling Age with the whole-dataset mean is data leakage**: the imputed value (and any\n",
    "   statistics derived from it, plus scaling) sneaks test information into training. It also\n",
    "   makes the test set unrealistically similar to train, so the evaluation is too optimistic.\n",
    "   Correct way: fit a `SimpleImputer`/median on `X_train` and apply it to `X_test`\n",
    "   (e.g. inside a `sklearn.pipeline.Pipeline`).\n",
    "3. Things worth engineering/investigating next:\n",
    "   - `Name` → title (Mr/Mrs/Miss/Master) and family name → family size / group survival,\n",
    "     plus `Ticket` prefix and `Cabin` deck letter (Cabin is dropped, but its first letter is\n",
    "     informative).\n",
    "   - Age binning (child/adult), `Fare` log-transform, group by `Pclass`.\n",
    "   - Handle Sex/Embarked/age inside a `Pipeline` + `ColumnTransformer` to avoid leakage, and\n",
    "     evaluate with cross-validation instead of a single split.\n",
    "   - Try a tree-based model (RandomForest / GradientBoosting) and compare.\n",
]))

json.dump(nb, open(path, "w"), indent=1, ensure_ascii=False)
print("filled", len(cells), "cells")
