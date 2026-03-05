"""
Fine-tune a YOLOv8 model on a custom ingredient detection dataset.

Usage:
    python scripts/train.py --data path/to/dataset.yaml
    python scripts/train.py --data path/to/dataset.yaml --model yolov8n.pt --epochs 100 --imgsz 640 --batch 16

The dataset must be in YOLO format with a dataset.yaml describing train/val
splits and class names. See https://docs.ultralytics.com/datasets/detect/

Trained weights are saved to data/weights/.
"""

import argparse
from pathlib import Path

from ultralytics import YOLO


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fine-tune YOLOv8 for ingredient detection"
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Path to dataset.yaml (YOLO format)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov8s.pt",
        help="Base model to fine-tune (default: yolov8s.pt)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=50,
        help="Number of training epochs (default: 50)",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Input image size (default: 640)",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=16,
        help="Batch size (default: 16)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Device: 'cpu', '0', '0,1', or 'mps' (default: auto-detect)",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="grubos",
        help="Run name for logging (default: grubos)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    weights_dir = Path("data/weights")
    weights_dir.mkdir(parents=True, exist_ok=True)

    model = YOLO(args.model)

    train_kwargs = dict(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        name=args.name,
        project=str(weights_dir),
        exist_ok=True,
    )
    if args.device is not None:
        train_kwargs["device"] = args.device

    results = model.train(**train_kwargs)

    best_weights = weights_dir / args.name / "weights" / "best.pt"
    if best_weights.exists():
        dest = weights_dir / "best.pt"
        best_weights.rename(dest)
        print(f"\nBest weights saved to: {dest}")
    else:
        print(f"\nTraining complete. Check {weights_dir / args.name} for outputs.")

    return results


if __name__ == "__main__":
    main()
