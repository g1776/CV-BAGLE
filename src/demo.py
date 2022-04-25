import streamlit as st
import pickle
import glob
import os
import random
from pathlib import Path
import pandas as pd
import numpy as np
import sys
sys.path.extend([
    os.path.join(Path(os.path.abspath(__file__)).parent, 'features/extraction'),
    os.path.join(Path(os.path.abspath(__file__)).parent, 'features/gen')
])
import cv2

from pipeline import pipeline
from features import calc_large_glyph_features, calc_small_glyph_features, calc_label_features

CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent, "volume", "raw")
MODEL_FP = r"C:\Users\grego\Documents\GitHub\DataVizCaptionGeneration\src\models\rf_clf.pkl"
clf = pickle.load(open(MODEL_FP, 'rb'))

def get_chart_features(extraction):

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


    return pd.DataFrame([F], columns=[
        # label features
        "n_labels",
        "n_num_labels",
        "num_labels_x_mean",
        "num_labels_y_mean",
        "num_labels_x_std",
        "num_labels_y_std",

        # glyph features
        "sizes_mean_large", 
        "sizes_std_large",
        "std_center_x_large", 
        "std_centers_y_large",
        "num_sides_mean_large", 
        "num_sides_std_large",
        "aspect_ratios_mean_large", 
        "aspect_ratios_std_large",
        "num_glyphs_large",
        "std_center_x_small", 
        "std_centers_y_small",
        "num_glyphs_small",
        "aspect_ratios_mean_small", 
        "aspect_ratios_std_small"
    ])



st.markdown("# CV-BAGLE")
st.markdown("## Computer Vision-BAsed Glyph and Label Extraction")

random_file = st.button("Get chart from training data")

col1, col2 = st.columns(2)

if random_file:
    chart_folder = random.choice(glob.glob(os.path.join(CHARTS_DIR, '*')))
    chart_fp = random.choice(glob.glob(os.path.join(chart_folder, '*.pkl')))
    extraction = pipeline(chart_fp, VISUALIZE=True, CV2_VISUALIZE=False)
    features = get_chart_features(extraction).melt(var_name="feature", value_name="value")
    c = clf.predict(features.value.values.reshape(1, -1))[0]
    

    with col1:
        st.image(cv2.cvtColor(extraction.img, cv2.COLOR_BGR2RGB), use_column_width=True)
    
    with col2:
        st.markdown(f"##### Predicted chart class: {c}")
        st.dataframe(features)