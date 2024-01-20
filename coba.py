import tkinter as tk

BOARD_SIZE = 3
CELL_SIZE = 100

X_SYMBOL = "X"
O_SYMBOL = "O"

X_COLOR = "blue"
O_COLOR = "red"
BG_COLOR = "white"

root = tk.Tk()
root.title("Tic Tac Toe")

canvas = tk.Canvas(root, width=CELL_SIZE * BOARD_SIZE, height=CELL_SIZE * BOARD_SIZE)
canvas.pack()

cells = []

player = tk.StringVar(root)
player.set(X_SYMBOL)

label = tk.Label(root, textvariable=player)
label.pack()

button = tk.Button(root, text="Restart", command=lambda: restart())
button.pack()

winner_text = canvas.create_text(CELL_SIZE * BOARD_SIZE / 2, CELL_SIZE * BOARD_SIZE / 2, text="", font="Times 20 bold")

def draw_board():
    for i in range(1, BOARD_SIZE):
        canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
    for i in range(1, BOARD_SIZE):
        canvas.create_line(0, i * CELL_SIZE, BOARD_SIZE * CELL_SIZE, i * CELL_SIZE)

def draw_symbol(row, col, symbol):
    x = col * CELL_SIZE + CELL_SIZE / 2
    y = row * CELL_SIZE + CELL_SIZE / 2
    if symbol == X_SYMBOL:
        canvas.create_line(x - 25, y - 25, x + 25, y + 25, fill=X_COLOR, width=4)
        canvas.create_line(x + 25, y - 25, x - 25, y + 25, fill=X_COLOR, width=4)
    elif symbol == O_SYMBOL:
        canvas.create_oval(x - 25, y - 25, x + 25, y + 25, outline=O_COLOR, width=4)

def click(event):
    x = event.x
    y = event.y
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    symbol = player.get()
    if cells[row][col] == "" and not game_over():
        draw_symbol(row, col, symbol)
        cells[row][col] = symbol
        if symbol == X_SYMBOL:
            player.set(O_SYMBOL)
        elif symbol == O_SYMBOL:
            player.set(X_SYMBOL)
        winner = check_winner() # Check the winner after each move
        if winner:
            label.config(text=f"{winner} wins!")
            highlight_winner(winner) # Highlight the winning cells
            canvas.unbind("<Button-1>") # Disable further clicks
            canvas.itemconfig(winner_text, text=f"{winner} wins!") # Update the text object
        elif is_board_full():
            label.config(text="It's a tie!")
            canvas.unbind("<Button-1>") # Disable further clicks
            canvas.itemconfig(winner_text, text="It's a tie!") # Update the text object

def game_over():
    # Return True if there is a winner or a tie, False otherwise
    return check_winner() or is_board_full()

def check_winner():
    # Return the symbol of the winner, or None if there is no winner
    for i in range(BOARD_SIZE):
        if cells[i][0] == cells[i][1] == cells[i][2] != "":
            return cells[i][0]
    for i in range(BOARD_SIZE):
        if cells[0][i] == cells[1][i] == cells[2][i] != "":
            return cells[0][i]
    if cells[0][0] == cells[1][1] == cells[2][2] != "":
        return cells[0][0]
    if cells[0][2] == cells[1][1] == cells[2][0] != "":
        return cells[0][2]
    return None

def highlight_winner(winner):
    # Highlight the cells that form the winning combination
    if winner == X_SYMBOL:
        color = X_COLOR
    elif winner == O_SYMBOL:
        color = O_COLOR
    else:
        return
    for i in range(BOARD_SIZE):
        if cells[i][0] == cells[i][1] == cells[i][2] == winner:
            canvas.itemconfig(i * BOARD_SIZE, fill=color)
            canvas.itemconfig(i * BOARD_SIZE + 1, fill=color)
            canvas.itemconfig(i * BOARD_SIZE + 2, fill=color)
    for i in range(BOARD_SIZE):
        if cells[0][i] == cells[1][i] == cells[2][i] == winner:
            canvas.itemconfig(i, fill=color)
            canvas.itemconfig(i + BOARD_SIZE, fill=color)
            canvas.itemconfig(i + 2 * BOARD_SIZE, fill=color)
    if cells[0][0] == cells[1][1] == cells[2][2] == winner:
        canvas.itemconfig(0, fill=color)
        canvas.itemconfig(4, fill=color)
        canvas.itemconfig(8, fill=color)
    if cells[0][2] == cells[1][1] == cells[2][0] == winner:
        canvas.itemconfig(2, fill=color)
        canvas.itemconfig(4, fill=color)
        canvas.itemconfig(6, fill=color)

def is_board_full():
    # Return True if the board is full, False otherwise
    for row in cells:
        if "" in row:
            return False
    return True

# Define a function to restart the game
def restart():
    # Clear the board cells
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            cells[i][j] = ""
    # Clear the canvas
    canvas.delete("all")
    # Draw the board
    draw_board()
    # Reset the player to X
    player.set(X_SYMBOL)
    # Reset the label to show the current player
    label.config(textvariable=player)

for i in range(BOARD_SIZE):
    cells.append([])
    for j in range(BOARD_SIZE):
        cells[i].append("")

canvas.bind("<Button-1>", click)

draw_board()

root.mainloop()