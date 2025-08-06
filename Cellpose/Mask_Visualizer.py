# Visualize Masks

import matplotlib.pyplot as plt

plt.imshow(image, cmap='gray')
plt.imshow(masks, alpha=0.3)  # overlay masks
plt.title("Cellpose Segmentation")
plt.show()
