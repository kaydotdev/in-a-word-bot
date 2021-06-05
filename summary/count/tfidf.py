import nltk
import math

from collections import defaultdict

from nltk import sent_tokenize, word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
sw = set(stopwords.words("english"))


def tf_idf_summary(text: str) -> str:
    sentences = sent_tokenize(text)
    sentence_frequencies = {}

    for sent in sentences:
        freq_table = defaultdict(int)
        words = word_tokenize(sent)

        for word in words:
            word = lemmatizer.lemmatize(word.lower())

            if word not in sw:
                freq_table[word] += 1

        sentence_frequencies[sent] = freq_table

    tf_matrix = {}

    for sent, f_table in sentence_frequencies.items():
        tf_table = {}

        words_in_sent = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / words_in_sent

        tf_matrix[sent] = tf_table

    word_per_doc_table = defaultdict(int)

    for sent, f_table in sentence_frequencies.items():
        for word, count in f_table.items():
            word_per_doc_table[word] += 1

    idf_matrix = {}

    for sent, f_table in sentence_frequencies.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(len(sentences) / float(word_per_doc_table[word]))

        idf_matrix[sent] = idf_table

    tf_idf_matrix = {}

    for (tokens, tf_table), (_, idf_table) in zip(tf_matrix.items(), idf_matrix.items()):
        tf_idf_table = {}

        for (token, tf_value), (_, idf_value) in zip(tf_table.items(), idf_table.items()):
            tf_idf_table[token] = float(tf_value * idf_value)

        tf_idf_matrix[tokens] = tf_idf_table

    sentence_weights = {}

    for sentence, frequency in tf_idf_matrix.items():
        sentence_weights[sentence] = sum(frequency.values()) / len(frequency)

    threshold = sum(sentence_weights.values()) / len(sentence_weights)

    return " ".join([sentence for sentence in sentences
                     if sentence in sentence_weights and sentence_weights[sentence] >= threshold])
