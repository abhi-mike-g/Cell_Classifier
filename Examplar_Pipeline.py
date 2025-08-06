import torch
import tifffile as tiff

# Load trained model (replace with your model path)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = UNet()
model.load_state_dict(torch.load("unet_rbc.pth", map_location=device))
model.to(device)
model.eval()

# Process a single image
image_path = "example.tiff"
image = tiff.imread(image_path).astype(np.float32)
image_norm = (image - image.min()) / (image.max() - image.min())
input_tensor = torch.tensor(image_norm).unsqueeze(0).unsqueeze(0).to(device)

with torch.no_grad():
    mask_pred = model(input_tensor).cpu().numpy()[0,0]

cells = extract_cells(mask_pred, image)
save_metadata("example.tiff", cells, "example.json")

print(f"Extracted {len(cells)} cells from {image_path}")
