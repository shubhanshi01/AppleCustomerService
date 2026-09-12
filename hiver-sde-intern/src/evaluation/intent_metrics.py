from sklearn.metrics import accuracy_score, classification_report, f1_score

def intent_metrics(y_true, y_pred):
    return {"accuracy": accuracy_score(y_true, y_pred), "macro_f1": f1_score(y_true, y_pred, average="macro"), "per_class": classification_report(y_true, y_pred, output_dict=True, zero_division=0)}
