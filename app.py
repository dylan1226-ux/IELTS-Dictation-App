from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

basic_words = pd.read_csv('/Users/dylanpan/Documents/GitHub/IELTS-Dictation-App/IELTS_vocab/words_basic.csv')
advanced_words = pd.read_csv('/Users/dylanpan/Documents/GitHub/IELTS-Dictation-App/IELTS_vocab/words_advanced.csv')

basic_words['code'] = basic_words['code'].astype(int)
advanced_words['code'] = advanced_words['code'].astype(int)


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

    return render_template('practice.html', words=word_code_translation_pairs, word_list=word_list)


@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    words = request.form
    word_list = request.form['word_list']  # Get the word_list value from the form

    result = []

    # Iterate over each submitted answer
    for code, user_input in words.items():
        # Skip the hidden field 'word_list'
        if code == 'word_list':
            continue

        # Fetch the correct word row based on whether it's from the basic or advanced list
        if word_list == 'basic':
            word_row = basic_words[basic_words['code'] == int(code)]
        else:
            word_row = advanced_words[advanced_words['code'] == int(code)]

        correct_word = word_row['word'].values[0]
        chinese_translation = word_row['translation'].values[0]
        is_correct = user_input.strip().lower() == correct_word.strip().lower()

        result.append((code, user_input, correct_word, chinese_translation,is_correct))

    return render_template('results.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)