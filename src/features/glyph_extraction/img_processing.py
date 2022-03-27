import cv2

def set_contrast(img, contrast):

    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))

    Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
    Gamma = 127 * (1 - Alpha)

    cal = cv2.addWeighted(img, Alpha, img, 0, Gamma)
    return cal  