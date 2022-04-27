from helpers import Eval, Metric

def pie_chart(pred, truth):
    
    labels_metric = len(list(set(truth.labels) & set(pred.labels))) / len(set(truth.labels))

    return Eval(
        label_metrics=[Metric(r"% of labels extracted", labels_metric)],
        glyph_metrics=[])
