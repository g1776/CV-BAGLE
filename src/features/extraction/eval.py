import cv2
import matplotlib.pyplot as plt

def pct_extracted(truth, pred):
    return len(list(set(truth.labels) & set(pred.labels))) / len(set(truth.labels))

def clean_labels(labels):
    clean = []
    for label in labels:
        if label != None:

            # tokenize by spaces
            words = label.split(" ")

            # remove special characters  and empty strings
            words_clean = [''.join(c for c in word if c.isalnum()) for word in words]
            words_clean = [word for word in words_clean if len(word) > 0]

            # make all words lowercase
            words_clean = [word.lower() for word in words_clean]

            # add to cumulative list
            clean.extend(words_clean)
    return clean

def fit_density_histogram_plot(pred, truth):
    return 0

def fit_regression_plot(pred, truth):
    return 0

def h_box_whisker_plot(pred, truth):
    return 0

def horizontal_bar_chart(pred, truth):
    return 0

def line_chart(pred, truth):
    return 0

def normalized_stacked_bar_chart(pred, truth):
    return 0

def pie_chart(pred, truth):
    return 0

def stacked_bar_chart(pred, truth):
    return 0

def unfit_density_histogram_plot(pred, truth):
    return 0

def unfit_regression_plot(pred, truth):
    return 0

def v_box_whisker_plot(pred, truth):
    return 0

def vertical_bar_chart(pred, truth):

    # add labels from data to truth.labels
    truth.labels = truth.labels + truth.data.iloc[:, 0].values.tolist()
    #preprocess
    truth.labels = clean_labels(truth.labels)

    # calculate percent of labels extracted
    labels_metric = len(list(set(truth.labels) & set(pred.labels))) / len(set(truth.labels))

    # calculate the heights of the extracted bars
    rects = list(filter(lambda contour: contour["n_sides"] == 4, pred.glyphs.large))
    pred_heights = np.array(list(map(lambda rect: cv2.boundingRect(rect["contour"])[3], rects)))
    
    
    # normalize truth heights
    truth_heights = truth.data.iloc[:, 1].values
    truth_heights = (truth_heights - np.min(truth_heights)) / (np.max(truth_heights) - np.min(truth_heights))

    # normalize pred heights
    pred_heights = (pred_heights - np.min(pred_heights)) / (np.max(pred_heights) - np.min(pred_heights))

    fig, ax = plt.subplots(1,1, figsize=((10,10)))
    x = range(0, max([len(truth_heights), len(pred_heights)]))
    
    ax.scatter(x[:len(truth_heights)], truth_heights, color="blue", label="truth")
    ax.scatter(x[:len(pred_heights)], pred_heights, color="red", label="pred")
    plt.show()

    return {
        "labels": labels_metric,
        "glyphs": 0

    }


def eval(pred, truth, chart_type):
    chart_type_evals = {
        "fit-density-histogram-plot": fit_density_histogram_plot,
        "fit-regression-plot": fit_regression_plot,
        "h-box-whisker-plot": h_box_whisker_plot,
        "horizontal-bar-chart": horizontal_bar_chart,
        "line-chart": line_chart,
        "normalized-stacked-bar-chart": normalized_stacked_bar_chart,
        "pie-chart": pie_chart,
        "stacked-bar-chart": stacked_bar_chart,
        "unfit-density-histogram-plot": unfit_density_histogram_plot,
        "unfit-regression-plot": unfit_regression_plot,
        "v-box-whisker-plot": v_box_whisker_plot,
        "vertical-bar-chart": vertical_bar_chart
    }

    # Format truth.labels into clean, tokenized list (general for all chart types)
    truth.labels = clean_labels(truth.labels.values())
    
    # Format pred.labels into clean, tokenized list (general for all chart types)
    pred.labels = clean_labels(pred.labels.text)

    return chart_type_evals[chart_type](pred, truth)


if __name__ == "__main__":
    import os, sys, glob, random
    import numpy as np
    from pathlib import Path
    import pickle
    sys.path.append(
        os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
    )

    from pipeline import pipeline


    CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "raw") # I apologize
    CHART_TYPE = "vertical-bar-chart"
    chart_folder = os.path.join(CHARTS_DIR, CHART_TYPE)
    N = 1

    for i in range(N):
        
        # chart_fp = glob.glob(os.path.join(chart_folder, '*.pkl'))[i]
        chart_fp = random.choice(glob.glob(os.path.join(chart_folder, '*.pkl')))

        with open(chart_fp, 'rb') as f:
            truth = pickle.load(f)
            pred = pipeline(chart_fp, VISUALIZE=False)
            
            evaluation = eval(pred, truth, CHART_TYPE)

            print("Labels:", evaluation["labels"])
            print("Glyphs:", evaluation["glyphs"])