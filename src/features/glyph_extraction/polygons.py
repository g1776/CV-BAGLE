import cv2
import numpy as np
from img_processing import set_contrast


def polygons(im):

    # blur to hopefully eliminate text as identified contours
    blurred = cv2.GaussianBlur(im, (15, 15), 0)

    # apply contrast. Seemed to help with ignoring the grid.
    contrasted = set_contrast(blurred, 400)

    # edge detection
    edges = cv2.Canny(contrasted, 100, 200)

    # find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
    # list for storing names of shapes. Skip first contour, as it represents the entire image.
    polygons = []
    for contour in contours[1:]:
        
        x, y, w, h = cv2.boundingRect(contour)

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        
        n_sides = len(approx)
        
        shape = ""

        if n_sides == 3:
            shape = "triangle"

        elif n_sides == 4:
            shape = "quadrilateral"

            # skip large quads (chart border)
            if (w > 750 and h > 750):
                continue

        else:
            shape = "polygon"

            # eliminate small, complex polygons, which are probably text
            if (w<100 and h<100):
                continue
        
        polygons.append({"contour": contour, "shape": shape})

    return polygons