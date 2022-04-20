import cv2
from img_processing import set_contrast
from ocr import get_labels
import numpy as np

def process(im):
    # blur to hopefully eliminate text as identified contours
    blurred = cv2.GaussianBlur(im, (15, 15), 0)

    # apply contrast. Seemed to help with ignoring the grid.
    contrasted = set_contrast(blurred, 400)

    # edge detection
    edges = cv2.Canny(contrasted, 100, 200)

    return edges

def extract_small_glyphs(im, label_mask, large_glyph_mask, show_processed=False, psm=2):
    """
    Extracts small glyphs from the image, along with more labels from the second round of OCR as part of preprocessing.
    
    Returns: dict of extracted glyphs and labels
    """

    processed = process(im)

    # apply label mask
    mask = np.ones(processed.shape, dtype=np.uint8) * 255
    for _, row in label_mask.iterrows():
        mask = cv2.rectangle(mask, row["p1"], row["p2"], 0, -1)
    processed = cv2.bitwise_and(processed, processed, mask=mask)

    # apply large glyph mask
    mask = np.zeros(processed.shape, dtype=np.uint8)
    for large_glyph in large_glyph_mask:
        cv2.drawContours(processed, [large_glyph["contour"]], 0, 255, -1)

    # run label extraction again and mask
    more_labels = get_labels(cv2.cvtColor(processed, cv2.COLOR_GRAY2RGBA), psm=psm, preprocess_im=False)
    mask = np.ones(processed.shape, dtype=np.uint8) * 255
    for _, row in more_labels.iterrows():
        mask = cv2.rectangle(mask, row["p1"], row["p2"], 0, -1)
    processed = cv2.bitwise_and(processed, processed, mask=mask)

    if show_processed:
        cv2.imshow('BBs processed', cv2.resize(processed, (500,500)))

    

    #find contours 
    contours, _ = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
    small_glyphs = []
    for contour in contours[1:]:

        x, y, w, h = cv2.boundingRect(contour)
        approx = cv2.approxPolyDP(contour, .01*cv2.arcLength(contour, True), True)
        
        n_sides = len(approx)

        # eliminate large polygons
        
        if w > 100 or h > 100:
            continue

        print(w, h)

        if n_sides == 3:
            shape = "triangle"

        elif n_sides == 4:
            shape = "quadrilateral"

            # skip large quads (chart border)
            if (w > 750 and h > 750):
                continue

        else:
            shape = "polygon"

        small_glyphs.append({"contour": contour, "shape": shape, "n_sides": n_sides})

    return {
        "glyphs": small_glyphs,
        "labels": more_labels
    }
    
    