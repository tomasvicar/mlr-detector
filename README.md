# Live object detection in the browser

A webcam object detector for lab 10 of the course *Machine Learning* (MPA-MLR).
It runs **YOLO11n** (Ultralytics, exported to ONNX at 320 px) with
**ONNX Runtime Web** entirely in the browser — no image leaves the device.

**Open it:** <https://tomasvicar.github.io/mlr-detector/>

Controls: confidence threshold, NMS on/off, NMS IoU threshold, per-class or
class-agnostic NMS, freeze frame, a test image and a photo upload when the
camera is blocked.

- `index.html` — the page (decode of the raw 1 × 84 × 2100 output and NMS in plain JavaScript)
- `model/yolo11n_320.onnx` — the model, reproduced by `make_model.py`
- `vendor/` — a self-hosted copy of ONNX Runtime Web (MIT), used when jsDelivr is unreachable
- `SOURCES.md` — versions, checksums, licences and what was checked

## Licence

YOLO11n and its exported weights are © Ultralytics, licensed under
[AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html); this repository is
therefore AGPL-3.0 as well (see `LICENSE`). ONNX Runtime Web is MIT
(`vendor/onnxruntime-web-1.31.1/LICENSE.txt`). The source of this page is kept
in the course repository under `course_pages/apps/detector/` and copied here.
