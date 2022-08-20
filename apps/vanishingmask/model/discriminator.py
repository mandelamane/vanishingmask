from tensorflow import keras
from tensorflow.keras import layers

from .utils import downsample


class Discriminator:
    def __init__(
        self,
        img_size,
        kernel_init,
        gamma_init,
        filters=64,
        num_downsampling=3,
        name=None,
    ):

        inputs = layers.Input(shape=img_size, name=name + "_img_input")

        x = layers.Conv2D(
            filters,
            (4, 4),
            strides=(2, 2),
            padding="same",
            kernel_initializer=kernel_init,
        )(inputs)
        x = layers.LeakyReLU(0.2)(x)

        num_filters = filters
        for num_downsample_block in range(3):
            num_filters *= 2
            if num_downsample_block < 2:
                x = downsample(
                    x,
                    filters=num_filters,
                    activation=layers.LeakyReLU(0.2),
                    kernel_init=kernel_init,
                    gamma_init=gamma_init,
                    kernel_size=(4, 4),
                    strides=(2, 2),
                )
            else:
                x = downsample(
                    x,
                    filters=num_filters,
                    activation=layers.LeakyReLU(0.2),
                    kernel_init=kernel_init,
                    gamma_init=gamma_init,
                    kernel_size=(4, 4),
                    strides=(1, 1),
                )

        x = layers.Conv2D(
            1, (4, 4), strides=(1, 1), padding="same", kernel_initializer=kernel_init
        )(x)

        self.model = keras.models.Model(inputs=inputs, outputs=x, name=name)
