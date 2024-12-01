import streamlit as st
import nltk

import string
import random
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from PyPDF2 import PdfReader
from docx import Document

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')

lemmatizer = nltk.stem.WordNetLemmatizer()
stop_words = set(nltk.corpus.stopwords.words('english'))

default_file_path = 'knowledge.txt'
def load_default_text():
    with open(default_file_path, 'r', encoding='UTF-8', errors='ignore') as file:
        text = file.read().lower()
    return text

default_text = load_default_text()
default_lines = default_text.splitlines()
default_sent_tokens = [nltk.sent_tokenize(line) for line in default_lines]

def lemmatize_normalize(text):
    return [lemmatizer.lemmatize(token) for token in nltk.word_tokenize(text.lower()) if token not in stop_words and token not in string.punctuation]

def read_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        return " ".join([page.extract_text() for page in reader.pages])
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        st.error("Unsupported file type. Please upload a .txt, .pdf, or .docx file.")
        return None

def response(user_response, tfidf, lines_with_sentences):
    time.sleep(1)
    user_response = user_response.lower()
    flattened_sentences = [sentence for line in lines_with_sentences for sentence in line]  # Flatten nested list for processing
    flattened_sentences.append(user_response)
    tfidf_matrix = tfidf.fit_transform(flattened_sentences)
    vals = cosine_similarity(tfidf_matrix[-1], tfidf_matrix)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    flattened_sentences.pop(-1)

    if req_tfidf == 0:
        fallback_responses = ["I'm sorry, I didn't understand that.",
                              "Could you please rephrase that?",
                              "I'm not sure what you mean.",
                              "I currently don't have enough knowledge on that topic.",
                              "I'm having trouble understanding. Can you please rephrase your question?"]
        return random.choice(fallback_responses)
    else:
        line_idx = 0
        sentence_idx = 0
        sentence_count = 0
        for i, line in enumerate(lines_with_sentences):
            if sentence_count + len(line) > idx:
                line_idx = i + 1
                sentence_idx = idx - sentence_count + 1
                break
            sentence_count += len(line)
        return f"{flattened_sentences[idx]} (Line {line_idx}, Sentence {sentence_idx})"

def generate_user_random_seed():
    seed_1 = 'assets\bigSmileBoy.png'
    seed_2 = 'assets\bigSmileGirl.png'
    selected_seed = random.choice([seed_1, seed_2])
    return selected_seed

def main():
    st.set_page_config(page_title="HistBot | CiteGen AI", page_icon="📖")
    
    with st.sidebar:
        st.title("📖 CiteGen AI")
        st.caption("### Explore, ask, and discover with CiteGen AI.")
        st.header("About")
        st.write(
            "📖 **CiteGen AI** lets you explore documents intelligently. Upload your documents to ask questions and get accurate answers with citations. If no document is uploaded, CiteGen AI uses its built-in knowledge base.\n\n"
            "This 🔧 tool is a ⚙️ work in progress."
        )
        st.write("---")
        st.header("How to use")
        st.write(
            "1. 📤 Upload a .txt, .pdf, or .docx file.\n"
            "2. ❓ Ask a question about the content of the document.\n"
            "3. 📖 If no document is uploaded, CiteGen AI will respond using its default knowledge base.\n"
            "4. ✨ Explore the generative capabilities by asking open-ended questions to get insightful responses."
        )
        st.write("---")
        st.header("Features")
        st.write(
            "- 📄 **Document Upload:** Seamlessly upload your documents for in-depth analysis.\n"
            "- 📝 **Citation Support:** Get answers backed by citations from your documents.\n"
            "- 🤖 **Generative Responses:** Engage with the AI for narrative generation and insights.\n"
            "- 🌟 **User-Friendly Interface:** Designed for ease of use for all users."
        )

    st.title("📖 CiteGen AI")
    st.caption("### 🚀 Please use CiteGen AI responsibly. Do not misuse it for inappropriate or harmful purposes.")

    if "greeting_displayed" not in st.session_state:
        st.session_state.greeting_displayed = False
    
    if "ask_messages" not in st.session_state:
        st.session_state.ask_messages = []

    if not st.session_state.greeting_displayed:
        histbot_greeting = "Hello! I'm CiteGen AI. How can I assist you today?"
        st.info(histbot_greeting)
        st.session_state.greeting_displayed = True

    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])
    
    if uploaded_file is not None:
        raw_text = read_file(uploaded_file)
        if raw_text:
            sent_tokens = [nltk.sent_tokenize(raw_text)]
            if "warning_displayed" in st.session_state:
                del st.session_state.warning_displayed
        else:
            if "warning_displayed" not in st.session_state:
                st.warning("The uploaded file is empty. Please upload a non-empty file or use the default knowledge base.")
                st.session_state.warning_displayed = True
            sent_tokens = default_sent_tokens
    else:
        sent_tokens = default_sent_tokens

    tfidf = TfidfVectorizer(tokenizer=lemmatize_normalize, token_pattern=None)
    tfidf.fit_transform([sentence for line in sent_tokens for sentence in line])

    if 'seed' not in st.session_state:
        st.session_state.seed = generate_user_random_seed()
    seed = st.session_state.seed

    for message in st.session_state.ask_messages:
        avatar = seed if message["role"] == "user" else 'assets\bottts.png'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if (prompt := st.chat_input("Ask a question")):
        st.session_state.ask_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=seed):
            st.markdown(prompt)
        
        if "warning_displayed" in st.session_state:
            del st.session_state.warning_displayed
        
        with st.chat_message("assistant", avatar='assets\bottts.png'):
            message_placeholder = st.empty()
            with st.spinner("HistBot is thinking..."):
                assistant_response = response(prompt, tfidf, sent_tokens)

        full_response = ""
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.ask_messages.append({"role": "assistant", "content": full_response})

    col1, col2 = st.columns([9, 1])
    with col2:
        st.button("Clear", key="clear_chat", disabled=len(st.session_state.ask_messages) == 0, on_click=lambda: st.session_state.ask_messages.clear())

if __name__ == "__main__":
    main()
