# RBC Segmentation Debug Script

import os
from tifffile import imread
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
from skimage.measure import regionprops, label
from cellpose import models
import json

# -----------------------------
# CONFIGURATION
# -----------------------------
debug_images = ['raw_images/sample1.tiff', 'raw_images/sample2.tiff']  # Add 1-2 test images
model_type = 'cyto'
use_gpu = True
diameter = None         # None = automatic
flow_threshold = 0.4
min_size = 50           # Remove tiny objects

# -----------------------------
# INITIALIZE MODEL
# -----------------------------
model = models.Cellpose(gpu=use_gpu, model_type=model_type)

# -----------------------------
# DEBUG LOOP
# -----------------------------
for filepath in debug_images:
    if not os.path.exists(filepath):
        print(f"File {filepath} not found, skipping.")
        continue

    print(f"Processing {os.path.basename(filepath)}...")

    # Load image
    img = imread(filepath)

    # Preprocessing
    img_norm = (img - np.min(img)) / (np.max(img) - np.min(img))
    img_eq = exposure.equalize_adapthist(img_norm)

    # Run Cellpose
    masks, flows, styles, diams = model.eval(img_eq,
                                            diameter=diameter,
                                            flow_threshold=flow_threshold,
                                            channels=[0,0])  # grayscale

    # Filter small objects
    labeled_masks = label(masks)
    props = regionprops(labeled_masks)
    filtered_masks = np.zeros_like(masks)
    cell_metadata = []

    for p in props:
        if p.area >= min_size:
            filtered_masks[labeled_masks == p.label] = p.label
            cell_metadata.append({
                'centroid': p.centroid,
                'area': p.area,
                'eccentricity': p.eccentricity,
                'bbox': p.bbox
            })

    # -----------------------------
    # DEBUG OUTPUT
    # -----------------------------
    print(f"Total cells detected: {len(cell_metadata)}")
    if len(cell_metadata) > 0:
        print("Example metadata for first cell:", cell_metadata[0])

    # Quick visual QC
    plt.figure(figsize=(5,5))
    plt.imshow(img_eq, cmap='gray')
    plt.imshow(filtered_masks, alpha=0.5)
    plt.title(f"{os.path.basename(filepath)} - Cells: {len(cell_metadata)}")
    plt.show()
    plt.close()

    # Optional: save JSON for test
    json_filename = filepath.replace('.tiff', '_debug.json')
    with open(json_filename, 'w') as f:
        json.dump(cell_metadata, f)

print("Debug run complete!")
