import os
import sys
import glob
import random
from pathlib import Path
sys.path.append(
    os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
)

from pipeline import pipeline


CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "raw") # I apologize
CHART_TYPE = "vertical-bar-chart"
chart_folder = os.path.join(CHARTS_DIR, CHART_TYPE)
N = 1

for _ in range(N):
    
    chart_fp = random.choice(glob.glob(os.path.join(chart_folder, '*.pkl')))

    extraction = pipeline(chart_fp, VISUALIZE=False)

    # The sets defined in the flowchart:
    G_l = extraction.glyphs.large
    G_s = extraction.glyphs.small
    G = [*extraction.glyphs.large, *extraction.glyphs.small]
    L = extraction.labels

    # get mapping from pixel to coordinate system in graph
    mapping = lambda pixel: 1*pixel # pixel2coordinate(L)

    # calculate label features
    F_L = [] # calc_label_features(L)
    F_G = [] # calc_glyph_features(G)

    c = None # get_chart_type(F_L, F_G)

    # filter L and G by chart type
    L_f = L # filter_labels(L, c)
    G_f = G # filter_glyphs(G, c)

    print("--- Output ---")
    print("Chart Type", c)
    print("Pixel to Coordinate Mapping", mapping)
    print("Glyphs:", G_f)
    print("Labels:", L_f)