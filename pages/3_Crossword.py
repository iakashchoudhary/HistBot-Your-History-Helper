import streamlit as st

# Define the crossword grid with pre-filled letters and empty spaces
grid = [
    [1, 1, 0, 2, 2, 2, 0, 3, 3],
    [4, 0, 0, 5, 0, 6, 6, 0, 7],
    [8, 9, 9, 10, 0, 11, 0, 0, 12],
    [0, 13, 0, 0, 14, 14, 14, 15, 15],
    [16, 17, 17, 0, 18, 0, 0, 19, 0],
    [20, 0, 0, 21, 21, 21, 21, 22, 22],
    [0, 23, 23, 24, 0, 25, 0, 0, 0],
]

# Define the solution (correct answers)
solution = [
    ['S', 'T', 0, 'C', 'R', 'O', 0, 'P', 'Y'],
    ['T', 0, 0, 'O', 0, 'A', 'P', 0, 'T'],
    ['R', 'E', 'A', 'M', 0, 'T', 0, 0, 'H'],
    [0, 'A', 0, 0, 'R', 'I', 'A', 'L', 'E'],
    ['L', 'I', 'T', 0, 'S', 0, 0, 'E', 0],
    ['E', 0, 0, 'H', 'O', 'U', 'S', 'E', 'S'],
    [0, 'A', 'S', 'E', 0, 'I', 0, 0, 0],
]

# Clues for Across and Down sections
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

# Title
st.title("Interactive Crossword Game")

# Function to render the grid
def render_grid(grid, solution):
    for i, row in enumerate(grid):
        cols = st.columns(len(row))
        for j, cell in enumerate(row):
            if cell == 0:
                cols[j].markdown("<div style='background-color:black; width:50px; height:50px;'></div>", unsafe_allow_html=True)
            else:
                prefilled_letter = solution[i][j] if solution[i][j] else ''
                cols[j].text_input("", value=prefilled_letter, max_chars=1, key=f"{i}-{j}", help=f"Cell {i+1},{j+1}")

# Render the crossword grid
render_grid(grid, solution)

# Display the clues
st.subheader("Across")
for num, clue in clues_across.items():
    st.markdown(f"**{num}.** {clue}")

st.subheader("Down")
for num, clue in clues_down.items():
    st.markdown(f"**{num}.** {clue}")
