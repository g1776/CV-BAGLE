from multiprocessing import Pool
import os, sys, glob
from pathlib import Path
import pickle

sys.path.extend([
    os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'extraction'),
    os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
    ]
)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from bar import bar_chart
from scatter import scatter_chart
from pie import pie_chart
from histogram import histogram_chart
from box import box_whisker
from stacked_bar import stacked_bar_chart
from pipeline import pipeline

from helpers import clean_labels

# GLOBALS
CHART_TYPE = "unfit-regression-plot"
CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "raw") # I apologize
chart_folder = os.path.join(CHARTS_DIR, CHART_TYPE)
OUT_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "processed")
OUT_FILE = os.path.join(OUT_DIR, f"eval_{CHART_TYPE}.pkl")

chart_fps = glob.glob(os.path.join(chart_folder, '*.pkl'))

chart_type_evals = {
        "fit-density-histogram-plot": histogram_chart,
        "fit-regression-plot": scatter_chart,
        "h-box-whisker-chart": lambda pred, truth: box_whisker(pred, truth, 'h'),
        "horizontal-bar-chart": lambda pred, truth: bar_chart(pred, truth, 'h'),
        "line-chart": lambda pred, truth: scatter_chart(pred, truth, is_line_chart=True),
        "normalized-stacked-bar-chart": stacked_bar_chart,
        "pie-chart": pie_chart,
        "stacked-bar-chart": stacked_bar_chart,
        "unfit-density-histogram-plot": histogram_chart,
        "unfit-regression-plot": scatter_chart,
        "v-box-whisker-chart": lambda pred, truth: box_whisker(pred, truth, 'v'),
        "vertical-bar-chart": lambda pred, truth: bar_chart(pred, truth, 'v')
    }


def eval(pred, truth, chart_type):

    # Format truth.labels into clean, tokenized list (general for all chart types)
    truth.labels = clean_labels(truth.labels.values())
    
    # Format pred.labels into clean, tokenized list (general for all chart types)
    pred.labels = clean_labels(pred.labels.text)

    return chart_type_evals[chart_type](pred, truth)


def eval_chart(chart_fp):
    print("Evaluating chart:", chart_fp)

    with open(chart_fp, 'rb') as f:
        truth = pickle.load(f)
        pred = pipeline(chart_fp, VISUALIZE=False)
        
        evaluation = eval(pred, truth, CHART_TYPE)
    
    eval_list = evaluation.to_list()
    for metric in eval_list:
        metric["chart_fp"] = chart_fp

    return eval_list
            

if __name__ == "__main__":

    
    df_list = []
    

    with Pool(processes=10) as p:
        out = p.imap(eval_chart, chart_fps)
        
        for row in out:
            for dp in row:
                df_list.append(dp)

    pickle.dump(df_list, open(OUT_FILE, 'wb'))

    print(f"\nWrote {len(df_list)} rows to {OUT_FILE}")