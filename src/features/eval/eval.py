from bar import bar_chart
from scatter import scatter_chart
from pie import pie_chart
from histogram import histogram_chart
from box import box_whisker
from stacked_bar import stacked_bar_chart

from helpers import clean_labels

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def eval(pred, truth, chart_type):
    chart_type_evals = {
        "fit-density-histogram-plot": histogram_chart,
        "fit-regression-plot": scatter_chart,
        "h-box-whisker-chart": lambda pred, truth: box_whisker(pred, truth, 'h'),
        "horizontal-bar-chart": lambda pred, truth: box_whisker(pred, truth, 'h'),
        "line-chart": lambda pred, truth: scatter_chart(pred, truth, is_line_chart=True),
        "normalized-stacked-bar-chart": stacked_bar_chart,
        "pie-chart": pie_chart,
        "stacked-bar-chart": stacked_bar_chart,
        "unfit-density-histogram-plot": histogram_chart,
        "unfit-regression-plot": scatter_chart,
        "v-box-whisker-chart": lambda pred, truth: bar_chart(pred, truth, 'v'),
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
    CHART_TYPE = "stacked-bar-chart"
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