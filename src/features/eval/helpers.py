import numpy as np
import cv2
import pandas as pd

class Metric:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        # check if var is a int or float
        if isinstance(self.value, int) or isinstance(self.value, float):
            return self.name + ": " + f'{self.value}'
        elif isinstance(self.value, list):
            return self.name + ": " + f'{self.value}'
            
        
    __str__ = __repr__

class Eval:
    def __init__(self, label_metrics, glyph_metrics):
        self.label_metrics = label_metrics
        self.glyph_metrics = glyph_metrics

    def to_list(self):
        out = []
        for metric in self.label_metrics:
            out.append({"name": metric.name, "value": metric.value, "type": "label"})
        for metric in self.glyph_metrics:
            out.append({"name": metric.name, "value": metric.value, "type": "glyph"})
        return out
        
    def __repr__(self):
        return "Label Metrics: " + str(self.label_metrics) + "\nGlyph Metrics: " + str(self.glyph_metrics)
    __str__ = __repr__

def pct_extracted(truth, pred):
    return len(list(set(truth.labels) & set(pred.labels))) / len(set(truth.labels))

def clean_labels(labels):
    clean = []
    for label in labels:
        if label != None:
            label = str(label)

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

def map_point_to_glyph(pred, truth, dist_f=lambda pred, truth: pred - truth, starting_dist=np.inf):
    matched_idxs = {} # the indices matched in the truth data
    for pred_val in pred:
        min_dist = starting_dist
        min_idx = -1
        for idx, true_val in enumerate(truth):
            dist = abs(dist_f(pred_val, true_val))
            if dist < min_dist:
                min_dist = dist
                min_idx = idx
        if str(min_idx) in matched_idxs:
            # check if smaller than current closest point to the bar at min_idx
            if min_dist < matched_idxs[str(min_idx)]:
                matched_idxs[str(min_idx)] = min_dist
        else:
            matched_idxs[str(min_idx)] = min_dist
    
    return matched_idxs

def contour_center(contour):
    # get cv2 bounding box
    x, y, w, h = cv2.boundingRect(contour)
    return (x + w/2, y + h/2)

def normalize(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))