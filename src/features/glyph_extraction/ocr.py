import pytesseract
import cv2
import numpy as np
from img_processing import set_contrast

# config
TESSERACT_DIR = r"C:\Users\grego\Documents\GitHub\DataVizCaptionGeneration\download\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_DIR



def preprocess(im):

    im = set_contrast(im, 300)

    # convert to grayscale
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # threshold the image
    thresh = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = cv2.bitwise_not(thresh)
    thresh2 = thresh.copy()


    # calculate mask by keeping contours of a certain size
    # This essentially removes large glyphs so they are not mistaken as text
    # https://stackoverflow.com/questions/10262600/how-to-detect-region-of-large-of-white-pixels-using-opencv
    mask = np.zeros(thresh.shape,np.uint8)
    contours, _ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(cnt) for cnt in contours]

    avgArea = np.mean(areas)

    for cnt in contours:
        if avgArea < cv2.contourArea(cnt):
            cv2.drawContours(mask,[cnt],0,255,-1)
    
    # apply mask
    masked = cv2.bitwise_not(thresh2,thresh2,mask)

    no_lines = masked.copy()

    # Remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
    remove_horizontal = cv2.morphologyEx(masked, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(no_lines, [c], -1, (0,0,0), 5)

    # Remove vertical lines
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
    remove_vertical = cv2.morphologyEx(masked, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(no_lines, [c], -1, (0,0,0), 5)

    # convert back to rgba
    no_lines  = cv2.cvtColor(no_lines,cv2.COLOR_GRAY2RGBA)
    
    return no_lines


def get_text_bbs(im, psm, show_processed=False):


    # preprocess
    processed = preprocess(im)

    # optionally show processed image
    if show_processed:
        cv2.imshow('BBs processed', cv2.resize(processed, (500,500)))

    # get image dimensions
    h, w, _ = processed.shape # assumes color image

    # run tesseract, returning the bounding boxes
    boxes = pytesseract.image_to_boxes(processed, config=f"box --psm {psm}")

    # draw the bounding boxes on the image
    pts = []
    for b in boxes.splitlines():
        b = b.split(' ')
        p1 = (int(b[1]), h - int(b[2]))
        p2 = (int(b[3]), h - int(b[4]))

        # ignore bounding boxes that are > 60% of image dimensions
        bw = abs(p1[0] - p2[0])
        bh = abs(p1[1] - p2[1])
        if bw > .6*w or bh > .6*h:
            continue
        
        pts.append((p1,p2))

    return pts
