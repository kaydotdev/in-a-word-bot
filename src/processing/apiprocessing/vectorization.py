import re
import numpy as np


__re_word_tokenize = re.compile(r"(?u)\b\w[\w']*\b")
__re_sentence_tokenize = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s")
__token_is_predefined = np.vectorize(
    lambda token, predefined_tokens: float(token == predefined_tokens)
)


def word_tokenize(__text: str, to_lower: bool = True) -> list:
    return __re_word_tokenize.findall(__text.lower() if to_lower else __text)


def sentence_tokenize(__text: str) -> list:
    return __re_sentence_tokenize.split(__text)


def unique_token_positional_matrix(__tokens: np.ndarray, __vocab: np.ndarray) -> np.ndarray:
    return __token_is_predefined(__vocab, np.expand_dims(__tokens, axis=1))


def unique_token_positions(__tokens: np.ndarray, __vocab: np.ndarray) -> np.ndarray:
    return np.sum(unique_token_positional_matrix(__tokens, __vocab), axis=0)


def tf(__document: str, __vocab: np.ndarray = None) -> tuple:
    doc_tokens = np.array(word_tokenize(__document))
    unique_tokens, token_counts = np.unique(doc_tokens, return_counts=True)

    if __vocab is None:
        return unique_tokens, token_counts / len(doc_tokens)
    else:
        tokens_tf = token_counts / len(doc_tokens)
        vocab_tf = unique_token_positional_matrix(unique_tokens, __vocab).T @ np.expand_dims(tokens_tf, axis=1)

        return __vocab, np.squeeze(vocab_tf, axis=1)

