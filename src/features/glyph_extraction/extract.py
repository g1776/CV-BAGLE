from PIL.Image import Image
from PIL import Image
import pickle
from pathlib import Path
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
    

    my_fp = os.path.join(CHARTS_DIR, "horizontal-bar-chart",  "horizontal-bar-chart-0.pkl")

    with open(my_fp, 'rb') as f:

        # load
        chart = pickle.load(f)
        im = Image.open(chart.img)

        polygons(im)

        # # display output
        # print(chart.labels)
        # print(chart.data)
        # im.show()