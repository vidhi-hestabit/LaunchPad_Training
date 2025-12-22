import numpy as np
import pandas as pd
import joblib


class DriftChecker:
    def __init__(self, model_path, baseline_data_path):
        self.model = joblib.load(model_path)

        baseline = pd.read_csv(baseline_data_path)
        baseline = baseline.select_dtypes(include=[np.number])

        self.base_mean = baseline.mean()
        self.base_std = baseline.std()

    def check_data_drift(self, new_data, threshold=0.1):
        new_data = new_data.select_dtypes(include=[np.number])

        mean_diff = (self.base_mean - new_data.mean()).abs()
        std_diff = (self.base_std - new_data.std()).abs()

        drift = (mean_diff > threshold) | (std_diff > threshold)

        return drift.any(), {
            "mean_diff": mean_diff.to_dict(),
            "std_diff": std_diff.to_dict()
        }

    def log_drift(self, drift_alert, report):
        if drift_alert:
            print("Data drift detected")
        else:
            print("No data drift detected")

        with open("monitoring/drift_log.txt", "a") as f:
            f.write(str(report) + "\n")


if __name__ == "__main__":
    MODEL_PATH = "src/models/best_model.pkl"
    BASELINE_PATH = "src/data/processed/X_train.csv"
    PROD_LOGS = "prediction_logs.csv"

    if not pd.read_csv(PROD_LOGS).shape[0]:
        print("No production data yet")
        exit()

    prod = pd.read_csv(PROD_LOGS)

    checker = DriftChecker(MODEL_PATH, BASELINE_PATH)
    alert, report = checker.check_data_drift(prod)
    checker.log_drift(alert, report)
