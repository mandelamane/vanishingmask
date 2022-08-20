import io

import cv2
import numpy as np
from PIL import Image
from tensorflow import keras

from .model.utils import ReflectionPadding2D


def binary2array(img_binary):
    stream = img_binary.stream.read()
    png = np.frombuffer(stream, dtype=np.uint8)
    img_array = cv2.imdecode(png, cv2.IMREAD_COLOR)[:, :, ::-1]
    return img_array


def generate_face(img_binary, img_size=(200, 200)):
    img_array = binary2array(img_binary)
    img_resized = cv2.resize(img_array, img_size)
    img_normalized = (img_resized.astype(np.float32) / 127.5) - 1.0
    img_normalized = img_normalized[np.newaxis, :, :, :]

    model = keras.models.load_model(
        "apps/vanishingmask/checkpoints/mask2face_212.h5",
        custom_objects={"ReflectionPadding2D": ReflectionPadding2D},
    )

    gen_face_array = model(img_normalized, training=False)[0].numpy()

    img_buffer = io.BytesIO()
    face_img = (gen_face_array * 127.5 + 127.5).astype(np.uint8)
    Image.fromarray(face_img).save(img_buffer, format="PNG")
    face_png = img_buffer.getvalue()

    return face_png
