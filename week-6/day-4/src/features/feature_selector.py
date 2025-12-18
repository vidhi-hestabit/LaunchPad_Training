import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif

X_train = pd.read_csv("/home/vidhiajmera/launchpad/week-6/day-2/src/data/processed/X_train.csv")
y_train = pd.read_csv("/home/vidhiajmera/launchpad/week-6/day-2/src/data/processed/y_train.csv").values.ravel()

# ---------- Correlation Filter ----------
corr = X_train.corr().abs()
upper = corr.where(
    np.triu(np.ones(corr.shape), k=1).astype(bool)
)
to_drop = [col for col in upper.columns if any(upper[col] > 0.9)]

X_corr_filtered = X_train.drop(columns=to_drop)

# ---------- Mutual Information ----------
mi_scores = mutual_info_classif(X_corr_filtered, y_train)
mi_series = pd.Series(mi_scores, index=X_corr_filtered.columns)
mi_series = mi_series.sort_values(ascending=False)

# ---------- Plot Feature Importance ----------
plt.figure(figsize=(10, 6))
mi_series.head(10).plot(kind="bar")
plt.title("Top 10 Feature Importance (Mutual Information)")
plt.tight_layout()
plt.savefig("/home/vidhiajmera/launchpad/week-6/day-2/src/data/processed/feature_importance.png")
plt.close()


print("Dropped correlated features:", to_drop)
