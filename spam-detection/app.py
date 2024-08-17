import streamlit as st
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
# Load the trained model and vectorizer
try:
    with open('model_spam.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
        
    with open('vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
except Exception as e:
    st.error(f"Error loading model or vectorizer: {str(e)}")
    st.stop()

# Function to predict if a message is spam or not
def predict_spam(message):
    try:
        # Transform the message using the vectorizer
        transformed_message = vectorizer.transform([message])
        # Predict using the loaded model
        prediction = model.predict(transformed_message)
        # Return "Spam" or "Not Spam" based on the prediction
        return "Spam" if prediction[0] == 1 else "Not Spam"
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return None

# Streamlit App
st.title("Spam Detection Tool")
st.write("Enter a message to check if it's spam or not:")

# User input area
user_input = st.text_area("Message:", height=150)

# Prediction logic
if st.button("Predict"):
    if user_input.strip():  # Check if input is not empty or just whitespace
        result = predict_spam(user_input)
        if result:
            st.write(f"Prediction: {result}")
    else:
        st.warning("Please enter a message to predict.")
