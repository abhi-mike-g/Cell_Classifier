def save_metadata(image_name, cells, save_path):
    metadata = {"image_name": image_name, "cells": cells}
    with open(save_path, "w") as f:
        json.dump(metadata, f, indent=4)
