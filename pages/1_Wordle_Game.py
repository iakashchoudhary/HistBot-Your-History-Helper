import datetime
import re

import sqlite3

import streamlit as st

DB_FILE = "wordle.db"

def adapt_date(date):
    return date.isoformat()

sqlite3.register_adapter(datetime.date, adapt_date)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            username TEXT PRIMARY KEY UNIQUE NOT NULL,
            name TEXT NOT NULL,
            streak INTEGER,
            total_score INTEGER,
            last_played DATE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            username TEXT PRIMARY KEY UNIQUE NOT NULL,
            total_games INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            current_streak INTEGER DEFAULT 0,
            FOREIGN KEY (username) REFERENCES leaderboard (username) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def update_leaderboard(username, name, streak, score, reset_streak=False):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT last_played FROM leaderboard WHERE username = ?", (username,))
    row = cursor.fetchone()
    today = datetime.date.today()
    if row and row[0] == today.isoformat():
        conn.close()
        return
    if reset_streak:
        cursor.execute('''
            UPDATE leaderboard
            SET streak = 0, last_played = ?
            WHERE username = ?
        ''', (today, username))
    else:
        cursor.execute('''
            INSERT INTO leaderboard (username, name, streak, total_score, last_played)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET
                streak = excluded.streak,
                total_score = leaderboard.total_score + excluded.total_score,
                last_played = excluded.last_played
        ''', (username, name, streak, score, today))
    conn.commit()
    conn.close()

def update_statistics(username, won_game):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM statistics WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result:
        total_games, wins, losses, longest_streak, current_streak = result[1:]
        total_games += 1
        if won_game:
            wins += 1
            current_streak += 1
        else:
            losses += 1
            current_streak = 0
        if current_streak > longest_streak:
            longest_streak = current_streak
        cursor.execute('''UPDATE statistics SET total_games = ?, wins = ?, losses = ?, longest_streak = ?, current_streak = ? WHERE username = ?''',
                       (total_games, wins, losses, longest_streak, current_streak, username))
    else:
        cursor.execute('''INSERT INTO statistics (username, total_games, wins, losses, longest_streak, current_streak) VALUES (?, 1, ?, ?, ?, ?)''',
                       (username, 1 if won_game else 0, 1 if not won_game else 0, 1 if won_game else 0, 1 if won_game else 0))
    conn.commit()
    conn.close()

def get_leaderboard():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT leaderboard.name, leaderboard.streak, leaderboard.total_score, statistics.longest_streak
        FROM leaderboard
        JOIN statistics ON leaderboard.username = statistics.username
        ORDER BY leaderboard.total_score DESC
        LIMIT 5
    ''')
    data = cursor.fetchall()
    conn.close()
    return data

def get_user(username, name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT username, name, streak, total_score, last_played FROM leaderboard WHERE username = ?', (username,))
    result = cursor.fetchone()
    today = datetime.date.today()
    if result:
        user, name, streak, total_score, last_played = result
        if last_played:
            last_played_date = datetime.date.fromisoformat(last_played)
            if (today - last_played_date).days > 1:
                streak = 0
                cursor.execute("UPDATE leaderboard SET streak = 0 WHERE username = ?", (username,))
                cursor.execute("UPDATE statistics SET current_streak = 0 WHERE username = ?", (username,))
                conn.commit()
        else:
            last_played_date = None
        conn.close()
        return user, name, streak, total_score, last_played_date
    else:
        cursor.execute('INSERT INTO leaderboard (username, name, streak, total_score, last_played) VALUES (?, ?, 0, 0, ?)', (username, name, None))
        conn.commit()
        conn.close()
        return username, name, 0, 0, None

def get_statistics(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT total_games, wins, losses, longest_streak, current_streak FROM statistics WHERE username = ?', (username,))
    stats = cursor.fetchone()
    conn.close()
    return stats

word_list = ["forts", "medal", "relic", "coins", "india", "sword", "stone", "caste", "valor", "troop", "tombs", "honor", "armor", "rules", "kings", "march", "peace", "queen", "crown", "realm"]

def load_words(filename="words.txt"):
    with open(filename, "r") as file:
        return set(word.strip() for word in file.readlines())

valid_words = load_words()

def is_valid_guess(guess):
    return len(guess) == 5 and guess.lower() in valid_words

def get_daily_word(word_list):
    today = datetime.date.today()
    index = today.toordinal() % len(word_list)
    return word_list[index]

def check_guess(guess, correct_word):
    result = []
    for i in range(5):
        if guess[i] == correct_word[i]:
            result.append('🟩')
        elif guess[i] in correct_word:
            result.append('🟨')
        else:
            result.append('⬜')
    return result

def validate_username(username):
    return re.match("^[a-z0-9]+$", username) is not None

def validate_name(name):
    return re.match("^[A-Z][a-z]*( [A-Z][a-z]*)*$", name) is not None

init_db()

st.set_page_config(page_title="HistBot | Wordle Game", page_icon="🔠")
st.sidebar.title("🔠 HistBot: Wordle Game")
st.sidebar.caption("### A fun word guessing game!")

if 'username_entered' not in st.session_state:
    st.session_state.username_entered = False

if 'name_entered' not in st.session_state:
    st.session_state.name_entered = False

if 'is_username_valid' not in st.session_state:
    st.session_state.is_username_valid = False

if 'is_name_valid' not in st.session_state:
    st.session_state.is_name_valid = False

if not st.session_state.username_entered:
    username = st.sidebar.text_input("Enter your username:", placeholder=None, disabled=st.session_state.is_username_valid)

    if username:
        st.session_state.is_username_valid = validate_username(username)
        if not st.session_state.is_username_valid:
            st.sidebar.error("Invalid username! Only a-z, 0-9, and no spaces permitted.")
        else:
            st.session_state.username = username
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM leaderboard WHERE username = ?', (username,))
            existing_user = cursor.fetchone()
            conn.close()
            if existing_user:
                st.session_state.username_entered = True
                st.session_state.name = existing_user[0]
                st.sidebar.success(f"Welcome back, {st.session_state.name}!")
                st.session_state.is_name_valid = True
            else:
                if not st.session_state.name_entered:
                    name = st.sidebar.text_input("Enter your name:", placeholder=None, disabled=st.session_state.is_name_valid)
                    if name:
                        st.session_state.is_name_valid = validate_name(name)
                        if not st.session_state.is_name_valid:
                            st.sidebar.error("Invalid name! Use CamelCase with spaces.")
                        else:
                            st.session_state.username_entered = True
                            st.session_state.name_entered = True
                            st.session_state.name = name
                            st.sidebar.success(f"Welcome, {st.session_state.name}!")
                    else:
                        st.sidebar.warning("Not registered. Please enter your name to begin!")
    else:
        st.sidebar.warning("Please enter your username to begin!")
else:
    if st.session_state.name_entered:
        st.sidebar.success(f"Welcome, {st.session_state.name}!")
    else:
        st.sidebar.success(f"Welcome back, {st.session_state.name}!")

st.sidebar.markdown("---")

st.sidebar.header("How to Play Wordle")
st.sidebar.write(""" 
1. Guess the correct 5-letter word within 6 tries. 
2. Each guess must be a valid 5-letter word. 
3. Feedback: 
   - 🟩: Correct letter and position 
   - 🟨: Correct letter, wrong position 
   - ⬜: Not in the word 
4. Use the feedback to improve your next guess! 
""")

st.title("🔠 Wordle Game")
st.caption("## Welcome to the 🔤 Wordle game! 🤔 Try to guess the word!")

st.write("### 🌐 Leaderboard")
st.write("Check out the top players!")
leaderboard_data = get_leaderboard()
if leaderboard_data:
    leaderboard_list = [
        {
            "Rank": i + 1,
            "Name": name + (" 👑" if i == 0 else " 🥈" if i == 1 else " 🥉" if i == 2 else ""),
            "Current Streak": streak,
            "Longest Streak": longest_streak,
            "Total Score": total_score
        } 
        for i, (name, streak, total_score, longest_streak) in enumerate(leaderboard_data)
    ]
    st.dataframe(leaderboard_list)
else:
    st.write("No entries yet.")

st.info("🔍 **Note:** Please read the rules of Wordle before entering your username.")

st.write("---")

if st.session_state.is_username_valid and st.session_state.is_name_valid:
    user, fullname, user_streak, total_score, last_played = get_user(st.session_state.username, st.session_state.name)
    today = datetime.date.today()
    stats = get_statistics(st.session_state.username)
    if stats:
        st.markdown(f"<h3 style='color: #4CAF50;'>Welcome back, <strong>{fullname}</strong>!</h3>", unsafe_allow_html=True)
        total_games, wins, losses, longest_streak, current_streak = stats
        winning_percentage = (wins / total_games * 100) if total_games > 0 else 0

        with st.container():
            st.markdown("<h4 style='color: #007BFF;'>Your Statistics:</h4>", unsafe_allow_html=True)
            data = {
                "Total Games Played": [total_games],
                "Wins": [wins],
                "Losses": [losses],
                "Current Streak": [current_streak],
                "Longest Streak": [longest_streak],
                "Total Score": [total_score],
                "Winning Percentage": [f"{winning_percentage:.2f}%"]
            }
            df = st.dataframe(data)
    else:
        st.markdown(f"<h3 style='color: #4CAF50;'>Welcome, <strong>{fullname}</strong>!</h3>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: #FF5722;'>No statistics available. Play a game to start tracking!</h4>", unsafe_allow_html=True)
    
    st.write("---")

    if last_played == today:
        if user_streak == 0:
            st.error("You've played your game for today! Come back tomorrow, and let's turn that streak around together!")
        else:
            st.success(f"You've already played today! With a streak of {user_streak}, come back tomorrow and see if you can keep it going!")
        st.stop()

    if "streak" not in st.session_state:
        st.session_state.streak = user_streak
        st.session_state.score = 0
        st.session_state.guesses = []
        st.session_state.attempts = 0
        st.session_state.correct_word = get_daily_word(word_list)
        st.session_state.completed = False
    
    success_message_placeholder = st.empty()
    error_message_placeholder = st.empty()

    st.write("### 🤔 Ready for a challenge? Guess the hidden word!")

    attempts_left_html = f"<div style='text-align: right; margin-top: 20px; font-size: 20px;'><b>Attempts left:</b> {5 - st.session_state.attempts}</div>"
    st.markdown(attempts_left_html, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    grid_html = "<div style='display: flex; flex-direction: column; gap: 4px; align-items: center;'>"
    for i in range(5):
        grid_html += "<div style='display: flex; gap: 4px;'>"
        if i < len(st.session_state.guesses):
            guess_row = st.session_state.guesses[i]
            result = check_guess(guess_row, st.session_state.correct_word)
            for j, letter in enumerate(guess_row):
                color = "#9e9e9e"
                if result[j] == '🟩':
                    color = "#90EE90"
                elif result[j] == '🟨':
                    color = "#FFD700"
                grid_html += f"<div style='width: 50px; height: 50px; background-color: {color}; border: 2px solid black; display: flex; justify-content: center; align-items: center; font-size: 24px; border-radius: 5px;'>{letter.upper()}</div>"
        else:
            for _ in range(5):
                grid_html += "<div style='width: 50px; height: 50px; background-color: #ffffff; border: 2px solid black; display: flex; justify-content: center; align-items: center; font-size: 24px; border-radius: 5px;'></div>"
        grid_html += "</div>"
    grid_html += "</div>"

    st.markdown(grid_html, unsafe_allow_html=True)

    st.write("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])

    with col1:
        guess = st.text_input("Enter your guess:", max_chars=5, key="guess_input").lower()

    with col2:
        st.markdown("""
            <style>
                .stButton > button {
                    width: 130px;
                    margin-top:12px;
                }
            </style>
        """, unsafe_allow_html=True)
        submit_guess = st.button("Submit Guess", key="submit_guess")

    if submit_guess and guess:
        if not is_valid_guess(guess):
            st.warning("Invalid word! Please enter a valid 5-letter word.")
        elif guess in st.session_state.guesses:
            st.warning("You've already guessed that word!")
        else:
            st.session_state.guesses.append(guess)
            st.session_state.attempts += 1
            
            feedback_result = check_guess(guess, st.session_state.correct_word)
            
            feedback_letters = []
            for i in range(5):
                letter = guess[i]
                if feedback_result[i] == '🟩':
                    feedback_letters.append((letter, "#90EE90"))
                elif feedback_result[i] == '🟨':
                    feedback_letters.append((letter, "#FFD700"))
                else:
                    feedback_letters.append((letter, "#9e9e9e"))
            grid_html = "<div style='display: flex; justify-content: center; gap: 4px;'>"
            for letter, color in feedback_letters:
                grid_html += f"<div style='width: 50px; height: 50px; background-color: {color}; border: 2px solid black; display: flex; justify-content: center; align-items: center; font-size: 24px; border-radius: 5px;'>{letter.upper()}</div>"
            grid_html += "</div>"
            st.markdown(grid_html, unsafe_allow_html=True)

            if guess == st.session_state.correct_word:
                success_message_placeholder.success("🎉 Congratulations! You guessed the word!")
                st.session_state.streak += 1
                st.session_state.score += 7 - st.session_state.attempts
                st.session_state.completed = True
                update_leaderboard(st.session_state.username, st.session_state.name, st.session_state.streak, st.session_state.score)
                update_statistics(st.session_state.username, won_game=True)
            elif st.session_state.attempts >= 6:
                error_message_placeholder.error(f"You've run out of attempts! The correct word was: {st.session_state.correct_word}")
                st.session_state.completed = True
                update_leaderboard(st.session_state.username, st.session_state.name, st.session_state.streak, st.session_state.score, reset_streak=True)
                update_statistics(st.session_state.username, won_game=False)
