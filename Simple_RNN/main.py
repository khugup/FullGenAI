import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import sequence

word_index=imdb.get_word_index()
reverse_word={value:key for key,value  in word_index.items()}


#  Load the pre trained model with Reu activation
model=load_model('simple_rnn_imdb.h5')

# Function to decode reviews
def decode_review(encoded_review):
    return ' '.join([reverse_word_.get(i-3,'?') for i in encoded_review])

# Function to preprocess user input
def preprocess_text(text):
    words=text.lower().split()
    encoded_review=[word_index.get(word,2)+3 for word in words]
    padded_review=sequence.pad_sequences([encoded_review],maxlen=500)
    return padded_review

# Step -3
def predict_sentiment(review):
    preprocessed_input=preprocess_text(review)
    pediction=model.predict(preprocessed_input)
    sentiment='Positive' if pediction[0][0] >0.5 else 'Negative'
    return sentiment, pediction[0][0]

# Step-4 : User input and prediction
# Example review for prediction
example_review='This movie was fabolous'
sentiment,score=predict_sentiment(example_review)
print(f"Review: {example_review}")
print(f"Sentiment: {sentiment}")
print(f"Score: {score}")




# Streamlit app
import streamlit as st
st.title('IMDB movie review sentiment analysis')
st.write('Enter a movie to classify it as a positive or negative')


# User input
user_input=st.text_area('Movie Review')
if st.button('Classify'):
    preprocessed_input=preprocess_text(user_input)
    
    # Make prediction
    prediction=model.predict(preprocessed_input)
    sentiment='Positive' if prediction[0][0]>0.5 else 'Negative'
    
    # Display the result
    st.write(f'Sentiment: {sentiment}')
    st.write(f'Prediction review: {prediction[0][0]}')
else:
    print("Enter the movie review")    