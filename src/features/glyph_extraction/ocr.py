import pytesseract
import cv2
import numpy as np
import matplotlib.pyplot as plt
from img_processing import set_contrast

# config
TESSERACT_DIR = r"C:\Users\grego\Documents\GitHub\DataVizCaptionGeneration\download\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_DIR


def preprocess(im):

    im = set_contrast(im, 300)

    # convert to grayscale
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # threshold the image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh2 = thresh.copy()


    # calculate mask by keeping contours of a certain size
    # This essentially removes large glyphs so they are not mistaken as text
    # https://stackoverflow.com/questions/10262600/how-to-detect-region-of-large-of-white-pixels-using-opencv
    mask = np.zeros(thresh.shape,np.uint8)
    contours, _ = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) > 10000:
            cv2.drawContours(mask,[cnt],0,255,-1)
    plt.imshow(mask, cmap='gray', vmin=0, vmax=255)
    plt.show()
    
    
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


def get_text_bbs(im):

    im = preprocess(im)
    cv2.imshow('processed', cv2.resize(im, (500,500)))

    # get image the dimensions
    h, w, _ = im.shape # assumes color image

    # run tesseract, returning the bounding boxes
    boxes = pytesseract.image_to_boxes(im, config="box --psm 2")
    # draw the bounding boxes on the image
    pts = []
    for b in boxes.splitlines():
        b = b.split(' ')
        p1 = (int(b[1]), h - int(b[2]))
        p2 = (int(b[3]), h - int(b[4]))
        pts.append((p1,p2))

    return pts
