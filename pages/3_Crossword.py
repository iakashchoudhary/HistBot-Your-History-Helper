import streamlit as st

# Define the crossword grid structure
grid = [
    [1, 1, 0, 2, 2, 2, 0, 3, 3],
    [4, 0, 0, 5, 0, 6, 6, 0, 7],
    [8, 9, 9, 10, 0, 11, 0, 0, 12],
    [0, 13, 0, 0, 14, 14, 14, 15, 15],
    [16, 17, 17, 0, 18, 0, 0, 19, 0],
    [20, 0, 0, 21, 21, 21, 21, 22, 22],
    [0, 23, 23, 24, 0, 25, 0, 0, 0],
]

# Define the pre-filled letters (clue letters)
pre_filled_letters = {
    (0, 1): 'T', (2, 0): 'R', (3, 4): 'R',
    (4, 1): 'I', (5, 5): 'U', (6, 3): 'E'
}

# Define the positions and lengths of the answers for each clue
answers_across = {
    1: (0, 0, 2),  # Start at (0,0), length 2
    2: (0, 3, 3),  # Start at (0,3), length 3
    3: (0, 7, 2),  # Start at (0,7), length 2
    4: (1, 0, 1),
    5: (1, 3, 1),
    6: (1, 5, 2),
    7: (1, 8, 1),
    8: (2, 0, 4),
    9: (2, 1, 2),
    10: (2, 3, 1),
    11: (2, 5, 1),
    12: (2, 8, 1),
    13: (3, 1, 1),
    14: (3, 4, 3),
    15: (3, 7, 2),
    16: (4, 0, 3),
    17: (4, 1, 2),
    18: (4, 4, 1),
    19: (4, 7, 1),
    20: (5, 0, 1),
    21: (5, 3, 4),
    22: (5, 7, 2),
    23: (6, 1, 2),
    24: (6, 3, 1),
    25: (6, 5, 1),
}

# Clues for Across and Down sections
clues_across = {
    1: "High-level, general-purpose programming language.",
    2: "Tool for digging.",
    3: "Suffix indicating a profession.",
    4: "Command for Linux OS.",
    5: "Code repository platform."
}

clues_down = {
    1: "Unit of language that contains meaning.",
    2: "Common programming language for web development.",
    3: "Term for system memory.",
    4: "Red fruit.",
    5: "To stare intently."
}

# Create inputs for Across and Down clues
st.subheader("Across")
across_answers = {}
for num, clue in clues_across.items():
    across_answers[num] = st.text_input(f"{num}. {clue}")

st.subheader("Down")
down_answers = {}
for num, clue in clues_down.items():
    down_answers[num] = st.text_input(f"{num}. {clue}")

# Function to render the crossword grid based on inputs
def render_grid():
    for i, row in enumerate(grid):
        cols = st.columns(len(row))
        for j, cell in enumerate(row):
            if cell == 0:
                cols[j].markdown("<div style='background-color:black; width:50px; height:50px;'></div>", unsafe_allow_html=True)
            else:
                input_value = ''
                if (i, j) in pre_filled_letters:
                    input_value = pre_filled_letters[(i, j)]
                else:
                    key = f"cell_{i}_{j}"
                    input_value = st.text_input("", value="", max_chars=1, key=key)
                
                cols[j].markdown(f"<div style='border:1px solid black; width:50px; height:50px; display:flex; align-items:center; justify-content:center;'>{input_value}</div>", unsafe_allow_html=True)

# Display the grid layout
st.title("Interactive Crossword Game")
render_grid()

# Display the clues
col1, col2 = st.columns(2)
with col1:
    st.subheader("Across")
    for num, clue in clues_across.items():
        st.markdown(f"**{num}.** {clue}")

with col2:
    st.subheader("Down")
    for num, clue in clues_down.items():
        st.markdown(f"**{num}.** {clue}")
