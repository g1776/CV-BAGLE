from utils import ChartGenerator
import glob
import os



for chart_class_fp in glob.glob(os.path.join(ChartGenerator.CHARTS_DIR, '*')):
    chart_class = os.path.basename(chart_class_fp)

    num_files = len(glob.glob(os.path.join(chart_class_fp, '*')))

    print(chart_class, num_files)
