import streamlit as st

# Define the crossword grid with pre-filled letters
grid = [
    [1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 1],
    [0, 1, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 1, 0],
    [1, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0, 1, 0, 0, 0],
]

# Define the solution and pre-filled letters
solution = [
    ['S', 'T', 0, 'C', 'R', 'O', 0, 'P', 'Y'],
    ['T', 0, 0, 'O', 0, 'A', 'P', 0, 'T'],
    ['R', 'E', 'A', 'M', 0, 'T', 0, 0, 'H'],
    [0, 'A', 0, 0, 'R', 'I', 'A', 'L', 'E'],
    ['L', 'I', 'T', 0, 'S', 0, 0, 'E', 0],
    ['E', 0, 0, 'H', 'O', 'U', 'S', 'E', 'S'],
    [0, 'A', 'S', 'E', 0, 'I', 0, 0, 0],
]

# Define clues for Across and Down sections
clues_across = {
    1: "High-level, general-purpose programming language.",
    4: "Tool for digging.",
    6: "Suffix indicating a profession.",
    7: "Command for Linux OS.",
    8: "Code repository platform."
}

clues_down = {
    1: "Unit of language that contains meaning.",
    2: "Common programming language for web development.",
    3: "Term for system memory.",
    5: "Red fruit.",
    6: "To stare intently."
}

# Initialize user input grid
user_input = [['' for _ in row] for row in grid]

# Title
st.title("Interactive Crossword Game")

# Display the crossword grid
for i, row in enumerate(grid):
    cols = st.columns(len(row))
    for j, cell in enumerate(row):
        if cell == 1:
            prefill = solution[i][j] if solution[i][j] else ''
            user_input[i][j] = cols[j].text_input("", value=prefill, max_chars=1, key=f"{i}-{j}")
        else:
            cols[j].markdown(f"<div style='background-color:black; width: 50px; height: 50px;'></div>", unsafe_allow_html=True)

# Across and Down Sections
st.subheader("Across")
for num, clue in clues_across.items():
    st.markdown(f"**{num}.** {clue}")

st.subheader("Down")
for num, clue in clues_down.items():
    st.markdown(f"**{num}.** {clue}")
