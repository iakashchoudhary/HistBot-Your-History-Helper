import random
import json
import pickle
import numpy as np
import nltk

nltk.download('punkt_tab')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
from keras.models import load_model

import streamlit as st
from streamlit_chat import message as st_message

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
# model = load_model('chatbot_model.h5')
model = load_model('chatbot_model.keras')

def clean_up_sentence(sentence):
    sentence = sentence.lower()
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

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

def get_response(intents_list, intents_json):
    if not intents_list:
        fallback_responses = ["I'm sorry, I didn't understand that.",
                              "Could you please rephrase that?",
                              "I'm not sure what you mean.",
                              "I currently don't have enough knowledge on that topic.",
                              "I'm having trouble understanding. Can you please rephrase your question?",
                              "I'm not trained on that content or knowledge. Is there anything else I can help you with?"]
        return random.choice(fallback_responses)
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def generate_user_random_seed():
    hair_types = ['bangs', 'bowlCutHair', 'braids', 'bunHair', 'curlyBob', 'curlyShortHair','froBun', 'halfShavedHead', 'mohawk', 'shavedHead', 'shortHair', 'straightHair', 'wavyBob']
    random_hair = random.choice(hair_types)
    seed = f'Leo&eyes=cheery&hair={random_hair}&hairColor=220f00&mouth=teethSmile&skinColor=efcc9f'
    return seed

def main():
    st.set_page_config(page_title="HistBot: Your History Helper", page_icon="📜")

    with st.sidebar:
        st.title("📜 HistBot")
        st.caption("### Explore history effortlessly with HistBot!")
        st.header("About")
        st.write(
            "📜 HistBot: Your History Helper is your virtual tutor for 4th-grade Maharashtra Board students 🎉\n\n"
            "This 🔧 tool is a ⚙️ work in progress."
        )
        st.write("---")
        st.header("Features")
        st.write(
            "Dive into Maharashtra's vibrant history with interactive lessons, quizzes, and stories.\n\n"
            "- 📚 Explore timelines from ancient wonders to modern marvels.\n\n"
            "- 🌟 Ask HistBot questions for clear answers.\n\n"
            "- 🏆 Unlock the fascinating world of Maharashtra's past!"
        )

    st.title("📜 HistBot")
    st.caption("### 🚀 Please use HistBot responsibly. Do not misuse it for inappropriate or harmful purposes.")
    
    if "greeting_displayed" not in st.session_state:
        st.session_state.greeting_displayed = False

    if not st.session_state.greeting_displayed:
        histbot_greeting = "Hello! I'm HistBot. How can I assist you today?"
        st.info(histbot_greeting)
        st.session_state.greeting_displayed = True

    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content="You are a very helpful assistant!")]

    prompt = st.chat_input("Message HistBot", key="prompt")

    if prompt:
        st.session_state.messages.append(HumanMessage(content=prompt))
        ints = predict_class(prompt)
        assistant_response = get_response(ints, intents)
        st.session_state.messages.append(AIMessage(content=assistant_response))

    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            if 'user_seed' not in st.session_state:
                st.session_state.user_seed = generate_user_random_seed()
            seed = st.session_state.user_seed
            st_message(msg.content, is_user=True, key=str(i) + '_user', avatar_style='big-smile', seed=seed)
        else:
            st_message(msg.content, is_user=False, key=str(i) + '_bot', avatar_style='bottts', seed='Leo&baseColor=00A6ED&eyes=frame1&face=round01&mouth[]&sides=cables01&texture=dots&top[]')

if __name__ == "__main__":
    main()
