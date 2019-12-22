from flask import Flask, url_for, make_response, request
from api.settings.launch import SECRET

from tensorflow import keras

app = Flask(__name__)
app.secret_key = SECRET


@app.route('/api/processText', methods=['POST'])
def process_text():
    theme = ""

    new_model = keras.models.load_model('lectureBotAiModel.h5')

    try:
        theme = str(request.json['theme'])
    except Exception:
        return make_response(f"Wrong input type!", 400)

    #new_model.predict(theme)
    res = make_response(f"Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit amet consectetur adipisci[ng] velit, sed quia non numquam [do] eius modi tempora inci[di]dunt, ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit, qui in ea voluptate velit esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum fugiat, quo voluptas nulla pariatur?")
    return res, 200
