from PIL.Image import Image
from PIL import Image
import pickle
from pathlib import Path
import numpy as np
import os
import glob
import random
import sys
import cv2
sys.path.append(
    os.path.join(Path(os.path.abspath(__file__)).parent.parent, 'gen')
)

from polygons import polygons
from ocr import get_text_bbs


if __name__ == '__main__':

    CHARTS_DIR = os.path.join(Path(os.path.abspath(__file__)).parent.parent.parent.parent, "volume", "raw") # I apologize
    font = (cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    n = 10
    

    for _ in range(n):

        chart_folder = os.path.join(CHARTS_DIR, "horizontal-bar-chart")
        chart_fp = random.choice(glob.glob(os.path.join(chart_folder, '*.pkl')))

        # try:
        with open(chart_fp, 'rb') as f:

            # load
            chart = pickle.load(f)
            im = Image.open(chart.img)
            im = np.array(im)

            # get glyphs
            polys = polygons(im)

            # get labels
            text_bbs = get_text_bbs(im)

            # draw label bbs
            for bb in text_bbs:
                im = cv2.rectangle(im, bb[0], bb[1], (0, 255, 0), 2)

            # draw polys
            for poly in polys:
                # finding center point of shape
                M = cv2.moments(poly["contour"])
                if M['m00'] != 0.0:
                    x = int(M['m10']/M['m00'])
                    y = int(M['m01']/M['m00'])
                    cv2.putText(im, poly["shape"], (x, y), *font)
                cv2.drawContours(im, [poly["contour"]], 0, (0, 0, 255), 5)


            # show result
            # print(chart.labels)
            # print(chart.data)
            cv2.imshow('Glyphs and labels', cv2.resize(im, (500,500)))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # except FileNotFoundError:
        #     print("Error opening file")
        #     continue