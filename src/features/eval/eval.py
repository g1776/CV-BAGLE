from bar import bar_chart
from scatter import scatter_chart
from pie import pie_chart
from helpers import clean_labels

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# 1
def unfit_density_histogram_plot(pred, truth):
    return 0

def fit_density_histogram_plot(pred, truth):
    return 0


# 2
def line_chart(pred, truth):
    return 0


# 4
def normalized_stacked_bar_chart(pred, truth):
    return 0

def stacked_bar_chart(pred, truth):
    return 0


# 5
def v_box_whisker_plot(pred, truth):
    return 0

def h_box_whisker_plot(pred, truth):
    return 0



def eval(pred, truth, chart_type):
    chart_type_evals = {
        "fit-density-histogram-plot": fit_density_histogram_plot,
        "fit-regression-plot": lambda pred, truth: scatter_chart(pred, truth),
        "h-box-whisker-plot": h_box_whisker_plot,
        "horizontal-bar-chart": lambda pred, truth: bar_chart(pred, truth, 'h'),
        "line-chart": line_chart,
        "normalized-stacked-bar-chart": normalized_stacked_bar_chart,
        "pie-chart": pie_chart,
        "stacked-bar-chart": stacked_bar_chart,
        "unfit-density-histogram-plot": unfit_density_histogram_plot,
        "unfit-regression-plot": lambda pred, truth: scatter_chart(pred, truth),
        "v-box-whisker-plot": v_box_whisker_plot,
        "vertical-bar-chart": lambda pred, truth: bar_chart(pred, truth, 'v')
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
    sys.path.extend([
        os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'extraction'),
        os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
        ]
    )
    

    from pipeline import pipeline


    CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "raw") # I apologize
    CHART_TYPE = "pie-chart"
    chart_folder = os.path.join(CHARTS_DIR, CHART_TYPE)
    N = 1

    for i in range(N):
        
        # chart_fp = glob.glob(os.path.join(chart_folder, '*.pkl'))[i]
        chart_fp = random.choice(glob.glob(os.path.join(chart_folder, '*.pkl')))

        with open(chart_fp, 'rb') as f:
            truth = pickle.load(f)
            print("running pipeline...")
            pred = pipeline(chart_fp, VISUALIZE=True)
            
            print("evaluating...")
            evaluation = eval(pred, truth, CHART_TYPE)

            print(evaluation)