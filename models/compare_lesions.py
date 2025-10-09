import nibabel as nib
import numpy as np
from scipy.ndimage import zoom
import matplotlib.pyplot as plt
import argparse
import os

# ----------------------------
# Argument Parser
# ----------------------------
parser = argparse.ArgumentParser(description="Evaluate overlap between MindGlide segmentation and expert gold-standard lesions.")
parser.add_argument('--patient', type=str, required=True, help="Patient ID (e.g. patient01)")
parser.add_argument('--data_dir', type=str, default='../open_ms_data/cross_sectional/MNI', help="Base path to dataset directory")
args = parser.parse_args()

# ----------------------------
# File paths
# ----------------------------
patient_dir = os.path.join(args.data_dir, args.patient)
gold_path = os.path.join(patient_dir, 'GOLD_STANDARD_N4_noneck_reduced_winsor_regtoFLAIR_regtoMNI.nii.gz')
seg_path  = os.path.join(patient_dir, 'FLAIR_N4_noneck_reduced_winsor_regtoFLAIR_brain_N4_regtoMNI_mindglide_seg.nii.gz')

# ----------------------------
# File validation
# ----------------------------
for path in [gold_path, seg_path]:
    if not os.path.exists(path):
        raise FileNotFoundError(f" File not found: {path}")

# ----------------------------
# Load images
# ----------------------------
print(f"📂 Loading data for {args.patient}...")
gold = nib.load(gold_path).get_fdata()
seg  = nib.load(seg_path).get_fdata()

# ----------------------------
# Align dimensions (if needed)
# ----------------------------
if gold.shape != seg.shape:
    zoom_factors = np.array(gold.shape) / np.array(seg.shape)
    seg = zoom(seg, zoom_factors, order=0)

# ----------------------------
# Compute lesion statistics
# ----------------------------
expert_lesions = int(np.sum(gold == 1))
mindglide_lesions = int(np.sum(seg == 18))
overlap = int(np.sum((seg == 18) & (gold == 1)))

recall = (mindglide_lesions / expert_lesions * 100) if expert_lesions > 0 else 0
precision = (overlap / mindglide_lesions * 100) if mindglide_lesions > 0 else 0

print(f" Expert ground truth lesions: {expert_lesions:,} voxels")
print(f" MindGlide detected lesions: {mindglide_lesions:,} voxels")
print(f"Detection rate: {recall:.1f}% of expert lesions")
print(f"Overlapping voxels: {overlap:,}")
print(f"MindGlide precision: {precision:.1f}%")

# ----------------------------
# Visualization
# ----------------------------
slice_idx = gold.shape[2] // 2  # middle slice
plt.imshow(gold[:, :, slice_idx], cmap='gray')
plt.imshow(seg[:, :, slice_idx], cmap='Reds', alpha=0.5)
plt.title(f"{args.patient}: Expert (gray) vs MindGlide (red)")
plt.axis('off')
plt.show()
