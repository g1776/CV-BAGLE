import os
import sys
import glob
import random
import numpy as np
from pathlib import Path
sys.path.append(
    os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
)
import argparse

from pipeline import pipeline
from features import calc_glyph_features, calc_label_features

if __name__ == "__main__":

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", '--chart_type', type=str, default='fit-regression-plot')
    parser.add_argument('-n', '--num_samples', type=int, default=1)
    parser.add_argument('-t', '--test', action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()

    # set constants
    TEST = args.test
    CHART_TYPE = args.chart_type
    N = args.num_samples
    CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "test" if TEST else "raw") # I apologize
    chart_folder = os.path.join(CHARTS_DIR, CHART_TYPE)

    # process N charts
    for _ in range(N):
        

        chart_fp = random.choice(glob.glob(os.path.join(chart_folder, '*.*')))
        extraction = pipeline(chart_fp, VISUALIZE=True, test=TEST)

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