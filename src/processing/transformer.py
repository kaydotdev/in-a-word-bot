import numpy as np
import onnxruntime as ort
import sentencepiece as spm


class SummaryTransformer:
    ONNX_PROVIERS = ['CPUExecutionProvider']

    def __init__(self, text_preprocessor_file: str, model_state_dict_file: str):
        self.tokenizer = spm.SentencePieceProcessor(model_file=text_preprocessor_file)
        self.ort_sess = ort.InferenceSession(model_state_dict_file, providers=self.ONNX_PROVIERS)
    
    def generate(self, text: str, max_length=128):
        encoded_input = self.tokenizer.encode(text, add_eos=True)

        input_ids = np.expand_dims(np.array(encoded_input), axis=0)
        decoder_input_ids = np.expand_dims(np.array([self.tokenizer.pad_id()]), axis=0)

        outputs = self.ort_sess.run(None, { 'input_ids': input_ids, 'decoder_input_ids': decoder_input_ids })
        next_decoder_sequence, next_id = outputs[1], outputs[2]

        for _ in range(max_length):
            if int(next_id) == self.tokenizer.eos_id():
                break

            outputs = self.ort_sess.run(None, { 'input_ids': input_ids, 'decoder_input_ids': next_decoder_sequence })
            next_decoder_sequence, next_id = outputs[1], outputs[2]

        return self.tokenizer.decode(next_decoder_sequence[0].tolist())
