import cv2
import numpy as np

font = (cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)


def set_contrast(img, contrast):

    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))

    Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
    Gamma = 127 * (1 - Alpha)

    cal = cv2.addWeighted(img, Alpha, img, 0, Gamma)
    return cal    


def polygons(im):

    # reading image
    img = np.array(im)
    img = cv2.resize(img, (1028,1028))

    # blur to hopefully eliminate text as identified contours
    blurred = cv2.GaussianBlur(img, (15, 15), 0)

    # apply contrast. Seemed to help with ignoring the grid.
    contrasted = set_contrast(blurred, 400)

    # edge detection
    edges = cv2.Canny(contrasted, 100, 200)

    # find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # list for storing names of shapes. Skip first contour, as it represents the entire image.
    for contour in contours[1:]:
        
        x, y, w, h = cv2.boundingRect(contour)

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)

        # finding center point of shape
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])

        # putting shape name at center of each shape
        if len(approx) == 3:
            cv2.putText(img, 'Triangle', (x, y), *font)

        elif len(approx) == 4:

            # skip large quads (chart border)
            if (w > 750 and h > 750):
                continue

            cv2.putText(img, 'Quadrilateral', (x, y), *font)
        
        else:

            # eliminate small, complex polygons, which are probably text
            if (w<100 and h<100):
                continue

            cv2.putText(img, 'polygon', (x, y), *font)

            

        # using drawContours() function
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)

    # displaying the image after drawing contours
    img = cv2.resize(img, (500, 500))
    cv2.imshow('shapes', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
