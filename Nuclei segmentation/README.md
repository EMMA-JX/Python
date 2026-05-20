# Nuclei Segmentation on PanNuke

This project performs nuclei instance segmentation on the PanNuke dataset using a ResNet50 + U-Net style model with auxiliary horizontal/vertical (HV) map prediction.

## Files

- `ddp_run.py`: training script
- `infer.py`: inference and evaluation
- `get_test_image.py`: export one sample image and masks
- `Model.py`: model definition
- `dataset.py`: dataset loading
- `loss.py`, `metrics.py`, `tools.py`: utilities

## How to run

### Train

```bash
python ddp_run.py
```

### Prepare one sample image

```bash
python get_test_image.py
```

This creates files in `test_image/`, including:

- `original.png`
- `merged_mask.png`
- `instances_grid.png`
- `h_map.png`
- `v_map.png`

### Inference

```bash
python infer.py
```

`infer.py` can be used for:

- single-image prediction
- full-dataset evaluation
- exporting instance results as `.geojson`

## Output

- `results/plt_output/`: saved visualization images
- `results/pth_output/`: model checkpoints
- `results/output_instances.geojson`: exported instance result

