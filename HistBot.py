import random
import json
import pickle
import numpy as np
import nltk

from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import streamlit as st
from streamlit_chat import message as st_message
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# Initialize the WordNet lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents data from a JSON file
intents = json.loads(open('intents.json').read())

# Load preprocessed words, classes, and the trained model
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

# Define a function to clean up a sentence by tokenizing and lemmatizing
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# Define a function to convert a sentence into a bag of words representation
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Define a function to predict the class of a given sentence
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Define a function to get a response based on predicted intents
def get_response(intents_list, intents_json):
    if not intents_list:
        fallback_responses = ["I'm sorry, I didn't understand that.",
                              "Could you please rephrase that?",
                              "I'm not sure what you mean."]
        return random.choice(fallback_responses)
    
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def main():
    st.set_page_config(
        page_title="HistBot: Your History Helper",
        page_icon="📜",
    )

    with st.sidebar:
        st.markdown("# 👾 HistBot: Your History Helper")
        st.markdown("## About")
        st.markdown(
            "HistBot: Your History Helper is your virtual tutor for 4th-grade Maharashtra Board students 🎉\n\n"
        )
        st.markdown(
            "This 🔧 tool is a ⚙️ work in progress."
        )
        st.markdown("---")
        st.markdown("## Features")
        st.markdown(
            "Dive into Maharashtra's vibrant history with interactive lessons, quizzes, and stories.\n\n"
            "- 📚 Explore timelines from ancient wonders to modern marvels.\n\n"
            "- 🌟 Ask HistBot questions for clear answers.\n\n"
            "- 🏆 Unlock the fascinating world of Maharashtra's past!"
        )

    st.title("👾 HistBot")
    st.caption("🚀 Please use HistBot responsibly. Do not misuse it for inappropriate or harmful purposes.")

    if "greeting_displayed" not in st.session_state:
        st.session_state.greeting_displayed = False

    if not st.session_state.greeting_displayed:
        histbot_greeting = "Hello! I'm HistBot. How can I assist you today?"
        st.info(histbot_greeting)
        st.session_state.greeting_displayed = True

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a very helpful assistant!")
        ]

    prompt = st.chat_input("Message HistBot", key="prompt")

    if prompt:
        st.session_state.messages.append(HumanMessage(content=prompt))
        ints = predict_class(prompt)
        assistant_response = get_response(ints, intents)
        st.session_state.messages.append(AIMessage(content=assistant_response))

    messages = st.session_state.get('messages', [])

    for i, msg in enumerate(messages[1:]):  
        if i % 2 == 0:
            st_message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            st_message(msg.content, is_user=False, key=str(i) + '_bot')

if __name__ == "__main__":
    main()
