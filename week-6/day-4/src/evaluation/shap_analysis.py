import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path("src/data/processed")
MODEL_DIR = Path("src/models")
EVAL_DIR = Path("src/evaluation")

X_train = pd.read_csv(DATA_DIR / "X_train.csv")
model = joblib.load(MODEL_DIR / "best_model.pkl")

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_train)

if isinstance(shap_values, list):
    shap_to_plot = shap_values[1]   # positive class
else:
    shap_to_plot = shap_values

plt.figure()
shap.summary_plot(shap_to_plot, X_train, show=False)
plt.tight_layout()
plt.savefig(EVAL_DIR / "shap_summary.png")
plt.close()

print("SHAP summary plot saved successfully")
