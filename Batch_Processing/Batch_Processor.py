# Script for Batch Processing

import os
import tifffile as tiff
from cellpose import models
from skimage.measure import regionprops
import json
import numpy as np

# Initialize the Cellpose model
model = models.Cellpose(model_type='cyto', gpu=False)  # Set gpu=True if you have a CUDA-enabled device

def process_image(image_path):
    """
    Process a single image with Cellpose and extract metadata.
    """
    # Load image
    image = tiff.imread(image_path)
    
    # If the image is RGB (3 channels), convert to grayscale
    if image.ndim == 3 and image.shape[2] == 3:
        image = image.mean(axis=2)  # Convert to grayscale by averaging the channels

    # Run Cellpose segmentation
    masks, _, _, _ = model.eval(image, diameter=None, channels=[0, 0])

    # Extract per-cell metadata using regionprops
    cells = []
    for region in regionprops(masks, intensity_image=image):
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

def save_metadata(image_name, cells, save_path):
    """
    Save the extracted metadata as a JSON file.
    """
    metadata = {"image_name": image_name, "cells": cells}
    with open(save_path, "w") as f:
        json.dump(metadata, f, indent=4)

def batch_process_images(input_folder, output_folder):
    """
    Process all .tiff images in the input folder, segment them, and save metadata.
    """
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop over all .tiff images in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".tiff"):
            image_path = os.path.join(input_folder, filename)
            
            # Process the image
            cells = process_image(image_path)

            # Save the metadata to JSON
            json_filename = os.path.splitext(filename)[0] + ".json"
            json_path = os.path.join(output_folder, json_filename)
            save_metadata(filename, cells, json_path)

            print(f"Processed {filename} - {len(cells)} cells detected.")

# Define input and output folders
input_folder = "path/to/your/tiff/images"  # Change to your folder containing .tiff images
output_folder = "path/to/output/json"      # Change to your desired output folder

# Run batch processing
batch_process_images(input_folder, output_folder)
