from numpy import power, arange, newaxis, sin, cos
from numpy import float32 as np_float

from tensorflow import float32 as tf_float
from tensorflow import cast as tf_cast


def get_angles(position, i, d_model):
    angle_rates = 1 / power(10000, (2 * (i // 2)) / np_float(d_model))
    return position * angle_rates


def positional_encoding(position, d_model):
    angle_rads = get_angles(
        arange(position)[:, newaxis],
        arange(d_model)[newaxis, :],
        d_model
    )

    angle_rads[:, 0::2] = sin(angle_rads[:, 0::2])
    angle_rads[:, 1::2] = cos(angle_rads[:, 1::2])
    pos_encoding = angle_rads[newaxis, ...]

    return tf_cast(pos_encoding, dtype=tf_float)
