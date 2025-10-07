```markdown
# 🧠 MindGlide-MS  
**Automated Multiple Sclerosis Lesion Segmentation using Deep Learning**

MindGlide-MS integrates the **MindGlide** lesion segmentation model with open-access **MSSEG1 MRI datasets** to enable automated, reproducible lesion detection and evaluation on MRI scans of MS patients.  
This repository wraps data, models, and processing pipelines inside a Docker environment for easy deployment.

---

## 📂 Repository Structure

```

mindglide-ms/
│
├── data/
│   └── msseg1/                # Submodule: Open MS Dataset ([https://github.com/muschellij2/open_ms_data](https://github.com/muschellij2/open_ms_data))
│
├── models/
│   └── mindglide/             # Submodule: MindGlide segmentation model ([https://github.com/mMedcon/mindGlide](https://github.com/mMedcon/mindGlide))
│
├── notebooks/                 # Example analysis and visualization notebooks
├── src/                       # Helper scripts for preprocessing / evaluation
├── environment.yml            # Conda environment specification
├── Makefile                   # Optional build commands
├── LICENSE
└── README.md

````

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository (with Submodules)

```bash
git clone --recurse-submodules https://github.com/<your-username>/mindglide-ms.git
cd mindglide-ms
````

If you already cloned without `--recurse-submodules`, run:

```bash
git submodule update --init --recursive
```

---

### Setup

If you’re not using Docker, create the environment manually:

```bash
conda env create -f environment.yml
conda activate mindglide
```

---

### Running Inference with Docker 🐳

This repo uses a prebuilt Docker image:
**`mspinpoint/mindglide:may2024`**

Make sure Docker and NVIDIA GPU drivers are installed, then run:

```bash
# Set the patient ID
PATIENT_ID="patient01"

docker run --ipc=host --ulimit memlock=-1 -it --rm \
  --gpus all \
  -u "$(id -u):$(id -g)" \
  -v "$(pwd):/mnt" \
  --entrypoint "" \
  mspinpoint/mindglide:may2024 \
  python3 /mnt/mindglide/mindGlide/run_inference.py \
    --model_file_paths /mnt/models/_20240404_conjurer_trained_dice_7733.pt \
    --scan_path /mnt/data/msseg1/cross_sectional/MNI/${PATIENT_ID}/FLAIR_N4_noneck_reduced_winsor_regtoFLAIR_brain_N4_regtoMNI.nii.gz \
    --gold_standard_path /mnt/data/msseg1/cross_sectional/MNI/${PATIENT_ID}/lesion_mask_goldstandard.nii.gz
```

Simply change `PATIENT_ID="patient02"` for the next patient.

---

### Updating Submodules

If you want the latest version of either dataset or model:

```bash
cd data/msseg1
git pull origin main
cd ../../models/mindglide
git pull origin main
cd ../..
git add data/msseg1 models/mindglide
git commit -m "Update submodules to latest versions"
```

---

## Components Overview

| Component                 | Description                                                           |
| ------------------------- | --------------------------------------------------------------------- |
| **MindGlide**             | Deep learning model (DoubleU-Net) trained for MS lesion segmentation  |
| **Open_MS_Data (MSSEG1)** | Publicly available MRI dataset of MS patients (FLAIR, T1, T2, T1Post) |
| **Docker Image**          | Preconfigured environment with dependencies and GPU support           |
| **Notebooks**             | Example scripts for visualizing results and comparing gold standards  |

---

## 📊 Example Output

After running inference, results typically include:

* Predicted lesion mask (`*_seg.nii.gz`)
* Overlap metrics (Dice score, volume difference, etc.)
* Visualization notebooks for lesion overlays

---

## License

This project is distributed under the **MIT License**.
Please review dataset licenses (MSSEG1) before redistribution.

---

## 🙌 Acknowledgements

* [mMedcon/mindGlide](https://github.com/mMedcon/mindGlide) for model development
* [muschellij2/open_ms_data](https://github.com/muschellij2/open_ms_data) for the open dataset
* The open-source neuroimaging community for tool support (NiBabel, MONAI, PyTorch)


---

> *MindGlide-MS: accelerating MS lesion detection through open data and deep learning.*

```

---
