import base64
from PIL import Image
from io import BytesIO
import base64

def encode_and_resize(image, crop=True):
    image = Image.open(BytesIO(image))
    width, _ = image.size

    left = 0
    top = 0
    right = width
    bottom = 768

    if crop:
        image = image.crop((left, top, right, bottom))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image

def extract_logo(url: str):
    return url