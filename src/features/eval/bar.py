import numpy as np
import cv2
from helpers import Eval, Metric, clean_labels

def bar_chart(pred, truth, orient='v'):

    # add labels from data to truth.labels and clean
    truth.labels = clean_labels(truth.labels + truth.data.iloc[:, 0].values.tolist())

    # calculate percent of labels extracted
    labels_metric = len(list(set(truth.labels) & set(pred.labels))) / len(set(truth.labels))

    # calculate the hws of the extracted bars
    rects = list(filter(lambda contour: contour["n_sides"] == 4, pred.glyphs.large))
    pred_hws = np.array(list(map(lambda rect: cv2.boundingRect(rect["contour"])[3 if orient=="v" else 2], rects))) # hw = height/width
    if len(pred_hws) == 0:
        avg_distance = -1
        num_bars_found = 0
    else:
        # normalize truth hws
        truth_hws = truth.data.iloc[:, 1].values
        truth_hws = (truth_hws - np.min(truth_hws)) / (np.max(truth_hws) - np.min(truth_hws))

        # normalize pred hws
        pred_hws = (pred_hws - np.min(pred_hws)) / (np.max(pred_hws) - np.min(pred_hws))
        
        # calculate closest match between truth and pred hws
        matched_idxs = {} # the indices matched in the truth data
        for pred_hw in pred_hws:
            min_dist = np.inf
            min_idx = -1
            for idx, truth_hw in enumerate(truth_hws):
                dist = abs(pred_hw - truth_hw)
                if dist < min_dist:
                    min_dist = dist
                    min_idx = idx
            if str(min_idx) in matched_idxs:
                # check if smaller than current closest point to the bar at min_idx
                if min_dist < matched_idxs[str(min_idx)]:
                    matched_idxs[str(min_idx)] = min_dist
            else:
                matched_idxs[str(min_idx)] = min_dist
        
        avg_distance = np.mean(list(matched_idxs.values()))
        num_bars_found = len(list(matched_idxs.keys()))

    return Eval(
        label_metrics=[Metric(r"% of labels extracted", labels_metric)],
        glyph_metrics=[
            Metric("The average distance between truth and predicted hws", avg_distance),
            Metric(r"% of bars found", num_bars_found / len(truth.data))
        ])
