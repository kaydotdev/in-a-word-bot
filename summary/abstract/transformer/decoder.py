import tensorflow as tf

from .attention import MultiHeadAttention
from .embedding import positional_encoding


class DecoderLayer(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, rate=0.1):
        super(DecoderLayer, self).__init__()

        self.multi_head_attention_masked = MultiHeadAttention(d_model, num_heads)
        self.multi_head_attention = MultiHeadAttention(d_model, num_heads)

        self.decoding_feedforward = tf.keras.Sequential([
            tf.keras.layers.Dense(dff, activation='relu'),
            tf.keras.layers.Dense(d_model)
        ])

        self.multi_head_attention_masked_norm = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.multi_head_attention_norm = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.decoding_feedforward_norm = tf.keras.layers.LayerNormalization(epsilon=1e-6)

        self.multi_head_attention_masked_dropout = tf.keras.layers.Dropout(rate)
        self.multi_head_attention_dropout = tf.keras.layers.Dropout(rate)
        self.decoding_feedforward_dropout = tf.keras.layers.Dropout(rate)

    def call(self, x, enc_output, training, look_ahead_mask, padding_mask):
        attention_masked_output, attention_weights_masked = self.multi_head_attention_masked(x, x, x, look_ahead_mask)
        attention_masked_output = self.multi_head_attention_masked_dropout(attention_masked_output, training=training)
        multi_head_attention_masked_out = self.multi_head_attention_masked_norm(attention_masked_output + x)

        attention_output, attention_weights = self.multi_head_attention(enc_output, enc_output,
                                                                        multi_head_attention_masked_out, padding_mask)
        attention_output = self.multi_head_attention_dropout(attention_output, training=training)
        multi_head_attention_out = self.multi_head_attention_norm(attention_output + multi_head_attention_masked_out)

        decoding_feedforward_output = self.decoding_feedforward(multi_head_attention_out)
        decoding_feedforward_output = self.decoding_feedforward_dropout(decoding_feedforward_output, training=training)
        decoding_feedforward_out = self.decoding_feedforward_norm(
            decoding_feedforward_output + multi_head_attention_out)

        return decoding_feedforward_out, attention_weights_masked, attention_weights


class Decoder(tf.keras.layers.Layer):
    def __init__(self, num_layers, d_model, num_heads, dff, target_vocab_size, maximum_position_encoding, rate=0.1):
        super(Decoder, self).__init__()

        self.d_model = d_model
        self.num_layers = num_layers

        self.embedding = tf.keras.layers.Embedding(target_vocab_size, d_model)
        self.pos_encoding = positional_encoding(maximum_position_encoding, d_model)

        self.dec_layers = [DecoderLayer(d_model, num_heads, dff, rate) for _ in range(num_layers)]
        self.dropout = tf.keras.layers.Dropout(rate)

    def call(self, x, enc_output, training, look_ahead_mask, padding_mask):
        seq_len = tf.shape(x)[1]
        attention_weights = {}

        x = self.embedding(x)
        x *= tf.math.sqrt(tf.cast(self.d_model, tf.float32))
        x += self.pos_encoding[:, :seq_len, :]

        x = self.dropout(x, training=training)

        for i in range(self.num_layers):
            x, aw_masked, aw = self.dec_layers[i](x, enc_output, training, look_ahead_mask, padding_mask)

            attention_weights['decoder_layer{}_aw_masked'.format(i + 1)] = aw_masked
            attention_weights['decoder_layer{}_aw'.format(i + 1)] = aw

        return x, attention_weights
