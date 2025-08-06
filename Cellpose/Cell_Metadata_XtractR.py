# Extract Metadata Per Cell

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
