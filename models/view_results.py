import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

# ----------------------------
# Argument Parser
# ----------------------------
parser = argparse.ArgumentParser(description="Visualize MindGlide segmentation results for a given patient.")
parser.add_argument('--patient', type=str, required=True, help="Patient ID (e.g. patient22)")
parser.add_argument('--data_dir', type=str, default='../open_ms_data/cross_sectional/MNI', help="Base path to data directory")
args = parser.parse_args()

# ----------------------------
# File paths
# ----------------------------
patient_dir = os.path.join(args.data_dir, args.patient)

scan_path = os.path.join(patient_dir, 'FLAIR_N4_noneck_reduced_winsor_regtoFLAIR_brain_N4_regtoMNI.nii.gz')
seg_path = os.path.join(patient_dir, 'FLAIR_N4_noneck_reduced_winsor_regtoFLAIR_brain_N4_regtoMNI_mindglide_seg.nii.gz')
gold_path = os.path.join(patient_dir, 'GOLD_STANDARD_N4_noneck_reduced_winsor_regtoFLAIR_regtoMNI.nii.gz')

# Check if files exist
for path in [scan_path, seg_path, gold_path]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File not found: {path}")

# ----------------------------
# Load data
# ----------------------------
print(f"📂 Loading data for {args.patient}...")
scan = nib.load(scan_path).get_fdata()
seg = nib.load(seg_path).get_fdata()
gold = nib.load(gold_path).get_fdata()

# ----------------------------
# Visualization
# ----------------------------
slice_idx = scan.shape[2] // 2
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Original FLAIR
axes[0,0].imshow(scan[:,:,slice_idx].T, cmap='gray', origin='lower')
axes[0,0].set_title('Original FLAIR Scan', fontsize=14)
axes[0,0].axis('off')

# Full segmentation (20 classes)
axes[0,1].imshow(seg[:,:,slice_idx].T, cmap='tab20', origin='lower')
axes[0,1].set_title('MindGlide: All Brain Structures', fontsize=14)
axes[0,1].axis('off')

# MindGlide lesions (class 18)
axes[1,0].imshow(scan[:,:,slice_idx].T, cmap='gray', origin='lower')
lesion_mask = np.ma.masked_where(seg[:,:,slice_idx] != 18, seg[:,:,slice_idx])
axes[1,0].imshow(lesion_mask.T, cmap='Reds', alpha=0.7, origin='lower')
axes[1,0].set_title('MindGlide Lesions (Class 18) in Red', fontsize=14)
axes[1,0].axis('off')

# Ground truth lesions
axes[1,1].imshow(scan[:,:,slice_idx].T, cmap='gray', origin='lower')
gold_mask = np.ma.masked_where(gold[:,:,slice_idx] == 0, gold[:,:,slice_idx])
axes[1,1].imshow(gold_mask.T, cmap='Greens', alpha=0.7, origin='lower')
axes[1,1].set_title('Expert Ground Truth in Green', fontsize=14)
axes[1,1].axis('off')

plt.tight_layout()

# Save figure
output_name = f"{args.patient}_comparison.png"
plt.savefig(output_name, dpi=150, bbox_inches='tight')
print(f" Saved visualization to: {output_name}")
plt.show()
