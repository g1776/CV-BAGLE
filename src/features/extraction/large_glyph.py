import cv2
from img_processing import set_contrast
import numpy as np


def process(im):
    # blur to hopefully eliminate text as identified contours
    blurred = cv2.GaussianBlur(im, (15, 15), 0)

    # apply contrast. Seemed to help with ignoring the grid.
    contrasted = set_contrast(blurred, 400)

    # edge detection
    edges = cv2.Canny(contrasted, 100, 200)

    return edges


def extract_large_glyphs(im, label_mask, show_processed=False):

    processed = process(im)


    # apply label mask
    mask = np.ones(processed.shape, dtype=np.uint8) * 255
    for _, row in label_mask.iterrows():
        mask = cv2.rectangle(mask, row["p1"], row["p2"], 0, -1)
    processed = cv2.bitwise_and(processed, processed, mask=mask)

    # optionally show processed image
    if show_processed:
        cv2.imshow('BBs processed', cv2.resize(processed, (500,500)))
    

    # find contours
    contours, _ = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    
    # list for storing names of shapes. Skip first contour, as it represents the entire image.
    polygons = []
    for contour in contours[1:]:
        
        x, y, w, h = cv2.boundingRect(contour)

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        
        n_sides = len(approx)
        
        shape = ""

        # eliminate small polygons which are probably text
        if (w<100 or h<100):
            continue

        if n_sides == 3:
            shape = "triangle"

        elif n_sides == 4:
            shape = "quadrilateral"

            # skip large quads (chart border)
            if (w > 750 and h > 750):
                continue

        else:
            shape = "polygon"

            
        
        polygons.append({"contour": contour, "shape": shape, "n_sides": n_sides})

    return polygons
