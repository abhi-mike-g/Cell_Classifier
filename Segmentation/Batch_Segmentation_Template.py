# RBC Segmentation Batch Script Template

import os
from tifffile import imread, imsave
import numpy as np
import matplotlib.pyplot as plt
from skimage import exposure
from skimage.measure import regionprops, label
from cellpose import models
import json

# -----------------------------
# CONFIGURATION
# -----------------------------
input_folder = 'raw_images/'       # Folder with .tiff images
output_json_folder = 'metadata/'   # Folder to save JSON metadata
output_mask_folder = 'masks/'      # Optional: save mask overlays

# Cellpose parameters
model_type = 'cyto'
use_gpu = True
diameter = None           # None = automatic
flow_threshold = 0.4
min_size = 50             # Remove tiny objects

# -----------------------------
# SETUP
# -----------------------------
os.makedirs(output_json_folder, exist_ok=True)
os.makedirs(output_mask_folder, exist_ok=True)

# Initialize Cellpose model
model = models.Cellpose(gpu=use_gpu, model_type=model_type)

# -----------------------------
# PROCESSING LOOP
# -----------------------------
for filename in os.listdir(input_folder):
    if not filename.endswith('.tiff'):
        continue

    filepath = os.path.join(input_folder, filename)
    print(f"Processing {filename}...")

    # Load image
    img = imread(filepath)

    # -----------------------------
    # PREPROCESSING (optional)
    # -----------------------------
    # Normalize image to 0-1
    img_norm = (img - np.min(img)) / (np.max(img) - np.min(img))
    
    # Optional: enhance contrast
    img_eq = exposure.equalize_adapthist(img_norm)

    # -----------------------------
    # SEGMENTATION
    # -----------------------------
    masks, flows, styles, diams = model.eval(img_eq,
                                            diameter=diameter,
                                            flow_threshold=flow_threshold,
                                            channels=[0,0])  # grayscale

    # Remove small objects
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
    # SAVE RESULTS
    # -----------------------------
    # Save JSON metadata
    json_filename = os.path.join(output_json_folder, filename.replace('.tiff', '.json'))
    with open(json_filename, 'w') as f:
        json.dump(cell_metadata, f)

    # Optional: save mask overlay for QC
    mask_overlay = np.stack([img_eq]*3, axis=-1)  # Convert to RGB
    mask_overlay[filtered_masks>0] = [1,0,0]      # Red overlay
    mask_filename = os.path.join(output_mask_folder, filename.replace('.tiff', '_mask.tiff'))
    imsave(mask_filename, (mask_overlay*255).astype(np.uint8))

    # Optional: quick QC plot
    plt.figure(figsize=(5,5))
    plt.imshow(img_eq, cmap='gray')
    plt.imshow(filtered_masks, alpha=0.5)
    plt.title(f'{filename} - Cells: {len(cell_metadata)}')
    plt.show()
    plt.close()

print("Batch processing complete!")
