import streamlit as st
import numpy as np
import nltk
import string
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Define lemmatizer and stopwords
lemmatizer = nltk.stem.WordNetLemmatizer()
stop_words = set(nltk.corpus.stopwords.words('english'))

# Function to lemmatize and normalize text
def lemmatize_normalize(text):
    return [lemmatizer.lemmatize(token) for token in nltk.word_tokenize(text.lower()) if token not in stop_words and token not in string.punctuation]

# Function to get response
def response(user_response, tfidf, sent_tokens):
    user_response = user_response.lower()
    sent_tokens.append(user_response)
    tfidf_matrix = tfidf.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
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
        page_title="HistBot | Ask Doc",
        page_icon="📜",
    )

    with st.sidebar:
        st.markdown("# 📖 HistBot: Ask Doc")
        st.markdown(
            "## How to use\n"
            "1. Upload a .txt 📄 file. (Currently we don't support PDF & Doc)\n"
            "2. Ask a question about the document.\n"
        )
        st.markdown("---")
        st.markdown("## About")
        st.markdown(
            "📖 HistBot: Ask Doc allows you to ask questions about your "
            "documents and get accurate answers with instant citations. "
        )
        st.markdown(
            "This tool is a 🔧 work in progress. "
        )

    st.title("📖 Ask Doc")
    st.caption("🚀 Please use Ask Doc responsibly. Do not misuse it for inappropriate or harmful purposes.")

    if "greeting_displayed" not in st.session_state:
        st.session_state.greeting_displayed = False

    if not st.session_state.greeting_displayed:
        histbot_greeting = "Hello! I'm HistBot. How can I assist you today?"
        st.info(histbot_greeting)
        st.session_state.greeting_displayed = True

    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file is not None:
        raw_text = uploaded_file.read().decode("utf-8")
        sent_tokens = nltk.sent_tokenize(raw_text)

        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(tokenizer=lemmatize_normalize, stop_words='english')
        tfidf_matrix = tfidf.fit_transform(sent_tokens)

        if "ask_messages" not in st.session_state:
            st.session_state.ask_messages = []

        for message in st.session_state.ask_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if (prompt := st.chat_input("Ask a question")):
            st.session_state.ask_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("HistBot is thinking..."):
                full_response = response(prompt, tfidf, sent_tokens)
                with st.chat_message("assistant"):
                    st.markdown(full_response)
                st.session_state.ask_messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
