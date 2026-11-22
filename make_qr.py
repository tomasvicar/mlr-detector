"""Regenerate the QR code of the detector page.

uv run --no-project --with qrcode --with pillow python course_pages/apps/detector/make_qr.py
"""
from pathlib import Path

import qrcode
from qrcode.image.svg import SvgPathImage

HERE = Path(__file__).resolve().parent
URL = 'https://tomasvicar.github.io/mlr-detector/'

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=4)
qr.add_data(URL)
qr.make(fit=True)
qr.make_image(image_factory=SvgPathImage).save(HERE / 'qr.svg')
print('Generated qr.svg:', URL)
