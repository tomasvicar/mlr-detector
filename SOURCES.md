# Live object detector (lab 10) — sources

The page `index.html` runs a pre-trained YOLO11n on the camera image in the
browser (ONNX Runtime Web, single-thread WASM), decodes the raw output and runs
NMS in plain JavaScript. Made on 22 November 2026 for lab 10 (author's
decisions of 11 and 22 November 2026 in `exercises/ex10/sources.md`; design in
`exercises/ex10/brainstorm-2026-11-09/SELECTION.md`, Task 1). It goes public
with lab 10 (`APP_LABS` in `tools/build_web.py`); Quarto copies the files
through `resources` in `course_pages/_quarto.yml`. This file is not deployed.

## Model

- **YOLO11n**, Ultralytics, COCO-trained (80 classes), weights `yolo11n.pt`
  downloaded by Ultralytics on first use.
- **Licence: AGPL-3.0** (<https://github.com/ultralytics/ultralytics>,
  <https://www.ultralytics.com/license>, which lists academic coursework under
  the free AGPL tier). The page shows the notice, links the Ultralytics
  repository and serves its own source (the HTML file itself, the ONNX file and
  `make_model.py`, all deployed next to the page) — the AGPL network clause.
- **Export:** `make_model.py` (the command is in its docstring), ultralytics
  8.4.216, onnx 1.23.2, onnxslim 0.1.99, torch 2.15.0, opset 17, `imgsz=320`,
  static shape, no NMS in the graph. Re-running it gave a byte-identical file.
- `model/yolo11n_320.onnx`: 10 615 289 bytes, sha256
  `1f47dce240becbce8df757bf796743cbc21e3696c8aa2472f4eb6a5bcd4b61cb`.
  Input `1 × 3 × 320 × 320` (RGB, 0–1, letterboxed with grey 114), output
  `1 × 84 × 2100` (cx, cy, w, h in input pixels + 80 class scores, anchor-free).

## Test image

- `test/bus.jpg` (810 × 1080) is copied from the `ultralytics` package
  (`ultralytics/assets/bus.jpg`), which is distributed under AGPL-3.0; the
  page credits it as such. Who took the photograph is not stated by
  Ultralytics. sha256
  `c02019c4979c191eb739ddd944445ef408dad5679acab6fd520ef9d434bfbc63`.
- **Reference result** (Ultralytics `predict` on the exported ONNX, imgsz 320,
  conf 0.25, IoU 0.45, CPU): bus 0.846, persons 0.811, 0.803, 0.731, 0.317.
  The page (canvas resize instead of OpenCV) gives 2100 candidates, 41 above
  confidence 0.25, 5 after NMS: bus 0.846, persons 0.842, 0.811, 0.781, 0.290
  (headless Chromium, 22 November 2026).
- **NMS threshold 0.5** (IoU > 0.5 within a class is removed), the value of the
  lecture slide "Box IoU and NMS by hand" and of the lab notebook; the builder
  had 0.45 (the YOLOv5-era default; Ultralytics `predict` now defaults to 0.7).
  On the test image this changes nothing at confidence ≥ 0.1; at 0.05 one more
  person box (0.096) survives (7 instead of 6).

## NMS controls (added 22 November 2026, approved for lab 10)

- **IoU-threshold slider** 0.1–0.95 (step 0.05, default 0.5): redraws from the
  stored model output like the confidence slider, no new inference.
- **Per-class / class-agnostic NMS** buttons (default per-class). Per-class
  compares only boxes of the same class; class-agnostic compares all boxes, as
  the `nms(boxes, scores, threshold=0.5)` of the lab notebook does (it takes no
  classes). The page says this in one sentence.
- **Measured** on the test image at confidence 0.25 (headless Chromium,
  Playwright, 22 November 2026), after-NMS count of 41 above confidence:

  | IoU threshold | 0.3 | 0.5 | 0.7 | 0.9 |
  | --- | --- | --- | --- | --- |
  | per-class | 5 | 5 | 5 | 6 |
  | class-agnostic | 5 | 5 | 5 | 6 |

  On this image the two modes do not differ at confidence 0.25 (the bus and
  the persons overlap by less than 0.3), and a duplicate comes back only at
  0.9; at 0.5 the result is unchanged (bus 0.846, persons 0.842, 0.811, 0.781,
  0.290). No horizontal scroll at 1280 px and 390 px, no page errors.

## Runtime

- **onnxruntime-web 1.31.1** (MIT, Microsoft), the WASM-only build
  `ort.wasm.bundle.min.mjs`, loaded from jsDelivr
  (`https://cdn.jsdelivr.net/npm/onnxruntime-web@1.31.1/dist/`). If that fails,
  the page loads the same files from `vendor/onnxruntime-web-1.31.1/`, copied
  unchanged from the npm tarball
  `https://registry.npmjs.org/onnxruntime-web/-/onnxruntime-web-1.31.1.tgz`
  (`package/dist/`); the tarball has no licence file, so `LICENSE.txt` there
  carries the MIT notice of the onnxruntime repository.

  | file | bytes | sha256 |
  | --- | --- | --- |
  | `ort.wasm.bundle.min.mjs` | 77 024 | `51bd7168…865f8dd` (identical to jsDelivr's) |
  | `ort-wasm-simd-threaded.mjs` | 24 738 | `30ed0b5c…770dac3` |
  | `ort-wasm-simd-threaded.wasm` | 14 848 852 | `4b884c20…cda001d` |

- One thread unless the page is cross-origin isolated (GitHub Pages is not),
  as in `course_pages/apps/classifier/`.

## QR code

`qr.svg` points to `https://tomasvicar.github.io/MLR-public/apps/detector/`,
made by `make_qr.py` (it only writes `qr.svg`; nothing is embedded in a
notebook).

## Checked (22 November 2026, headless Chromium, Playwright)

- Runtime from jsDelivr, and with jsDelivr blocked from `vendor/`: both load.
- Test image: the result above; NMS off shows all 41 boxes.
- Fake camera (a 640 × 480 video of `bus.jpg`): the loop runs at about
  7–8 frames/s, inference about 100 ms; bus + 3 persons on the live frame
  (the small person at the left edge falls below 0.25 at that resolution).
  Freeze frame, then confidence 0.10: 47 above, 6 after NMS.
- Not checked: a real lab computer, a phone (iOS Safari, Android Chrome).

## Review (22 November 2026, independent reviewer)

- **Decode and NMS:** the page's raw output (read from the page) was decoded
  and NMS-ed independently in Python/NumPy: identical counts and boxes at
  confidence 0.05 / 0.1 / 0.25 / 0.5 / 0.8 → above 63 / 48 / 41 / 36 / 14,
  after NMS 7 / 5 / 5 / 4 / 3 (bus 0.846 at [24, 230, 808, 739]). A separate
  end-to-end run with `onnxruntime` (Python, PIL bilinear letterbox) gave
  58 / 48 / 42 / 36 / 14 above and the same detections after NMS from 0.1 up
  (the differences are the resampling).
- **Changes:** NMS 0.45 → 0.5 (above); box line width and label size now
  follow the size on screen (2 and 13 screen pixels — before, labels were
  about 6 px on a 390 px phone), labels kept inside the image, redraw on
  resize; the stage takes the aspect ratio of the image (max 72 % of the
  viewport height), so portrait photos and phone cameras are not shrunk;
  a camera inference still running when the camera is stopped no longer
  overwrites a photo or the test image.
- **Playwright** (fake camera from a 640 × 480 video of `bus.jpg`, 1280 px and
  390 px viewports, jsDelivr blocked → `vendor/`, served from the source and
  from `_site` after `tools/build_web.py`): test image, slider, NMS off
  (41 boxes), upload, camera (about 9–10 frames/s, inference about 95 ms,
  4 boxes), freeze + confidence 0.10 (46 above, 6 after NMS), stop, no
  horizontal scroll. The only external requests are the three GETs of the
  runtime from jsDelivr; no POST, no request carries image data.
- Not checked: a real lab computer, a phone (iOS Safari, Android Chrome).

## Public copy: `tomasvicar/mlr-detector` (22 November 2026)

At the author's request the page is also published as its own public
repository with GitHub Pages: <https://github.com/tomasvicar/mlr-detector>,
<https://tomasvicar.github.io/mlr-detector/>. It is a plain copy of this folder
plus `README.md`, `LICENSE` (AGPL-3.0 text) and `.nojekyll`; `sources.md` is
renamed to `SOURCES.md`. The QR code and the "open on your phone" link point to
that URL. **This folder stays the source**: after a change, copy it into a
clone of `mlr-detector` (keeping README.md, LICENSE, .nojekyll), rename
`sources.md` to `SOURCES.md`, commit and push. Checked after the first push:
the test image gives bus 0.85 + persons 0.84, 0.81, 0.78, 0.29 on the live URL.
