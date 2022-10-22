import tensorflow_addons as tfa
from tensorflow import keras
from tensorflow.keras import layers

from .utils import ReflectionPadding2D, downsample, residual_block, upsample


class Generator:
    def __init__(
        self,
        img_size,
        kernel_init,
        gamma_init,
        filters=64,
        num_downsampling_blocks=2,
        num_residual_blocks=9,
        num_upsample_blocks=2,
        name=None,
    ):

        inputs = layers.Input(shape=img_size, name=name + "_input")

        x = ReflectionPadding2D(padding=(3, 3))(inputs)
        x = layers.Conv2D(
            filters, (7, 7), kernel_initializer=kernel_init, use_bias=False
        )(x)
        x = tfa.layers.InstanceNormalization(gamma_initializer=gamma_init)(x)
        x = layers.Activation("relu")(x)

        for _ in range(num_downsampling_blocks):
            filters *= 2
            x = downsample(
                x,
                filters=filters,
                kernel_init=kernel_init,
                gamma_init=gamma_init,
                activation=layers.Activation("relu"),
            )

        for _ in range(num_residual_blocks):
            x = residual_block(
                x,
                kernel_init=kernel_init,
                gamma_init=gamma_init,
                activation=layers.Activation("relu"),
            )

        for _ in range(num_upsample_blocks):
            filters //= 2
            x = upsample(
                x,
                filters,
                kernel_init=kernel_init,
                gamma_init=gamma_init,
                activation=layers.Activation("relu"),
            )

        x = ReflectionPadding2D(padding=(3, 3))(x)
        x = layers.Conv2D(3, (7, 7), padding="valid")(x)
        x = layers.Activation("tanh")(x)

        self.model = keras.models.Model(inputs, x, name=name)
