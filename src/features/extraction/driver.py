import os
import sys
import glob
import random
import numpy as np
from pathlib import Path
sys.path.append(
    os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
)

from pipeline import pipeline
from features import calc_glyph_features, calc_label_features


CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "raw") # I apologize
CHART_TYPE = "line-chart"
chart_folder = os.path.join(CHARTS_DIR, CHART_TYPE)
N = 5

for _ in range(N):
    
    chart_fp = random.choice(glob.glob(os.path.join(chart_folder, '*.pkl')))

    extraction = pipeline(chart_fp, VISUALIZE=True)

    # The sets defined in the flowchart:
    G_l = extraction.glyphs.large
    G_s = extraction.glyphs.small
    G = [*extraction.glyphs.large, *extraction.glyphs.small]
    L = extraction.labels

    # get mapping from pixel to coordinate system in graph
    mapping = lambda pixel: 1*pixel # pixel2coordinate(L)

    # calculate features
    F_L = calc_label_features(L)
    F_G = calc_glyph_features(G)
    F = np.concatenate([F_L, F_G])


    c = None # get_chart_type(F)

    # filter L and G by chart type
    L_f = L # filter_labels(L, c)
    G_f = G # filter_glyphs(G, c)

    print("--- Output ---")
    print("Chart Type", c)
    print("Pixel to Coordinate Mapping", mapping)
    print("Glyphs:", F_G)
    print("Labels:", F_L)
    print("Features:", F)