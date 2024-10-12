import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Using v3 as it doesn't need a authentication
from googletrans import Translator

nltk.download('vader_lexicon')

def analyze_sentiment(text):

    # Translate Slovenian to English
    translator = Translator()
    translated_text = translator.translate(text, src='sl', dest='en').text

    # Perform sentiment analysis on the translated text
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(translated_text)
    sentiment = sentiment_scores['compound']

    if sentiment >= 0.05:
        return 'Positive'
    elif sentiment <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Example usage
text = input('Add Slovenian text: ')
sentiment = analyze_sentiment(text)
print(f'Sentiment: {sentiment}')