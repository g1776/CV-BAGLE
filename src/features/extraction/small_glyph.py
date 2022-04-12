import cv2
from img_processing import set_contrast

def process(im):
    # blur to hopefully eliminate text as identified contours
    blurred = cv2.GaussianBlur(im, (15, 15), 0)

    # apply contrast. Seemed to help with ignoring the grid.
    contrasted = set_contrast(blurred, 400)

    # edge detection
    edges = cv2.Canny(contrasted, 100, 200)

    return edges

def extract_small_glyphs(im, show_processed=False):
    processed = process(im)

    if show_processed:
        cv2.imshow('BBs processed', cv2.resize(processed, (500,500)))

    #find contours 
    contours, _ = cv2.findContours(processed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sm_glyph = []
    for contour in contours[1:]:

        x, y, w, h = cv2.boundingRect(contour)
        approx = cv2.approxPlyDP(contour, .01*cv2.arcLength(contour, True), True)
        

    ##for small shapes, calculate area based on sizes less than 100 (traingel, square)
    ##tick marks for axis??????
    ##implement text detction???
    ##componenets of scatteract can be added??? xxxxx
    