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

# Colors for across and down clues
colors = {
    "across": "#ffffff",  # White
    "down": "#d3d3d3"     # Light grey
}

# Map cell to clue type (across or down)
cell_clue_type = {}
for num, (r, c, length) in answers_across.items():
    for i in range(length):
        cell_clue_type[(r, c + i)] = "across"

for num, (r, c, length) in answers_across.items():
    for i in range(length):
        cell_clue_type[(r + i, c)] = "down"

# Function to render the crossword grid
def render_grid():
    for i, row in enumerate(grid):
        cols = st.columns(len(row))
        for j, cell in enumerate(row):
            if cell == 0:
                cols[j].markdown("<div style='background-color:black; width:50px; height:50px;'></div>", unsafe_allow_html=True)
            else:
                clue_type = cell_clue_type.get((i, j), "across")
                color = colors[clue_type]
                # input_value = ''
                # if (i, j) in pre_filled_letters:
                #     input_value = pre_filled_letters[(i, j)]
                # else:
                #     key = f"cell_{i}_{j}"
                #     input_value = st.text_input("", value="", max_chars=1, key=key)

                # Display the cell with small number and input
                cell_content = f"<div style='border:1px solid black; background-color:{color}; width:50px; height:50px; position:relative;'>"
                cell_content += f"<div style='position:absolute; top:0; left:0; font-size:10px; padding:2px;'>{cell}</div>"
                cell_content += f"<div style='display:flex; align-items:center; justify-content:center; height:100%;'>{input_value}</div>"
                cell_content += "</div>"

                cols[j].markdown(cell_content, unsafe_allow_html=True)

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
