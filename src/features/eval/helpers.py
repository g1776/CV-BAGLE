class Metric:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return self.name + ": " + f'{self.value:.2f}'
    __str__ = __repr__

class Eval:
    def __init__(self, label_metrics, glyph_metrics):
        self.label_metrics = label_metrics
        self.glyph_metrics = glyph_metrics
    def __repr__(self):
        return "Label Metrics: " + str(self.label_metrics) + "\nGlyph Metrics: " + str(self.glyph_metrics)
    __str__ = __repr__

def pct_extracted(truth, pred):
    return len(list(set(truth.labels) & set(pred.labels))) / len(set(truth.labels))

def clean_labels(labels):
    clean = []
    for label in labels:
        if label != None:

            # tokenize by spaces
            words = label.split(" ")

            # remove special characters  and empty strings
            words_clean = [''.join(c for c in word if c.isalnum()) for word in words]
            words_clean = [word for word in words_clean if len(word) > 0]

            # make all words lowercase
            words_clean = [word.lower() for word in words_clean]

            # add to cumulative list
            clean.extend(words_clean)
    return clean
