import random
import re
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Emotion and Swear Words Lexicons
emotion_words = {
    "happy": ["delicious", "great", "wonderful", "recommend", "nice", "good", "tasty", "flavorful", "excellent", "satisfying", 
              "mouthwatering", "superb", "amazing", "divine", "scrumptious", "tantalizing", "delectable", "delightful", "savory",
              "yummy", "succulent", "outstanding", "fabulous", "fantastic", "terrific", "phenomenal", "perfect", "top-notch", 
              "first-rate", "exceptional", "brilliant", "stellar", "impeccable", "wonderful", "exceptional", "five-star", "glorious",
              "splendid", "superior", "memorable", "joyful", "ecstatic", "elated", "cheerful", "thrilled", "content", "radiant", 
              "exuberant", "jubilant", "blissful", "euphoric", "overjoyed"],

    "sad": ["bland", "slow", "disappointing", "unclean", "not seasoned", "soggy", "bitter", "stale", "overpriced", "undercooked",
            "mediocre", "subpar", "forgettable", "lackluster", "below-average", "underwhelming", "boring", "dreary", "dismal", 
            "lousy", "upsetting", "unpleasant", "unsatisfactory", "dreadful", "poor", "miserable", "heartbreaking", "depressing", 
            "disheartening", "gloomy", "melancholy", "woeful", "tragic", "dispiriting", "regrettable", "unfulfilling", "uninspiring"],

    "mad": ["rude", "unprofessional", "poor", "bad", "unsanitary", "chaotic", "unorganized", "horrible", "awful", "terrible", 
            "outrageous", "infuriating", "frustrating", "enraging", "irritating", "exasperating", "annoying", "disruptive", 
            "offensive", "aggravating", "agitated", "incensed", "livid", "furious", "irate", "angry", "hostile", "fuming", 
            "indignant", "irate", "vehement", "rabid", "pissed off", "vexed", "maddening", "infuriated", "outraged", "incensed"],

    "disgusted": ["disgusting", "inedible", "unappetizing", "grimy", "gross", "unsanitary", "unhygienic", "appalling", "shoddy",
                  "cheaply-made", "horrendous", "revolting", "repulsive", "nauseating", "vile", "foul", "repugnant", "abhorrent",
                  "disdainful", "offensive", "repellent", "detestable", "noxious", "grotesque", "displeasing", "unpalatable", 
                  "off-putting", "distasteful", "horrible", "off-putting", "distasteful", "disagreeable", "horrible"],

    "fear": ["scared", "frightened", "afraid", "terrified", "panicked", "anxious", "worried", "nervous", "uneasy", "spooked",
             "alarmed", "dismayed", "horrified", "petrified", "intimidated", "threatened", "paranoid", "apprehensive", 
             "tense", "jittery", "timid", "hesitant", "shaken", "fearful", "daunted", "pensive", "anxious", "worried"],

    "surprised": ["surprised", "shocked", "astonished", "amazed", "stunned", "dumbfounded", "flabbergasted", "bewildered",
                  "taken aback", "startled", "disbelief", "unbelievable", "unexpected", "unforeseen", "jaw-dropping",
                  "mind-blowing", "eye-opening", "incredible", "astounding", "awe-inspiring", "unanticipated", "startling",
                  "unpredictable", "striking", "impressive", "extraordinary", "remarkable"]
}

swear_words = ["fuck", "shit", "bitch", "asshole", "damn", "crap", "bastard", "bloody", "bollocks", "wanker", "piss"]

def get_sentiment(text):
    # Analyze text for sentiment words based on emotion categories
    emotion_scores = {emotion: 0 for emotion in emotion_words}
    for word in text.split():
        for emotion, words in emotion_words.items():
            if word.lower() in words:
                emotion_scores[emotion] += 1
    return max(emotion_scores, key=emotion_scores.get)

def get_response(emotion):
    responses = {
        "happy": "The comment highlights a positive experience.",
        "sad": "The comment points out issues that need attention.",
        "mad": "The comment reflects frustration or anger.",
        "disgusted": "The comment expresses disgust.",
        "fear": "The comment expresses fear or concern.",
        "surprised": "The comment indicates surprise."
    }
    return responses[emotion]

def handle_greeting(message):
    greetings = ["hi", "hello", "hey", "greeting"]
    if any(greet in message.lower() for greet in greetings):
        responses = [
            "Hi! How can I help you?",
            "Hello! What brings you here today?",
            "Hey! How can I assist you?",
            "Greetings! What can I do for you?"
        ]
        return random.choice(responses)
    return None

def handle_swear_words(message):
    for word in swear_words:
        if re.search(r'\b{}\b'.format(word), message.lower()):
            return "I'm sorry, I can't assist with that."
    return None

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data.get('message')

    # Check for greetings
    greeting_response = handle_greeting(user_text)
    if greeting_response:
        return jsonify({"response": greeting_response})

    # Check for swear words
    swear_response = handle_swear_words(user_text)
    if swear_response:
        return jsonify({"response": swear_response})

    # Analyze sentiment
    emotion = get_sentiment(user_text)
    response = get_response(emotion)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
