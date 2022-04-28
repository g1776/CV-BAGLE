import numpy as np
import cv2
import matplotlib.pyplot as plt
from helpers import Eval, Metric, clean_labels, map_point_to_glyph, normalize

def stacked_bar_chart(pred, truth):


    # add labels from data to truth.labels and clean
    truth.labels = clean_labels(truth.labels + list(truth.data.index.values) + list(truth.data.columns))
    
    ax = truth.data.plot(kind="bar",
                    stacked=True)
    
    # get pixels heights of bars
    y_coeff = np.array(ax.transData.transform([(0,1),(1,0)])-ax.transData.transform((0,0)))[0][1]
    truth_heights = []
    for bars in ax.containers:
        for bar in bars:
            truth_heights.append(bar._height * y_coeff)

    # normalize truth_heights
    truth_hws = normalize(np.array(truth_heights))
    

    # calculate percent of labels extracted
    labels_metric = len(list(set(truth.labels) & set(pred.labels))) / len(set(truth.labels))

    # calculate the hws of the extracted bars
    rects = list(filter(lambda contour: contour["n_sides"] == 4, pred.glyphs.large))
    pred_hws = np.array(list(map(lambda rect: cv2.boundingRect(rect["contour"])[3], rects))) # hw = height/width
    
    if len(pred_hws) == 0:
        avg_distance = -1
        pct_bars_found = 0
    else:

        # normalize pred hws
        pred_hws = normalize(pred_hws)
        
        # calculate closest match between truth and pred hws
        matched_idxs = map_point_to_glyph(pred_hws, truth_hws)
        
        avg_distance = np.mean(list(matched_idxs.values()))
        num_bars_found = len(matched_idxs)
        pct_bars_found = num_bars_found / len(truth_hws)

    return Eval(
        label_metrics=[Metric(r"% of labels extracted", labels_metric)],
        glyph_metrics=[
            Metric("The average distance between truth and predicted hws", avg_distance),
            Metric(r"% of bars found", pct_bars_found)
        ])
