import os
import sys
import glob
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action="ignore", category=RuntimeWarning)
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
sys.path.append(
    os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
)
from multiprocessing import Pool

from pipeline import pipeline
from features import calc_large_glyph_features, calc_small_glyph_features, calc_label_features


CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "raw") # I apologize
CHART_TYPE = "vertical-bar-chart"
chart_folder = os.path.join(CHARTS_DIR, CHART_TYPE)

OUT_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "processed")
OUT_FILE = os.path.join(OUT_DIR, "features.pkl")

chart_type_folders = glob.glob(os.path.join(CHARTS_DIR, '*'))

def get_features_for_chart_in_folder(folder):
    out = []

    chart_type = os.path.basename(folder)
    print(f"Chart Type {chart_type}")

    chart_fps =glob.glob(os.path.join(folder, '*.pkl'))
    num_chart_fps = len(chart_fps)
    for chart_idx, chart_fp in enumerate(chart_fps):

        try:
            if chart_idx % 25 == 0:
                print(f"Chart {chart_idx}/{num_chart_fps} ({os.path.basename(chart_fp)})")


            extraction = pipeline(chart_fp, VISUALIZE=False)

            # The sets defined in the flowchart:
            G_l = extraction.glyphs.large
            G_s = extraction.glyphs.small
            L = extraction.labels

            # calculate features
            F_L = calc_label_features(L)
            F_G_l = calc_large_glyph_features(G_l)
            F_G_s = calc_small_glyph_features(G_s)
            F_G = F_G_l + F_G_s
            F = F_L + F_G

            # add IDs
            F = [chart_type] + F + [chart_fp]
            out.append(F)

        except:
            print(f"Error with chart {chart_fp}")
            continue

    return out

if __name__ == '__main__':

    df_list = []

    with Pool() as p:
        out = p.imap(get_features_for_chart_in_folder, chart_type_folders)
        for row in out:
            for dp in row:
                df_list.append(dp)

    pickle.dump(df_list, open(OUT_FILE, 'wb'))

    print("\nDONE!!!!!!!")