# Dataset Loader for .tiff Bitmap images

import torch
from torch.utils.data import Dataset, DataLoader
import tifffile as tiff
import albumentations as A
import numpy as np

class RBCDataset(Dataset):
    def __init__(self, image_paths, mask_paths=None, transforms=None):
        self.image_paths = image_paths
        self.mask_paths = mask_paths
        self.transforms = transforms

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image = tiff.imread(self.image_paths[idx])
        image = image.astype(np.float32)
        image = (image - image.min()) / (image.max() - image.min())  # normalize to 0-1

        mask = None
        if self.mask_paths:
            mask = tiff.imread(self.mask_paths[idx]).astype(np.uint8)
        
        if self.transforms:
            augmented = self.transforms(image=image, mask=mask)
            image = augmented['image']
            if mask is not None:
                mask = augmented['mask']
        
        image = torch.tensor(image).unsqueeze(0)  # add channel dimension
        if mask is not None:
            mask = torch.tensor(mask).unsqueeze(0)
        
        return image, mask
