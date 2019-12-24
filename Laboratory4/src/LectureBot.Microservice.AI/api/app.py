from flask import Flask, make_response, request
from api.settings.launch import SECRET

import math
import random

app = Flask(__name__)
app.secret_key = SECRET

denormalize_coefficient = 71046

GENERATING_SEED = random.random()

N_neurons_1 = 2
N_neurons_2 = 3
N_neurons_3 = 1

w1x = [[-1.1168175893607841, -0.6007507791876884, -1.2028397816557672],
       [-1.2216277149266128, -1.485808908860868, -1.1953925200354931],
       [-0.701533748909971, -0.8068347181943529, -0.6587955735056054]]

w2x = [[0.025289942329191697], [1.094625578260335], [1.166365699549035], [1.0732918766039488]]

layer1_out = [0., 0.]
layer2_out = [0., 0., 0.]
layer3_out = [0.]

y_output = [layer1_out, layer2_out, layer3_out]

lecture_size = 20


def y_model_sigmoid(x_sum):
    y_model = 1 / (1 + math.exp(- x_sum))
    return y_model


def normalize_inputs(input_str):
    num = 0

    for let in input_str:
        num += ord(let)

    return num / lecture_size


def find_word(vocab, index):
    word = ''

    for pair in vocab:
        if pair[0] == index:
            word = pair[1]
            break

    return word


def predict_next_index(x):
    x_test = [x[0] / denormalize_coefficient, x[1] / denormalize_coefficient]
    for i in range(0, N_neurons_1):
        y_output[0][i] = x_test[i]

    x_sum = 0
    for i in range(0, N_neurons_2):
        for j in range(0, len(w1x)):
            if j == 0:
                x_sum += 1 * w1x[j][i]
            else:
                x_sum += y_output[0][j - 1] * w1x[j][i]
        y_output[1][i] = y_model_sigmoid(x_sum)
        x_sum = 0

    for i in range(0, N_neurons_3):
        for j in range(0, len(w2x)):
            if j == 0:
                x_sum += 1 * w2x[j][i]
            else:
                x_sum += y_output[1][j - 1] * w2x[j][i]
        y_output[2][i] = y_model_sigmoid(x_sum)
        x_sum = 0

    return int(y_output[2][0] * denormalize_coefficient)


@app.route('/api/processText', methods=['POST'])
def process_text():
    vocaborary = []

    f = open('vocab', 'r')

    for i in range(denormalize_coefficient):
        pair = f.readline().split(',')
        pair[1] = pair[1].replace('\n', '')
        vocaborary.append(pair)

    f.close()

    theme = ""
    word_indexes = []

    try:
        theme = str(request.json['theme'])
    except Exception:
        return make_response(f"Wrong input type!", 400)

    current_prediction = normalize_inputs(theme)
    next_prediction = predict_next_index([GENERATING_SEED, current_prediction])

    word_indexes.append(next_prediction)

    for i in range(lecture_size):
        post_prediction = predict_next_index([current_prediction, next_prediction])
        word_indexes.append(post_prediction)

        current_prediction = next_prediction
        next_prediction = post_prediction

    words = [find_word(vocaborary, str(index)) for index in word_indexes]

    res = make_response(' '.join(words))
    return res, 200
