extends Control
## Main game controller for Tic Tac Toe
##
## Handles game state, player turns, win detection, and UI updates.

signal game_ended(winner: String)
signal turn_changed(player: String)

enum CellState { EMPTY, X, O }

const WINNING_COMBINATIONS := [
	[0, 1, 2],  # Top row
	[3, 4, 5],  # Middle row
	[6, 7, 8],  # Bottom row
	[0, 3, 6],  # Left column
	[1, 4, 7],  # Middle column
	[2, 5, 8],  # Right column
	[0, 4, 8],  # Diagonal top-left to bottom-right
	[2, 4, 6],  # Diagonal top-right to bottom-left
]

var board: Array[CellState] = []
var current_player: CellState = CellState.X
var game_active: bool = true
var moves_count: int = 0

@onready var grid_container: GridContainer = $VBoxContainer/GameBoard/GridContainer
@onready var status_label: Label = $VBoxContainer/StatusLabel
@onready var restart_button: Button = $VBoxContainer/RestartButton


func _ready() -> void:
	print("[TicTacToe] Game initialized")
	_initialize_board()
	_connect_signals()
	_update_status()


func _initialize_board() -> void:
	board.clear()
	board.resize(9)
	for i in range(9):
		board[i] = CellState.EMPTY
	print("[TicTacToe] Board initialized with 9 empty cells")


func _connect_signals() -> void:
	restart_button.pressed.connect(_on_restart_pressed)

	# Connect cell buttons
	for i in range(grid_container.get_child_count()):
		var cell := grid_container.get_child(i) as Button
		if cell:
			cell.pressed.connect(_on_cell_pressed.bind(i))


func _on_cell_pressed(index: int) -> void:
	if not game_active:
		print("[TicTacToe] Game not active, ignoring cell press")
		return

	if board[index] != CellState.EMPTY:
		print("[TicTacToe] Cell %d already occupied" % index)
		return

	# Make the move
	board[index] = current_player
	moves_count += 1
	_update_cell_display(index)

	var player_symbol := "X" if current_player == CellState.X else "O"
	print("[TicTacToe] Player %s placed at cell %d" % [player_symbol, index])

	# Check for winner
	var winner := _check_winner()
	if winner != CellState.EMPTY:
		_end_game(winner)
		return

	# Check for draw
	if moves_count >= 9:
		_end_game(CellState.EMPTY)
		return

	# Switch player
	current_player = CellState.O if current_player == CellState.X else CellState.X
	turn_changed.emit("X" if current_player == CellState.X else "O")
	_update_status()


func _update_cell_display(index: int) -> void:
	var cell := grid_container.get_child(index) as Button
	if cell:
		match board[index]:
			CellState.X:
				cell.text = "X"
				cell.add_theme_color_override("font_color", Color("#e74c3c"))
			CellState.O:
				cell.text = "O"
				cell.add_theme_color_override("font_color", Color("#3498db"))
			CellState.EMPTY:
				cell.text = ""


func _check_winner() -> CellState:
	for combo in WINNING_COMBINATIONS:
		var a: int = combo[0]
		var b: int = combo[1]
		var c: int = combo[2]

		if board[a] != CellState.EMPTY and board[a] == board[b] and board[b] == board[c]:
			print("[TicTacToe] Winning combination found: %s" % str(combo))
			return board[a]

	return CellState.EMPTY


func _end_game(winner: CellState) -> void:
	game_active = false

	match winner:
		CellState.X:
			status_label.text = "Player X Wins!"
			print("[TicTacToe] Game ended - X wins!")
			game_ended.emit("X")
		CellState.O:
			status_label.text = "Player O Wins!"
			print("[TicTacToe] Game ended - O wins!")
			game_ended.emit("O")
		CellState.EMPTY:
			status_label.text = "It's a Draw!"
			print("[TicTacToe] Game ended - Draw!")
			game_ended.emit("Draw")


func _update_status() -> void:
	if game_active:
		var player := "X" if current_player == CellState.X else "O"
		status_label.text = "Player %s's Turn" % player


func _on_restart_pressed() -> void:
	print("[TicTacToe] Restarting game...")
	_initialize_board()
	current_player = CellState.X
	game_active = true
	moves_count = 0

	# Clear all cells
	for i in range(grid_container.get_child_count()):
		var cell := grid_container.get_child(i) as Button
		if cell:
			cell.text = ""

	_update_status()
	print("[TicTacToe] Game restarted")


## Get current board state as array of strings (for testing/automation)
func get_board_state() -> Array[String]:
	var state: Array[String] = []
	for cell in board:
		match cell:
			CellState.X:
				state.append("X")
			CellState.O:
				state.append("O")
			_:
				state.append("")
	return state


## Make a move programmatically (for testing/automation)
func make_move(index: int) -> bool:
	if not game_active or index < 0 or index > 8:
		return false
	if board[index] != CellState.EMPTY:
		return false

	_on_cell_pressed(index)
	return true


## Check if game is still active
func is_game_active() -> bool:
	return game_active


## Get current player symbol
func get_current_player() -> String:
	return "X" if current_player == CellState.X else "O"
