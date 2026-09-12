import pandas as pd
from sklearn.metrics import cohen_kappa_score

def agreement(csv_path, human_column, judge_column):
    data = pd.read_csv(csv_path).dropna(subset=[human_column, judge_column])
    if len(data) < 20:
        raise ValueError("Need at least 20 double-scored items for a meaningful agreement check.")
    return {"n": len(data), "exact_agreement": float((data[human_column] == data[judge_column]).mean()), "cohen_kappa": float(cohen_kappa_score(data[human_column], data[judge_column]))}
