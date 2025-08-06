# Post-Processing for instance segmentation

import cv2
from skimage.measure import label, regionprops
from skimage.segmentation import watershed
from scipy import ndimage
import json
import numpy as np

def extract_cells(mask, original_image, min_area=50):
    """
    mask: binary mask from U-Net (0-1)
    original_image: raw tiff image
    """
    mask = (mask > 0.5).astype(np.uint8)

    # Remove small noise
    num_labels, labels_im = cv2.connectedComponents(mask)

    # Distance transform for watershed
    distance = ndimage.distance_transform_edt(mask)
    local_maxi = cv2.dilate(distance, np.ones((3,3)))  # simple local maxima
    markers = label(local_maxi)
    labels = watershed(-distance, markers, mask=mask)

    cells = []
    for region in regionprops(labels, intensity_image=original_image):
        if region.area < min_area:
            continue
        cell = {
            "id": int(region.label),
            "centroid": [float(region.centroid[0]), float(region.centroid[1])],
            "area": float(region.area),
            "perimeter": float(region.perimeter),
            "eccentricity": float(region.eccentricity),
            "bounding_box": [int(x) for x in region.bbox],
            "mean_intensity": float(region.mean_intensity)
        }
        cells.append(cell)
    return cells
