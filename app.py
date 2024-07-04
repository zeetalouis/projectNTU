from flask import Flask, request, jsonify, render_template
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

app = Flask(__name__, static_url_path='/static', template_folder='templates')
analyzer = SentimentIntensityAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    message = data.get('message')
    sentiment_score = analyzer.polarity_scores(message)

    emotion = ''
    if sentiment_score['compound'] > 0.05:
        emotion = 'happy'
    elif sentiment_score['compound'] < -0.05:
        emotion = 'sad'
    else:
        emotion = 'neutral'

    return jsonify({'emotion': emotion})

if __name__ == '__main__':
    app.run(debug=True, port=8000)


