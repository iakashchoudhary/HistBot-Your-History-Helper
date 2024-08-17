import streamlit as st

# Define the crossword grid
grid = [
    [1, 1, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 1],
]

# Define the solution
solution = [
    ['C', 'A', 0, 'P', 'Y', 'T'],
    ['O', 0, 0, 'R', 0, 'H'],
    ['D', 'I', 'N', 'A', 'M', 'I'],
    [0, 'N', 0, 0, 'L', 0],
    ['S', 'T', 'R', 'E', 'A', 'M'],
    ['E', 0, 0, 'L', 'I', 'T'],
]

# Initialize the user input grid
user_input = [['' for _ in row] for row in grid]

st.title("Interactive Crossword Game")

# Create the crossword grid with Streamlit
for i, row in enumerate(grid):
    cols = st.columns(len(row))
    for j, cell in enumerate(row):
        if cell == 1:
            user_input[i][j] = cols[j].text_input("", value=user_input[i][j], max_chars=1, key=f"{i}-{j}")

# Check and highlight correct answers
for i, row in enumerate(grid):
    cols = st.columns(len(row))
    for j, cell in enumerate(row):
        if cell == 1:
            if user_input[i][j].upper() == solution[i][j]:
                cols[j].markdown(f"<span style='color: green; font-size: 24px;'>**{user_input[i][j].upper()}**</span>", unsafe_allow_html=True)
            elif user_input[i][j].strip():
                cols[j].markdown(f"<span style='color: red; font-size: 24px;'>**{user_input[i][j].upper()}**</span>", unsafe_allow_html=True)
            else:
                cols[j].markdown(f"<span style='color: black; font-size: 24px;'>_</span>", unsafe_allow_html=True)
