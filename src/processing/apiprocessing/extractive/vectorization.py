import re
import numpy as np

from typing import Union


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


def tf(__document: str, __vocab: np.ndarray = None, return_tokens=False) -> Union[tuple, np.ndarray]:
    doc_tokens = np.array(word_tokenize(__document))
    unique_tokens, token_counts = np.unique(doc_tokens, return_counts=True)

    if __vocab is None:
        freq = token_counts / len(doc_tokens)

        return (unique_tokens, freq) if return_tokens else freq
    else:
        tokens_tf = token_counts / len(doc_tokens)
        vocab_tf = unique_token_positional_matrix(unique_tokens, __vocab).T @ np.expand_dims(tokens_tf, axis=1)
        freq = np.squeeze(vocab_tf, axis=1)

        return (__vocab, freq) if return_tokens else freq


def __idf_for_words(__words: list, return_tokens=False):
    corpus_tokens = np.array(__words)
    unique_tokens, token_counts = np.unique(corpus_tokens, return_counts=True)

    N = len(corpus_tokens)
    inv_freq = np.log(N / (token_counts + 1))

    return (unique_tokens, inv_freq) if return_tokens else inv_freq


def idf(__corpus: str, return_tokens=False):
    return __idf_for_words(word_tokenize(__corpus), return_tokens)


def __tfidf_words_and_sentences(__words: list, __sentences: list):
    vocab = np.unique(__words)
    tfs = np.array([tf(sent, vocab) for sent in __sentences if len(sent) != 0])

    return tfs * np.expand_dims(__idf_for_words(__words), axis=0)


def tfidf(__corpus: str):
    sentences, words = sentence_tokenize(__corpus), word_tokenize(__corpus)

    return __tfidf_words_and_sentences(words, sentences)


def __calculate_sentence_scores(__corpus: str) -> str:
    corpus_frequencies = tfidf(__corpus)

    len_frequencies = np.sum(np.sign(corpus_frequencies), axis=1)
    return np.sum(corpus_frequencies, axis=1) / len_frequencies


def extractive_summary(__corpus: str, threshold: float = 1.0) -> str:
    sentences = sentence_tokenize(__corpus)
    sentence_scores = __calculate_sentence_scores(__corpus)

    mean_score = np.mean(sentence_scores)

    return " ".join([sentence for sentence, is_relevant_score
                     in zip(sentences, sentence_scores >= threshold * mean_score)
                     if is_relevant_score])


def extractive_summary_single_sentence(__corpus: str) -> str:
    sentences = sentence_tokenize(__corpus)
    sentence_scores = __calculate_sentence_scores(__corpus)
    top_score_index = np.argmax(sentence_scores)

    return sentences[top_score_index]
