import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow.keras import layers


class ReflectionPadding2D(layers.Layer):
    def __init__(self, padding=(1, 1), **kwargs):
        self.padding = tuple(padding)
        super(ReflectionPadding2D, self).__init__(**kwargs)

    def call(self, input_tensor, mask=None):
        padding_width, padding_height = self.padding
        padding_tensor = [
            [0, 0],
            [padding_height, padding_height],
            [padding_width, padding_width],
            [0, 0],
        ]
        return tf.pad(input_tensor, padding_tensor, mode="REFLECT")

    def get_config(self):
        config = {"padding": self.padding}
        base_config = super(ReflectionPadding2D, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


def downsample(
    x,
    filters,
    activation,
    kernel_init,
    gamma_init,
    kernel_size=(3, 3),
    strides=(2, 2),
    padding="same",
    use_bias=False,
):

    x = layers.Conv2D(
        filters,
        kernel_size,
        strides=strides,
        kernel_initializer=kernel_init,
        padding=padding,
        use_bias=use_bias,
    )(x)

    x = tfa.layers.InstanceNormalization(gamma_initializer=gamma_init)(x)

    if activation:
        x = activation(x)

    return x


def upsample(
    x,
    filters,
    activation,
    kernel_init,
    gamma_init,
    kernel_size=(3, 3),
    strides=(2, 2),
    padding="same",
    use_bias=False,
):

    x = layers.Conv2DTranspose(
        filters,
        kernel_size,
        strides=strides,
        padding=padding,
        kernel_initializer=kernel_init,
        use_bias=use_bias,
    )(x)

    x = tfa.layers.InstanceNormalization(gamma_initializer=gamma_init)(x)

    if activation:
        x = activation(x)

    return x


def residual_block(
    x,
    activation,
    kernel_init,
    gamma_init,
    kernel_size=(3, 3),
    strides=(1, 1),
    padding="valid",
    use_bias=False,
):

    xdim = x.shape[-1]
    input_tensor = x

    x = ReflectionPadding2D()(input_tensor)

    x = layers.Conv2D(
        xdim,
        kernel_size,
        strides=strides,
        kernel_initializer=kernel_init,
        padding=padding,
        use_bias=use_bias,
    )(x)

    x = tfa.layers.InstanceNormalization(gamma_initializer=gamma_init)(x)
    x = activation(x)

    x = ReflectionPadding2D()(x)

    x = layers.Conv2D(
        xdim,
        kernel_size,
        strides=strides,
        kernel_initializer=kernel_init,
        padding=padding,
        use_bias=use_bias,
    )(x)

    x = tfa.layers.InstanceNormalization(gamma_initializer=gamma_init)(x)
    x = layers.add([input_tensor, x])

    return x
