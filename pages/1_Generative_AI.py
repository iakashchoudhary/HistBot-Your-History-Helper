import streamlit as st
import numpy as np
import nltk
import string
import time
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK resources
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('stopwords')

# Load the dataset
file_path = 'knowledge.txt'
with open(file_path, 'r', encoding='UTF-8', errors='ignore') as file:
    dataset = file.read()

# Preprocess the dataset
dataset = dataset.lower()
sent_tokens = nltk.sent_tokenize(dataset)

# Define lemmatizer and stopwords
lemmatizer = nltk.stem.WordNetLemmatizer()
stop_words = set(nltk.corpus.stopwords.words('english'))

# Function to lemmatize and normalize text
def lemmatize_normalize(text):
    return [lemmatizer.lemmatize(token) for token in nltk.word_tokenize(text.lower()) if token not in stop_words and token not in string.punctuation]

# Function to get response
def response(user_response):
    user_response = user_response.lower()
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=lemmatize_normalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    sent_tokens.pop(-1)
    if req_tfidf == 0:
        fallback_responses = ["I'm sorry, I didn't understand that.",
                              "Could you please rephrase that?",
                              "I'm not sure what you mean.",
                              "I currently don't have enough knowledge on that topic.",
                              "I'm having trouble understanding. Can you please rephrase your question?",
                              "I'm not trained on that content or knowledge. Is there anything else I can help you with?"]
        return random.choice(fallback_responses)
    else:
        return sent_tokens[idx]

# Streamlit app
def main():
    st.set_page_config(
        page_title="HistBot | Generative AI",
        page_icon="📜",
    )

    with st.sidebar:
        st.markdown("# 🧠 HistBot: Generative AI")
        st.markdown("## About")
        st.markdown(
            "🧠 HistBot: Generative AI delves into history using cutting-edge AI. It crafts accurate narratives, timelines, and scenarios by analyzing vast datasets.\n\n"
            "From pivotal 📊 moments to alternate histories, HistBot sparks curiosity and provides engaging content for history buffs and scholars. 📜✨"
        )
        st.markdown(
            "This tool is a ⚙️ work in progress."
        )
        st.markdown("---")
        st.markdown(
            "## How to use\n"
            "1. Just randomly 🎲 type any sentences.\n"
            "2. It will respond with generative thoughts 🤖✨ based on the model's knowledge.\n"
        )

    st.title("🧠 Generative AI")
    st.caption("🚀 Please use HistBot responsibly. Do not misuse it for inappropriate or harmful purposes.")

    if "generative_ai_messages" not in st.session_state:
        st.session_state.generative_ai_messages = []

    if "greeting_displayed" not in st.session_state:
        st.session_state.greeting_displayed = False

    if not st.session_state.greeting_displayed:
        histbot_greeting = "Hello! I'm HistBot. How can I assist you today?"
        st.info(histbot_greeting)
        st.session_state.greeting_displayed = True

    for message in st.session_state.generative_ai_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if (prompt := st.chat_input("Message HistBot")):
        st.session_state.generative_ai_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = response(prompt)
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.generative_ai_messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
