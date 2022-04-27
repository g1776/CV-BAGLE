import numpy as np
import random
import matplotlib.pyplot as plt
import cv2
from helpers import Eval, Metric, clean_labels, map_point_to_glyph, normalize

def histogram_chart(pred, truth):

    # add labels from data to truth.labels and clean
    truth.labels = clean_labels(truth.labels + truth.data.iloc[:, 0].values.tolist())

    # calculate percent of labels extracted
    labels_metric = len(list(set(truth.labels) & set(pred.labels))) / len(set(truth.labels))

    # get single giant glyph extracted
    if len(pred.glyphs.large) > 0:
        # get contour with biggest area
        glyph = max(pred.glyphs.large, key=lambda x: cv2.contourArea(x["contour"]))["contour"]
        
        ys = glyph[:, :, 1]
        
        # get "bottom" of glyph (aka zero on the y axis)
        bottom = np.max(ys)

        # normalized bar heights
        pred_heights = normalize(ys - bottom)

        # the number of bins is random between 30 to 40 for 
        # all the histograms, so since we don't know how many bins
        # for this chart in particular, we will randomize again to get a close approximation
        n_bins = random.randint(30, 40)
        truth_heights_approx, _, _ = plt.hist(truth.data, n_bins)
        truth_heights_approx = normalize(truth_heights_approx)

        mapping = map_point_to_glyph(pred_heights, truth_heights_approx)
        
        avg_distance = np.mean(list(mapping.values()))

    else:
        avg_distance = -1

    return Eval(
        label_metrics=[Metric(r"% of labels extracted", labels_metric)],
        glyph_metrics=[
            Metric("The average distance between truth and predicted hws", avg_distance)
        ])
