# PanNuke Nuclei Instance Segmentation (Distributed Deep Learning Pipeline)

## Overview

This project implements a distributed deep learning pipeline for **nuclei instance segmentation** on the **PanNuke dataset**. The pipeline is based on a **ResNet50 + U-Net-like architecture** with dual-task predictions:

- **Binary nuclei mask segmentation**
- **Horizontal and Vertical (HoVer) distance map regression** for instance separation.

The pipeline supports **DistributedDataParallel (DDP)** to fully utilize multiple GPUs for efficient training.



### Features

- **Dual-Task Architecture**: Mask segmentation and HV-map regression.
- **Data Augmentation**: Geometry (shape) and color transformations.
- **Multi-GPU Training**: Efficient training using PyTorch DDP.
- **Evaluation Metrics**: DICE, AJI, AJI+, DQ, SQ, PQ.
- **Instance Export**: Results saved in `.geojson` and `.mat` formats for visualization or further processing.



## Repository Structure

### Main Output Directory:

```bash
results/
├── plt_output/        # Visualization output
│   ├── mask/
│   └── hv/
└── pth_output/        # Model checkpoints
    ├── mask/
    └── hv/
```

### Main Scripts:

- `dataset.py`: Data loading and preprocessing for PanNuke.
- `ddp_run.py`: Multi-GPU training using DDP.
- `infer.py`: Inference and evaluation on test data.
- `get_test_image.py`: Exports a single sample image and associated maps.
- `loss.py`: Loss functions (Cross-Entropy, Dice, MSE, MSGE).
- `metrics.py`: Metrics computation (DICE, AJI, PQ, etc.).
- `Model.py`: ResNet50 + U-Net-like dual-task model architecture.
- `tools.py`: Utilities for augmentation, visualization, and evaluation.



## Running the Code

### Training

#### Usage:

```bash
python ddp_run.py
```

#### Configurable Parameters:

- `dataset_path`: Path to store the dataset. Downloads if not present.
- `plt_output_path`: Path to save mask and HV-map visualizations.
- `pth_output_path`: Path to save model checkpoints.
- `weights_pth`: Path to pretrained weights (optional).
- `folder_name`: Fold selection (`fold1`, `fold2`, `fold3` in PanNuke).
- `os.environ["CUDA_VISIBLE_DEVICES"]`: GPU IDs to use. Remove to use all available GPUs.
- `batch_size`: Batch size for training.
- `epoch_size`: Number of training epochs.
- `save_plt`: Whether to save comparison plots (else displays them).
- `save_pth`: Whether to save model weights after each epoch.

#### Note:

- The program checks for `sampled_data.npz`. If not found, it preprocesses data from `dataset_path` and caches it as `sampled_data.npz` for faster subsequent loading.



### Inference

#### Single Image Preparation:

- To prepare **a sample image** for inference, run:

  ```bash
  python get_test_image.py
  ```

  This will:

  - Select a sample from `fold1` with **16 instances**.
  - Generate visualization files in the `test_image/` directory:
    - `original.png`: Original image.
    - `instances_grid.png`: 4×4 grid of instance masks.
    - `merged_mask.png`: Combined instance mask (Ground Truth).
    - `h_map.png`, `v_map.png`: Ground truth HV-maps.

> **Note**: `get_test_image.py` **does not** generate `.geojson`. It only prepares test images.

#### Single Image Inference and GeoJSON Export:

- To **infer on the prepared single image** and generate a **QuPath-compatible `.geojson`**, run:

  ```bash
  python infer.py
  ```

  Ensure `check_one_image = True` in `infer.py`.
   This will:

  - Load data from `test_image/`.
  - Generate predictions.
  - Save instance segmentation as `results/output_instances.geojson` and `pred_inst.mat`.

#### Full Dataset Inference:

- To **evaluate the entire dataset**, set `check_one_image = False` in `infer.py` and run:

  ```bash
  python infer.py
  ```

  This will process all samples in `sampled_data.npz` and evaluate segmentation performance.



## Segmentation Prediction


<p align="center">
  <img src="./results/seg.png" alt="Segmentation Prediction" width="300"/>
</p>


## Datasets

- [PanNuke Dataset on Hugging Face](https://huggingface.co/datasets/RationAI/PanNuke)



## Model Weights

- [Model Weights](https://drive.google.com/drive/folders/1dHkDqeW3b7rHwZEUZ97cEzKcCFkqLMUA?usp=drive_link)


## Example Segmentation Results

|   DICE   |   AJI    |    DQ    |    SQ    |    PQ    |   AJI+   |
| :------: | :------: | :------: | :------: | :------: | :------: |
| 0.858729 | 0.737947 | 0.817771 | 0.824612 | 0.715987 | 0.746932 |

