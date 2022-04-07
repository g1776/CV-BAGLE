import cv2
import numpy as np

def calc_glyph_features(G: list[dict]):
        
    
    # glyph size
    sizes = [cv2.contourArea(g['contour']) for g in G]
    sizes_mean = np.mean(sizes)
    sizes_std = np.std(sizes)

    # glyph position
    centers = []
    for g in G:
        M = cv2.moments(g['contour'])
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
            centers.append({'x': x, 'y': y})
    std_center_x = np.std([c['x'] for c in centers])
    std_centers_y = np.std([c['y'] for c in centers])

    # glyph shape (num sides)
    num_sides = [g['n_sides'] for g in G]
    num_sides_mean = np.mean(num_sides)
    num_sides_std = np.std(num_sides)

    # glyph edge distance
    # mean
    # std

    # glyph aspect ratio
    aspect_ratios = []
    for g in G:
        x,y,w,h = cv2.boundingRect(g["contour"])
        aspect_ratios.append(w/h)
    aspect_ratios_mean = np.mean(aspect_ratios)
    aspect_ratios_std = np.std(aspect_ratios)

    # num glyphs
    num_glyphs = len(G)

    return np.array([
        sizes_mean, 
        sizes_std,
        std_center_x, 
        std_centers_y,
        num_sides_mean, 
        num_sides_std,
        aspect_ratios_mean, 
        aspect_ratios_std,
        num_glyphs
    ])

def calc_label_features(L):
    num_labels = []
    for _, l in L.iterrows():
        clean = l.text.replace('-', '').replace('%', '')
        if clean.isnumeric():
            num_labels.append({'x': l.left + l.width/2, 'y': l.top + l.height/2})

    num_labels_x_mean = np.mean([l['x'] for l in num_labels])
    num_labels_y_mean = np.mean([l['y'] for l in num_labels])
    num_labels_x_std = np.std([l['x'] for l in num_labels])
    num_labels_y_std = np.std([l['y'] for l in num_labels])


    
    return [
        num_labels_x_mean,
        num_labels_y_mean,
        num_labels_x_std,
        num_labels_y_std
    ]
