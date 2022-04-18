from PIL.Image import Image
from PIL import Image
import pickle
import numpy as np
import cv2
from types import SimpleNamespace


from large_glyph import extract_large_glyphs
from small_glyph import extract_small_glyphs
from ocr import get_labels



FONT = (cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 2)

# https://stackoverflow.com/questions/16279212/how-to-use-dot-notation-for-dict-in-python
class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)

def pipeline(
    chart_fp,
    
    VISUALIZE = True,
    test=False
    ):
    """
    To get the sets defined in the flowchart:

    Gl = output.glyphs.large

    Gs = output.glyphs.small

    G = [*output.glyphs.large, *output.glyphs.small]
    
    L = output.labels                                      (This is a dataframe)
    """

    try:
        with open(chart_fp, 'rb') as f:

            # load
            if test:
                im = Image.open(chart_fp).convert("RGB")
            else:
                chart = pickle.load(f)
                im = Image.open(chart.img).convert("RGB")
            im = np.array(im)

            # get labels
            labels = get_labels(im, psm=2)

            # get glyphs
            large_glyphs = extract_large_glyphs(im, label_mask=labels)
            small_glyphs_and_labels = extract_small_glyphs(im, label_mask=labels)
            small_glyphs = small_glyphs_and_labels["glyphs"]

            # add round 2 labels
            labels.append(small_glyphs_and_labels["labels"], ignore_index=True)
            
            if VISUALIZE:

                # draw label bounding boxes in green
                for _, label in labels.iterrows():

                    # get text and bounding box of label
                    text = label.text
                    bb = label[["p1", "p2"]]

                    # get center of bounding box
                    # center = (bb.p1[0] + bb.p2[0]) / 2, (bb.p1[1] + bb.p2[1]) / 2

                    # draw bounding box
                    im = cv2.rectangle(im, bb.p1, bb.p2, (0, 255, 0), 2)

                # draw large glyphs in blue
                for large_glyph in large_glyphs:

                    contour = large_glyph["contour"]

                    # finding center point of contour and put label of shape
                    M = cv2.moments(contour)
                    if M['m00'] != 0.0:
                        x = int(M['m10']/M['m00'])
                        y = int(M['m01']/M['m00'])
                        cv2.putText(im, large_glyph["shape"], (x, y), *FONT)
                    
                    # draw contour of glyph
                    cv2.drawContours(im, [contour], 0, (0, 0, 255), 5)
                
                for small_glyph in small_glyphs:

                    contour = small_glyph["contour"]

                    # finding center point of contour and put label of shape
                    M = cv2.moments(contour)
                    if M['m00'] != 0.0:
                        x = int(M['m10']/M['m00'])
                        y = int(M['m01']/M['m00'])
                        cv2.putText(im, small_glyph["shape"], (x, y), *FONT)
                    
                    # draw contour of glyph
                    cv2.drawContours(im, [contour], 0, (255, 0, 0), 5)

                # show result
                # print(chart.labels)
                # print(chart.data)
                cv2.imshow('Glyphs and labels', cv2.resize(im, (600,600)))
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            # return labels and glyphs
            return NestedNamespace({
                "labels": labels,
                "glyphs": {
                    "large": large_glyphs,
                    "small": small_glyphs
                }
            })
            

    except FileNotFoundError:
        print(f"Error opening {chart_fp}")