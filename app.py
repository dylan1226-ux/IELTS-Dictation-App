from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


basic_words = pd.read_csv('words_basic.csv')
advanced_words = pd.read_csv('words_advanced.csv')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_practice', methods=['POST'])
def start_practice():
    word_list = request.form['list']
    start_code, end_code = map(int, request.form['range'].split('-'))

    # Select the word list
    if word_list == 'basic':
        words = basic_words[(basic_words['code'] >= start_code) & (basic_words['code'] <= end_code)]
    else:
        words = advanced_words[(advanced_words['code'] >= start_code) & (advanced_words['code'] <= end_code)]

    word_code_translation_pairs = [(row['code'], row['translation']) for _, row in words.iterrows()]

    return render_template('practice.html', words=word_code_translation_pairs)


@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    words = request.form
    result = []

    # collect user input
    for code, user_input in words.items():
        word_row = basic_words[basic_words['code'] == int(code)] if int(code) in basic_words['code'].values else \
            advanced_words[advanced_words['code'] == int(code)]

        correct_word = word_row['word'].values[0]
        chinese_translation = word_row['translation'].values[0]
        result.append((code, user_input, correct_word, chinese_translation))

    return render_template('results.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
