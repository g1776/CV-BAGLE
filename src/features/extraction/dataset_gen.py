import os
import sys
import glob
import random
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from pathlib import Path
sys.path.append(
    os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
)
from multiprocessing import Pool

from pipeline import pipeline
from features import calc_glyph_features, calc_label_features


CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "raw") # I apologize
CHART_TYPE = "vertical-bar-chart"
chart_folder = os.path.join(CHARTS_DIR, CHART_TYPE)

OUT_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "processed")
OUT_FILE = os.path.join(OUT_DIR, "features_fit_histogram.csv")


chart_type_folders = glob.glob(os.path.join(CHARTS_DIR, '*'))

def get_features_for_chart_in_folder(folder):
    out = []

    # for folder_idx, folder in enumerate(chart_type_folders):
    print(f"Folder {folder}")

    chart_type = os.path.basename(folder)

    chart_fps =glob.glob(os.path.join(folder, '*.pkl'))
    num_chart_fps = len(chart_fps)
    for chart_idx, chart_fp in enumerate(chart_fps):

        try:
            if chart_idx % 5 == 0:
                print(f"Chart {chart_idx}/{num_chart_fps} ({chart_fp})")
            

            extraction = pipeline(chart_fp, VISUALIZE=False)

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

    with Pool(processes=12) as p:
        out = p.map(get_features_for_chart_in_folder, [r"C:\Users\grego\Documents\GitHub\DataVizCaptionGeneration\volume\raw\fit-density-histogram-plot"])
        for row in out:
            for dp in row:
                df_list.append(dp)

    df = pd.DataFrame(df_list, columns=[

        # chart type
        'chart_type',

        # label features
        "has_num_labels",
        "num_labels_x_mean",
        "num_labels_y_mean",
        "num_labels_x_std",
        "num_labels_y_std",

        # glyph features
        "sizes_mean", 
        "sizes_std",
        "std_center_x", 
        "std_centers_y",
        "num_sides_mean", 
        "num_sides_std",
        "aspect_ratios_mean", 
        "aspect_ratios_std",
        "num_glyphs",

        # chart file name
        "chart_fp"

    ])
    df.to_csv(OUT_FILE)


    print("\nDONE!!!!!!!")