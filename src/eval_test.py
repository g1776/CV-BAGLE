import os
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import glob
import pickle
sys.path.extend([
    os.path.join(Path(os.path.abspath(__file__)).parent, 'features/extraction'),
    os.path.join(Path(os.path.abspath(__file__)).parent, 'features/gen')
])
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score


from pipeline import pipeline
from features import calc_large_glyph_features, calc_small_glyph_features, calc_label_features

def get_chart_features(chart_fp):

    extraction = pipeline(chart_fp, VISUALIZE=False, test=True)

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

if __name__ == "__main__":
    MODEL_FP = r"C:\Users\grego\Documents\GitHub\DataVizCaptionGeneration\src\models\rf_clf.pkl"
    TEST_DIR = r"C:\Users\grego\Documents\GitHub\DataVizCaptionGeneration\volume\test"
    
    y_pred = []
    y_test = []
    

    clf = pickle.load(open(MODEL_FP, 'rb'))
    for chart_folder in glob.glob(os.path.join(TEST_DIR, '*')):
        chart_fps = glob.glob(os.path.join(chart_folder, '*.*'))
        chart_type = os.path.basename(chart_folder)
        for chart_fp in chart_fps:
            try:
                chart_features = get_chart_features(chart_fp)
                c = clf.predict(chart_features)[0]

                y_pred.append(c.replace("-test",""))
                y_test.append(chart_type.replace("-test",""))
                print("Truth: {}\tPrediction: {}".format(chart_type, c))
            except:
                print("Error:", chart_fp)

    # display confusion matrix
    fig, ax = plt.subplots(1,1, figsize=(12,12))
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, include_values=True, xticks_rotation='vertical', ax=ax, cmap="YlOrRd")

    # save as svg
    fig.savefig("test_confusion_matrix.svg")

    print("Accuracy:", accuracy_score(y_test, y_pred))
    plt.show()