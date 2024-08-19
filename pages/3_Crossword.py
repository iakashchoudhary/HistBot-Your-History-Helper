import streamlit as st

# Define the crossword grid structure
grid = [
    [0, 0, 3, 0, 0, 0, 0],
    [0, 5, 0, 4, 0, 0, 0],
    [1, 0, 6, 0, 7, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0],
]

# Define the positions and lengths of the answers for each clue
answers_across = {
    3: (0, 2, 4),  # Start at (0,2), length 4
    5: (1, 1, 3),  # Start at (1,1), length 3
    7: (2, 4, 3)   # Start at (2,4), length 3
}

answers_down = {
    1: (2, 0, 3),  # Start at (2,0), length 3
    2: (4, 1, 3),  # Start at (4,1), length 3
    4: (1, 3, 3),  # Start at (1,3), length 3
    6: (2, 2, 3)   # Start at (2,2), length 3
}

# Clues for Across and Down sections
clues_across = {
    3: "Opposite of short",
    5: "Opposite of old",
    7: "Opposite of goodbye"
}

clues_down = {
    1: "Opposite of square",
    2: "Opposite of big",
    4: "Opposite of bad",
    6: "Opposite of black"
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

for num, (r, c, length) in answers_down.items():
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
                key = f"cell_{i}_{j}"
                input_value = st.text_input("", value="", max_chars=1, key=key)

                # Display the cell with small number and input
                cell_content = f"<div style='border:1px solid black; background-color:{color}; width:50px; height:50px; position:relative;'>"
                cell_content += f"<div style='position:absolute; top:0; left:0; font-size:10px; padding:2px;'>{cell}</div>"
                cell_content += f"<div style='display:flex; align-items:center; justify-content:center; height:100%;'>{input_value}</div>"
                cell_content += "</div>"

                cols[j].markdown(cell_content, unsafe_allow_html=True)

# Display the grid layout
st.title("Interactive Crossword Game")
render_grid()

# Input sections for Across and Down clues
st.subheader("Input your answers:")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Across")
    for num, clue in clues_across.items():
        st.text_input(f"{num}. {clue}")

with col2:
    st.subheader("Down")
    for num, clue in clues_down.items():
        st.text_input(f"{num}. {clue}")
