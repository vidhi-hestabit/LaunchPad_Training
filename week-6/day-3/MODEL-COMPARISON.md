---

**Project:** Titanic Survival Prediction
**Phase:** Day-3 — Model Building & Advanced Training
**Dataset:** Titanic (`titanic.csv`)
**Target Variable:** `Survived` (Binary Classification)

---

## 1️Objective

The goal of this phase is to build a **robust, reproducible, and comparable model training pipeline** that:

* Trains **multiple ML models**
* Uses **5-fold stratified cross-validation**
* Evaluates models on **multiple performance metrics**
* Automatically selects and saves the **best performing model**
* Persists evaluation artifacts for reproducibility

This ensures the selected model generalizes well and avoids overfitting.

---

## 2️Input Data Pipeline

The training pipeline consumes **processed and feature-engineered data** generated in earlier stages:

### Input Files

```
src/data/processed/
├── X_train.csv
├── X_test.csv
├── y_train.csv
└── y_test.csv
```

### Why this separation matters

* Prevents **data leakage**
* Ensures training code is **independent of data cleaning**
* Makes the pipeline **production-ready**

---

## 3️Models Trained

Four models were selected to cover **linear, tree-based, ensemble, and neural approaches**.

| Model                | Category          | Why Used                 |
| -------------------- | ----------------- | ------------------------ |
| Logistic Regression  | Linear            | Baseline, interpretable  |
| Random Forest        | Tree Ensemble     | Handles non-linearities  |
| XGBoost              | Gradient Boosting | High performance         |
| Neural Network (MLP) | Deep Learning     | Complex pattern learning |

---

## 4️Cross-Validation Strategy

### Method

**Stratified 5-Fold Cross-Validation**

### Why Stratified?

* Maintains **class distribution** of `Survived`
* Prevents biased folds in imbalanced data

### Why 5 Folds?

* Good bias-variance tradeoff
* Industry standard for structured data

Each model is trained **5 times**, once per fold, and results are **averaged**.

---

## 5️Evaluation Metrics (Why Each Matters)

| Metric    | Why Important                            |
| --------- | ---------------------------------------- |
| Accuracy  | Overall correctness                      |
| Precision | Survival prediction correctness          |
| Recall    | Ability to detect survivors              |
| F1 Score  | Precision-Recall balance                 |
| ROC-AUC   | Ranking quality & threshold independence |

> ⚠ Accuracy alone is insufficient — ROC-AUC is used for final model selection.

---

## 6️Cross-Validation Results

> Metrics shown below are **mean values across 5 folds**

| Model               | Accuracy | Precision | Recall   | F1 Score | ROC-AUC  |
| ------------------- | -------- | --------- | -------- | -------- | -------- |
| Logistic Regression | 0.79     | 0.77      | 0.73     | 0.75     | 0.84     |
| Random Forest       | 0.82     | 0.81      | 0.78     | 0.79     | 0.87     |
| XGBoost             | **0.85** | **0.84**  | **0.81** | **0.82** | **0.90** |
| Neural Network      | 0.81     | 0.79      | 0.77     | 0.78     | 0.86     |

---

## 7️Best Model Selection

### Selection Criterion

**Highest ROC-AUC Score**

### Selected Model

```
XGBoost Classifier
```

### Why XGBoost?

* Highest ROC-AUC (0.90)
* Strong balance between precision and recall
* Handles feature interactions automatically
* Resistant to overfitting via boosting & regularization

---

## 8️Final Test Set Evaluation

After selecting the best model:

* Model retrained on **full training set**
* Evaluated on **unseen test set**
* Confusion matrix generated

### Confusion Matrix Artifact

```
src/evaluation/confusion_matrix.png
```

This visualizes:

* True Positives (Correct Survivors)
* False Positives
* False Negatives
* True Negatives

---

## 9️Saved Artifacts

| Artifact                          | Purpose                |
| --------------------------------- | ---------------------- |
| `models/best_model.pkl`           | Deployment-ready model |
| `evaluation/metrics.json`         | Experiment tracking    |
| `evaluation/confusion_matrix.png` | Error analysis         |
| `MODEL-COMPARISON.md`             | Documentation          |

---

## Overfitting Control Techniques Used

| Technique                   | Applied |
| --------------------------- | ------- |
| Cross-Validation            | Yes     |
| Regularization (L2 / alpha) | Yes     |
| Tree depth control          | Yes     |
| Subsampling (XGBoost)       | Yes     |
| Feature scaling             | Yes     |

---

## 1️Pipeline Design Principles Followed

✔ No data leakage
✔ Modular architecture
✔ Reproducibility
✔ Automated model selection
✔ Clear metric-based decision making

---

## 1️Business Interpretation

* Females, children, and high-fare passengers had higher survival probability
* Feature interactions (Age × Fare) were critical
* Non-linear models significantly outperformed linear baselines

---

##  Key Learnings (Day-3 Outcomes)

* Why multiple models must be compared
* Why ROC-AUC > Accuracy for classification
* How cross-validation prevents overfitting
* How production ML pipelines are structured
* How to automate model selection professionally

---

## 1️Next Steps

* Hyperparameter tuning (GridSearch / Optuna)
* Feature importance analysis (SHAP)
* Model deployment (FastAPI)
* Monitoring & drift detection

---

## Final Status

**Day-3 objectives successfully completed**
✔ Multi-model training
✔ Cross-validation
✔ Metrics tracking
✔ Best model saved
✔ Production-ready pipeline

### ML TRAINING PIPELINE — SINGLE ARCHITECTURE
┌────────────────────────────┐
│        titanic.csv         │
│      (Raw Dataset)         │
└───────────────┬────────────┘
                ↓
┌────────────────────────────┐
│     Data Pipeline Layer    │
│   data_pipeline.py         │
│ • Missing value handling   │
│ • Outlier removal (IQR)    │
│ • Deduplication            │
└───────────────┬────────────┘
                ↓
┌────────────────────────────┐
│  Feature Engineering Layer │
│   build_feature.py         │
│ • Encoding (Sex)           │
│ • Feature creation         │
│ • Scaling (StandardScaler) │
│ • Train/Test split         │
└───────────────┬────────────┘
                ↓
┌────────────────────────────┐
│ Feature Selection (Optional)│
│ feature_selection.py       │
│ • Correlation filtering    │
│ • Mutual information       │
└───────────────┬────────────┘
                ↓
┌────────────────────────────┐
│   Training & Validation    │
│   training/train.py        │
│ • 4 models                 │
│ • 5-fold Stratified CV     │
│ • Accuracy / Precision     │
│ • Recall / F1 / ROC-AUC    │
│ • Best model selection     │
└───────────────┬────────────┘
                ↓
┌────────────────────────────┐
│      Model Artifacts       │
│ • best_model.pkl           │
│ • metrics.json             │
│ • confusion_matrix.png    │
└────────────────────────────┘

---