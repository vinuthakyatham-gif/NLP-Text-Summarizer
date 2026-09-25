# from flask import Flask, render_template, request, redirect, url_for, session
# from nltk.tokenize import sent_tokenize

# app = Flask(__name__)
# app.secret_key = 'admin'  # For session handling


# def summarize_text(text, num_sentences=3):
#     sentences = sent_tokenize(text)
#     return sentences[:min(num_sentences, len(sentences))]


# @app.route('/')
# def index():
#     return redirect(url_for('login'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username == 'admin' and password == 'admin':
#             session['user'] = username
#             return redirect(url_for('home'))
#         else:
#             return render_template('login.html', error='Invalid credentials')
#     return render_template('login.html')


# @app.route('/home')
# def home():
#     if 'user' not in session:
#         return redirect(url_for('login'))
#     return render_template('home.html')


# @app.route('/summarizer', methods=['GET', 'POST'])
# def summarizer():
#     if 'user' not in session:
#         return redirect(url_for('login'))

#     output_summary = []
#     original_text = ""
#     if request.method == 'POST':
#         original_text = request.form.get('input_text')
#         num_sentences = int(request.form.get('num_sentences', 3))
#         output_summary = summarize_text(original_text, num_sentences)

#     return render_template('summarizer.html', output_summary=output_summary, original_text=original_text)


# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect(url_for('login'))


# if __name__ == '__main__':
#     import nltk
#     nltk.download('punkt')  # Ensure tokenizer is downloaded
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from nltk.tokenize import sent_tokenize
import nltk

app = Flask(__name__)
app.secret_key = 'admin'  # For session handling


# ✅ Ensure required NLTK data is available (only downloads if missing)
def download_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')

    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        nltk.download('punkt_tab')


# Call once at startup
download_nltk_resources()


def summarize_text(text, num_sentences=3):
    if not text:
        return []

    sentences = sent_tokenize(text)

    # Handle edge cases safely
    num_sentences = max(1, min(num_sentences, len(sentences)))

    return sentences[:num_sentences]


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'admin':
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/summarizer', methods=['GET', 'POST'])
def summarizer():
    if 'user' not in session:
        return redirect(url_for('login'))

    output_summary = []
    original_text = ""

    if request.method == 'POST':
        original_text = request.form.get('input_text', '')
        
        try:
            num_sentences = int(request.form.get('num_sentences', 3))
        except ValueError:
            num_sentences = 3

        output_summary = summarize_text(original_text, num_sentences)

    return render_template(
        'summarizer.html',
        output_summary=output_summary,
        original_text=original_text
    )


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)