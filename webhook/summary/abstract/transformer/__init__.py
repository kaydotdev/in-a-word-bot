import tensorflow as tf

from tokenizers import Tokenizer
from .transformer import Transformer
from .masking import create_masks


class SummaryTransformer:
    def __init__(self, tokenizer_config, transformer_path,
                 num_layers=6, d_model=128, num_heads=8, dff=512,
                 encoder_vocab_size=50257, decoder_vocab_size=50257,
                 encoder_maxlen=400, decoder_maxlen=75):
        self.tokenizer = Tokenizer.from_file(tokenizer_config)
        self.transformer = Transformer(
            num_layers, d_model, num_heads, dff,
            encoder_vocab_size, decoder_vocab_size,
            pe_input=encoder_vocab_size, pe_target=decoder_vocab_size,
        )

        ### Cold-start problem ###
        enc_padding_mask, combined_mask, dec_padding_mask = create_masks(tf.zeros((1, encoder_maxlen)),
                                                                         tf.zeros((1, 1)))
        self.transformer(
            tf.zeros((1, encoder_maxlen)), tf.zeros((1, 1)), False,
            enc_padding_mask, combined_mask, dec_padding_mask
        )
        ### --- --- ###

        self.transformer.load_weights(transformer_path)
        self.encoder_maxlen = encoder_maxlen
        self.decoder_maxlen = decoder_maxlen

    def summarize(self, input_document):
        input_document = [self.tokenizer.encode("[START] " + input_document).ids]
        input_document = tf.keras.preprocessing.sequence.pad_sequences(input_document, maxlen=self.encoder_maxlen,
                                                                       padding='post', truncating='post')

        encoder_input = tf.expand_dims(input_document[0], 0)
        output = tf.expand_dims(self.tokenizer.encode("[TL;DR]").ids, 0)

        for i in range(self.decoder_maxlen):
            enc_padding_mask, combined_mask, dec_padding_mask = create_masks(encoder_input, output)
            predictions, attention_weights = self.transformer(
                encoder_input,
                output,
                False,
                enc_padding_mask,
                combined_mask,
                dec_padding_mask
            )

            predictions = predictions[:, -1:, :]
            predicted_id = tf.cast(tf.argmax(predictions, axis=-1), tf.int32)

            if predicted_id == self.tokenizer.encode("[END]").ids[0]:
                break

            output = tf.concat([output, predicted_id], axis=-1)

        return self.tokenizer.decode(
            tf.squeeze(output, axis=0).numpy()
        )
