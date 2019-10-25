from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

