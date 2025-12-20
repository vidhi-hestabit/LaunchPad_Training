import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

df = pd.read_csv("salary_data.csv")

# REMOVE AGE COMPLETELY
X = df.drop(["expected_package_lpa", "age"], axis=1)
y = df["expected_package_lpa"]

categorical = ["primary_tech", "education_level"]
numerical = ["experience_years", "tech_count"]

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ("num", StandardScaler(), numerical)
    ]
)

model = RandomForestRegressor(
    random_state=42,
    n_estimators=300,
    max_depth=12,
    min_samples_leaf=3
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

pipeline.fit(X_train, y_train)

preds = pipeline.predict(X_test)

print("MAE:", mean_absolute_error(y_test, preds))
print("R²:", r2_score(y_test, preds))

feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
importances = pipeline.named_steps["model"].feature_importances_

print("\nFeature importance:")
for f, imp in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
    print(f"{f}: {imp:.3f}")

plt.figure(figsize=(6,6))
plt.scatter(y_test, preds, alpha=0.7)
plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--")
plt.xlabel("Actual Package (LPA)")
plt.ylabel("Predicted Package (LPA)")
plt.title("Actual vs Predicted Salary")
plt.grid(True)
plt.show()

os.makedirs("ml_service/models", exist_ok=True)
joblib.dump(pipeline, "ml_service/models/model.joblib")
print("Model saved successfully")
