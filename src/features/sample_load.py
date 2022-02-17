from utils import ChartGenerator
from PIL import Image
import pickle
import os

my_fp = os.path.join(ChartGenerator.CHARTS_DIR, "horizontal-bar-chart",  "horizontal-bar-chart-0.pkl")

with open(my_fp, 'rb') as f:

    # load
    chart = pickle.load(f)
    im = Image.open(chart.img)

    # display output
    print(chart.labels)
    print(chart.data)
    im.show()
