def save_metadata(image_name, cells, save_path):
    metadata = {"image_name": image_name, "cells": cells}
    with open(save_path, "w") as f:
        json.dump(metadata, f, indent=4)

save_metadata("example.tiff", cells, "example_cellpose.json")
print(f"Extracted {len(cells)} cells from {image_path}")
