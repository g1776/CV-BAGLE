import os
import sys
import glob
import random
import numpy as np
from pathlib import Path
import pickle
from pprint import pprint
sys.path.append(
    os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
)

from pipeline import pipeline
from features import calc_glyph_features, calc_label_features


CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "raw") # I apologize
CHART_TYPE = "pie-chart"
chart_folder = os.path.join(CHARTS_DIR, CHART_TYPE)
N = 5

for _ in range(N):
    
    chart_fp = random.choice(glob.glob(os.path.join(chart_folder, '*.pkl')))


    with open(chart_fp, 'rb') as f:
        truth = pickle.load(f)

    extraction = pipeline(chart_fp, VISUALIZE=True)

    # The sets defined in the flowchart:
    G_l = extraction.glyphs.large
    G_s = extraction.glyphs.small
    G = [*extraction.glyphs.large, *extraction.glyphs.small]
    L = extraction.labels

    # calculate features
    F_L = calc_label_features(L)
    F_G = calc_glyph_features(G)
    F = np.concatenate([F_L, F_G])


    c = None # get_chart_type(F)

    print("--- Output ---")
    print("Chart Type", c)
    print("Glyphs:", F_G)
    print("Labels:", F_L)
    print("Features:", F)