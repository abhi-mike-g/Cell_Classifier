from skimage.measure import regionprops, label
import json

label_mask = label(binary_mask)  # binary mask of segmented cells
cells = []

for region in regionprops(label_mask, intensity_image=image):
    cell = {
        "id": region.label,
        "centroid": region.centroid,
        "area": region.area,
        "perimeter": region.perimeter,
        "bounding_box": region.bbox,
        "eccentricity": region.eccentricity,
        "mean_intensity": region.mean_intensity
    }
    cells.append(cell)

metadata = {"image_name": "example.tiff", "cells": cells}
with open("example.json", "w") as f:
    json.dump(metadata, f, indent=4)
