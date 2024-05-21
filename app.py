from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def init_board():
    return [' ' for _ in range(9)]

board = init_board()
player = "X"

def check_win():
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
        (0, 4, 8), (2, 4, 6)              # Diagonal
    ]
    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=['POST'])
def move():
    global player
    index = int(request.json['index'])
    if board[index] == ' ':
        board[index] = player
        winner = check_win()
        player = 'O' if player == 'X' else 'X'
        return jsonify({"move": index, "player": board[index], "winner": winner})
    return jsonify({"move": None})

@app.route("/reset", methods=['POST'])
def reset():
    global board, player
    board = init_board()
    player = "X"
    return jsonify({"message": "Board reset."})

if __name__ == "__main__":
    app.run(debug=True)
