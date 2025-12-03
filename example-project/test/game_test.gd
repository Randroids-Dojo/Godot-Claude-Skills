## Unit tests for the Tic Tac Toe game logic.
##
## Run with: godot --headless -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd --run-tests
extends GdUnitTestSuite

const GameScript = preload("res://scripts/game.gd")

var game: Control


func before_test() -> void:
	# Create a fresh game instance for each test
	game = auto_free(GameScript.new())


func test_initial_state_is_x_turn() -> void:
	assert_that(game.get_current_player()).is_equal("X")


func test_initial_state_game_active() -> void:
	assert_that(game.is_game_active()).is_true()


func test_initial_board_is_empty() -> void:
	var state := game.get_board_state()
	assert_that(state).has_size(9)
	for cell in state:
		assert_that(cell).is_equal("")


func test_make_valid_move() -> void:
	var success := game.make_move(4)  # Center cell
	assert_that(success).is_true()

	var state := game.get_board_state()
	assert_that(state[4]).is_equal("X")


func test_make_move_switches_player() -> void:
	game.make_move(0)  # X plays
	assert_that(game.get_current_player()).is_equal("O")

	game.make_move(1)  # O plays
	assert_that(game.get_current_player()).is_equal("X")


func test_cannot_move_to_occupied_cell() -> void:
	game.make_move(4)  # X takes center
	var success := game.make_move(4)  # O tries same cell
	assert_that(success).is_false()

	# Player should still be O (move failed)
	assert_that(game.get_current_player()).is_equal("O")


func test_invalid_move_negative_index() -> void:
	var success := game.make_move(-1)
	assert_that(success).is_false()


func test_invalid_move_out_of_bounds() -> void:
	var success := game.make_move(9)
	assert_that(success).is_false()


func test_x_wins_top_row() -> void:
	# X: 0, 1, 2 (top row)
	# O: 3, 4
	game.make_move(0)  # X
	game.make_move(3)  # O
	game.make_move(1)  # X
	game.make_move(4)  # O
	game.make_move(2)  # X wins

	assert_that(game.is_game_active()).is_false()


func test_o_wins_diagonal() -> void:
	# X: 1, 2, 5
	# O: 0, 4, 8 (diagonal)
	game.make_move(1)  # X
	game.make_move(0)  # O
	game.make_move(2)  # X
	game.make_move(4)  # O
	game.make_move(5)  # X
	game.make_move(8)  # O wins

	assert_that(game.is_game_active()).is_false()


func test_draw_game() -> void:
	# Fill board without winner:
	# X O X
	# X X O
	# O X O
	game.make_move(0)  # X
	game.make_move(1)  # O
	game.make_move(2)  # X
	game.make_move(5)  # O
	game.make_move(3)  # X
	game.make_move(6)  # O
	game.make_move(4)  # X
	game.make_move(8)  # O
	game.make_move(7)  # X - draw

	assert_that(game.is_game_active()).is_false()


func test_cannot_move_after_game_over() -> void:
	# X wins quickly
	game.make_move(0)  # X
	game.make_move(3)  # O
	game.make_move(1)  # X
	game.make_move(4)  # O
	game.make_move(2)  # X wins

	# Try to make another move
	var success := game.make_move(5)
	assert_that(success).is_false()


func test_win_detection_all_rows() -> void:
	# Test middle row win
	var game2 := auto_free(GameScript.new())
	game2.make_move(3)  # X
	game2.make_move(0)  # O
	game2.make_move(4)  # X
	game2.make_move(1)  # O
	game2.make_move(5)  # X wins middle row
	assert_that(game2.is_game_active()).is_false()

	# Test bottom row win
	var game3 := auto_free(GameScript.new())
	game3.make_move(6)  # X
	game3.make_move(0)  # O
	game3.make_move(7)  # X
	game3.make_move(1)  # O
	game3.make_move(8)  # X wins bottom row
	assert_that(game3.is_game_active()).is_false()


func test_win_detection_all_columns() -> void:
	# Left column
	var game2 := auto_free(GameScript.new())
	game2.make_move(0)  # X
	game2.make_move(1)  # O
	game2.make_move(3)  # X
	game2.make_move(2)  # O
	game2.make_move(6)  # X wins left column
	assert_that(game2.is_game_active()).is_false()

	# Middle column
	var game3 := auto_free(GameScript.new())
	game3.make_move(1)  # X
	game3.make_move(0)  # O
	game3.make_move(4)  # X
	game3.make_move(2)  # O
	game3.make_move(7)  # X wins middle column
	assert_that(game3.is_game_active()).is_false()

	# Right column
	var game4 := auto_free(GameScript.new())
	game4.make_move(2)  # X
	game4.make_move(0)  # O
	game4.make_move(5)  # X
	game4.make_move(1)  # O
	game4.make_move(8)  # X wins right column
	assert_that(game4.is_game_active()).is_false()


func test_win_detection_diagonals() -> void:
	# Top-left to bottom-right diagonal
	var game2 := auto_free(GameScript.new())
	game2.make_move(0)  # X
	game2.make_move(1)  # O
	game2.make_move(4)  # X
	game2.make_move(2)  # O
	game2.make_move(8)  # X wins diagonal
	assert_that(game2.is_game_active()).is_false()

	# Top-right to bottom-left diagonal
	var game3 := auto_free(GameScript.new())
	game3.make_move(2)  # X
	game3.make_move(0)  # O
	game3.make_move(4)  # X
	game3.make_move(1)  # O
	game3.make_move(6)  # X wins anti-diagonal
	assert_that(game3.is_game_active()).is_false()
