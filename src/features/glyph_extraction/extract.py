from cgitb import text
from ctypes.wintypes import RECT
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
    n = 3
    

    for _ in range(n):

        chart_folder = os.path.join(CHARTS_DIR, "vertical-bar-chart")
        chart_fp = random.choice(glob.glob(os.path.join(chart_folder, '*.pkl')))

        # try:
        with open(chart_fp, 'rb') as f:

            # load
            chart = pickle.load(f)
            im = Image.open(chart.img)
            im = np.array(im)

            # get labels
            text_bbs = get_text_bbs(im, psm=2)

            # get glyphs
            polys = polygons(im)
            

            # draw label bounding boxes in green
            for _, bb in text_bbs.iterrows():
                # average between 2 points
                avg_pt = (bb.p1[0] + bb.p2[0]) / 2, (bb.p1[1] + bb.p2[1]) / 2
                print(bb.text, avg_pt)
                im = cv2.rectangle(im, bb.p1, bb.p2, (0, 255, 0), 2)

            # draw polys
            for poly in polys:

                contour = poly["contour"]

                # finding center point of shape and draw labels
                M = cv2.moments(contour)
                if M['m00'] != 0.0:
                    x = int(M['m10']/M['m00'])
                    y = int(M['m01']/M['m00'])
                    cv2.putText(im, poly["shape"], (x, y), *font)
                
                # draw contour in red
                cv2.drawContours(im, [contour], 0, (0, 0, 255), 5)

            print('-----------------')

            # show result
            # print(chart.labels)
            # print(chart.data)
            cv2.imshow('Glyphs and labels', cv2.resize(im, (700,700)))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # except FileNotFoundError:
        #     print("Error opening file")
        #     continue