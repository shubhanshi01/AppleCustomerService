from sklearn.metrics import precision_recall_fscore_support

def escalation_metrics(y_true, y_pred):
    p, r, f, _ = precision_recall_fscore_support(y_true, y_pred, average="binary", pos_label=True, zero_division=0)
    return {"precision": p, "recall": r, "f1": f}
