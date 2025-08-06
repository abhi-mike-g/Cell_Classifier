# Segmenting RBCs with Cellpose

from cellpose import models, io
import tifffile as tiff
import numpy as np
from skimage.measure import regionprops, label
import json

# Load Cellpose model (cyto for circular cells, nucleus for small round cells)
model = models.Cellpose(model_type='cyto', gpu=False)  # set gpu=True if you have CUDA

# Load image
image_path = "example.tiff"
image = tiff.imread(image_path)

# If image is grayscale (label-free), ensure shape is (H, W)
if image.ndim == 3 and image.shape[2] == 3:
    image = image.mean(axis=2)  # convert to grayscale

# Run Cellpose segmentation
masks, flows, styles, diams = model.eval(image, diameter=None, channels=[0,0])
