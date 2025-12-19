import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import confusion_matrix

DATA_DIR = Path("src/data/processed")
MODEL_DIR = Path("src/models")
EVAL_DIR = Path("src/evaluation")

X_test = pd.read_csv(DATA_DIR / "X_test.csv")
y_test = pd.read_csv(DATA_DIR / "y_test.csv").values.ravel()

model = joblib.load(MODEL_DIR / "best_model.pkl")

y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Error Analysis – Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig(EVAL_DIR / "error_heatmap.png")
plt.close()

print("Error analysis heatmap saved")
