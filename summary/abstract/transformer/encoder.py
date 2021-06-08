import tensorflow as tf

from attention import MultiHeadAttention
from embedding import positional_encoding


class EncoderLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super(EncoderLayer, self).__init__()

        self.multi_head_attention = MultiHeadAttention(d_model, num_heads)
        self.encoding_feedforward = tf.keras.Sequential([
            tf.keras.layers.Dense(dff, activation='relu'),
            tf.keras.layers.Dense(d_model)
        ])

        self.multi_head_attention_norm = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.encoding_feedforward_norm = tf.keras.layers.LayerNormalization(epsilon=1e-6)

        self.multi_head_attention_dropout = tf.keras.layers.Dropout(rate)
        self.encoding_feedforward_dropout = tf.keras.layers.Dropout(rate)

    def call(self, x, training, mask):
        attention_output, _ = self.multi_head_attention(x, x, x, mask)
        attention_output = self.multi_head_attention_dropout(attention_output, training=training)
        multi_head_attention_out = self.multi_head_attention_norm(x + attention_output)

        encoding_feedforward_output = self.encoding_feedforward(multi_head_attention_out)
        encoding_feedforward_output = self.encoding_feedforward_dropout(encoding_feedforward_output, training=training)
        encoding_feedforward_out = self.encoding_feedforward_norm(
            multi_head_attention_out + encoding_feedforward_output)

        return encoding_feedforward_out


class Encoder(tf.keras.layers.Layer):
    def __init__(self, num_layers, d_model, num_heads, dff,
                 input_vocab_size, maximum_position_encoding, rate=0.1):
        super(Encoder, self).__init__()

        self.d_model = d_model
        self.num_layers = num_layers

        self.embedding = tf.keras.layers.Embedding(input_vocab_size, d_model)
        self.pos_encoding = positional_encoding(maximum_position_encoding, self.d_model)

        self.enc_layers = [EncoderLayer(d_model, num_heads, dff, rate) for _ in range(num_layers)]

        self.dropout = tf.keras.layers.Dropout(rate)

    def call(self, x, training, mask):
        seq_len = tf.shape(x)[1]

        x = self.embedding(x)
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
        x += self.pos_encoding[:, :seq_len, :]

        x = self.dropout(x, training=training)

        for i in range(self.num_layers):
            x = self.enc_layers[i](x, training, mask)

        return x
