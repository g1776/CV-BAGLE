from PIL.Image import Image
from PIL import Image
import pickle
from pathlib import Path
import numpy as np
import os
import sys
sys.path.append(
    os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
)

from polygons import polygons


def extract(im: Image):
    '''Extract glyphs from image'''

    pass

if __name__ == '__main__':

    CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "raw") # I apologize
    
    chart_idxs = np.random.choice(1000, 10)

    for idx in chart_idxs:

        my_fp = os.path.join(CHARTS_DIR, "horizontal-bar-chart",  f"horizontal-bar-chart-{idx}.pkl")

        with open(my_fp, 'rb') as f:

            # load
            chart = pickle.load(f)
            im = Image.open(chart.img)

            polygons(im)

            # # display output
            # print(chart.labels)
            # print(chart.data)
            # im.show()