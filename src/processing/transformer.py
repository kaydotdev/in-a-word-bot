import numpy as np
import onnxruntime as ort
import sentencepiece as spm


class SummaryTransformer:
    ONNX_PROVIERS = {
        "cpu": ['CPUExecutionProvider'],
        "gpu": [
            ('CUDAExecutionProvider', {
                'device_id': 0,
                'arena_extend_strategy': 'kNextPowerOfTwo',
                'cudnn_conv_algo_search': 'EXHAUSTIVE'
            })
        ]
    }

    def __init__(self, text_preprocessor_file: str, model_state_dict_file: str, provider="cpu"):
        self.tokenizer = spm.SentencePieceProcessor(model_file=text_preprocessor_file)
        self.ort_sess = ort.InferenceSession(model_state_dict_file, providers=self.ONNX_PROVIERS.get(provider, ['CPUExecutionProvider']))

    def generate(self, text: str, max_length=128):
        encoded_input = self.tokenizer.encode(text, add_eos=True)

        input_ids = np.expand_dims(np.array(encoded_input), axis=0)
        decoder_input_ids = np.expand_dims(np.array([self.tokenizer.pad_id()]), axis=0)

        flatten_tokens = decoder_input_ids.flatten()

        for _ in range(max_length):
            if int(flatten_tokens[-1]) == self.tokenizer.eos_id(): break

            output_ids = self.ort_sess.run(None, { 'input_ids': input_ids, 'decoder_input_ids': decoder_input_ids })[0]
            flatten_tokens = output_ids.flatten()
            decoder_input_ids = np.expand_dims(np.array([tokenizer.pad_id(), *flatten_tokens]), axis=0)

        return self.tokenizer.decode(decoder_input_ids[0].tolist())
