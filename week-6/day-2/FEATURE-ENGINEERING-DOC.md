# Feature Engineering & Feature Selection

## Project: Titanic Dataset

**Day 2 — Feature Engineering Pipeline**

---

## Objective

Build a reusable feature engineering pipeline that:

* Encodes categorical variables
* Transforms numerical features
* Generates new features
* Applies feature selection
* Produces model-ready train/test datasets

---

## Folder Structure

```
features/
├── build_features.py
├── feature_selector.py
├── feature_list.json

data/processed/
├── final.csv
├── X_train.csv
├── X_test.csv
├── y_train.csv
├── y_test.csv
├── feature_importance.png
```

---

## Feature Engineering Steps

### 1. Input Data

* Source: `data/processed/final.csv`
* Cleaned dataset from Day-1 pipeline

### 2. Encoding

* `Sex` → Label encoded (male = 0, female = 1)

### 3. Feature Generation

Generated 10+ features:

* AgeGroup
* Fare_log
* Fare_sqrt
* IsChild
* IsSenior
* HighFare
* FamilySize
* IsAlone
* Pclass_sq
* Age_Fare

### 4. Feature Scaling

* Applied `StandardScaler` to all numerical features

### 5. Train/Test Split

* 80% Train / 20% Test
* Stratified on target (`Survived`)
* `random_state = 42`

---

## Feature Selection

### Correlation Filter

* Removed features with correlation > 0.9

### Mutual Information

* Ranked features using `mutual_info_classif`
* Top 10 features plotted and saved

---

## Outputs

* Model-ready datasets (`X_train`, `X_test`, `y_train`, `y_test`)
* Feature importance plot
* Final feature list saved as JSON

---

## Status

✔ Feature pipeline implemented
✔ Feature selection applied
✔ Artifacts saved successfully

---
