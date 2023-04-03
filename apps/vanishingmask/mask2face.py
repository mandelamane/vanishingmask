import io

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow import keras
from tensorflow.keras.losses import mean_squared_error
from tensorflow.keras.utils import CustomObjectScope


def binary2array(img_binary):
    stream = img_binary.stream.read()
    png = np.frombuffer(stream, dtype=np.uint8)
    img_array = cv2.imdecode(png, cv2.IMREAD_COLOR)[:, :, ::-1]
    return img_array


def ssim_l1_loss(gt, y_pred, max_val=1.0, l1_weight=1.0):
    ssim_loss = 1 - tf.reduce_mean(tf.image.ssim(gt, y_pred, max_val=max_val))
    l1 = mean_squared_error(gt, y_pred)
    return ssim_loss + tf.cast(l1 * l1_weight, tf.float32)


def ssim_loss(gt, y_pred, max_val=1.0):
    return 1 - tf.reduce_mean(tf.image.ssim(gt, y_pred, max_val=max_val))


def generate_face(img_binary, img_size=(256, 256)):
    img_array = binary2array(img_binary)

    img_shape = img_array.shape
    height, width = img_shape[0], img_shape[1]

    cut_index1 = (width - height) // 2
    cut_index2 = (width + height) // 2

    img_array = img_array[:, cut_index1:cut_index2]
    img_resized = cv2.resize(img_array, img_size)

    img_normalized = img_resized[:, :, ::-1].astype(np.float32) / 255.0
    img_normalized = img_normalized[np.newaxis, :, :, :]

    with CustomObjectScope(
        {"ssim_loss": ssim_loss, "ssim_l1_loss": ssim_l1_loss}
    ):
        model = keras.models.load_model(
            "apps/vanishingmask/models/mask2face_mega.h5"
        )

    gen_face_array = model.predict(img_normalized)[0][:, :, ::-1]

    gen_face_array_resize = cv2.resize(gen_face_array, (height, height))
    gen_face_array = np.append(
        np.ones((height, cut_index1, 3)), gen_face_array_resize, axis=1
    )
    gen_face_array = np.append(
        gen_face_array, np.ones((height, cut_index1, 3)), axis=1
    )

    img_buffer = io.BytesIO()

    face_img = (gen_face_array * 255.0).astype(np.uint8)
    Image.fromarray(face_img).save(img_buffer, format="PNG")
    face_png = img_buffer.getvalue()

    return face_png
