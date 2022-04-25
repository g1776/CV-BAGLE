import numpy as np 
import matplotlib.pyplot as plt
import cv2
from zmq import PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_UNSPECIFIED
from helpers import Eval, Metric, clean_labels, map_point_to_glyph, contour_center, normalize

def scatter_chart(pred, truth):
    truth.labels = clean_labels(truth.labels)
    truth.labels += clean_labels(list(truth.data.columns))
    labels_metric = len(list(set(truth.labels) & set(pred.labels))) / len(set(truth.labels))

    # pts = list(filter(lambda contour: contour["shape"] == "polygon", pred.glyphs.small)) #parameters right???
    pts = pred.glyphs.small
    pred_coords = np.array(list(map(lambda pt: contour_center(pt["contour"]), pts)))
  

    #taken from bar.py
    if len(pred_coords) == 0:
        mapping = {'0': -1}


    else:
        # normalize truth hws
        truth_coords = truth.data.values

        # flip ys
        pred_coords[:, 1] = 1 - pred_coords[:, 1]

        # normalize data
        truth_coords = np.apply_along_axis(normalize, 0, truth_coords)
        pred_coords = np.apply_along_axis(normalize, 0, pred_coords)
        

        # calculate closest match between truth and pred hws
        mapping = map_point_to_glyph(pred_coords, truth_coords, dist_f=lambda pred_coord, truth_coord: np.linalg.norm(pred_coord - truth_coord))
        

    return Eval(
        label_metrics=[Metric(r"% of labels extracted", labels_metric)],
        glyph_metrics=[
            Metric("The average Euclidean distance from glyph to mapped truth", np.mean(list(mapping.values())))
        ])
