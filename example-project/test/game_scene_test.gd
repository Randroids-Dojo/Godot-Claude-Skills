## Integration tests for the Tic Tac Toe game scene.
##
## These tests use the Scene Runner to simulate user input.
## Run with: godot --headless -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd --run-tests
extends GdUnitTestSuite

var runner: GdUnitSceneRunner


func before_test() -> void:
	runner = scene_runner("res://scenes/main.tscn")


func after_test() -> void:
	runner.free()


func test_scene_loads() -> void:
	await runner.await_idle_frame()

	var game = runner.scene()
	assert_that(game).is_not_null()
	assert_that(game.is_game_active()).is_true()


func test_click_center_cell() -> void:
	await runner.await_idle_frame()

	# Find the center cell (Cell4)
	var cell = runner.find_child("Cell4")
	assert_that(cell).is_not_null()

	# Click the cell
	var cell_center = cell.global_position + cell.size / 2
	runner.set_mouse_position(cell_center)
	runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)
	await runner.await_input_processed()

	# Verify X was placed
	var game = runner.scene()
	assert_that(game.get_board_state()[4]).is_equal("X")


func test_two_players_alternate() -> void:
	await runner.await_idle_frame()

	# X clicks cell 0
	var cell0 = runner.find_child("Cell0")
	runner.set_mouse_position(cell0.global_position + cell0.size / 2)
	runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)
	await runner.await_input_processed()

	# O clicks cell 4
	var cell4 = runner.find_child("Cell4")
	runner.set_mouse_position(cell4.global_position + cell4.size / 2)
	runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)
	await runner.await_input_processed()

	# Verify both moves
	var game = runner.scene()
	var state = game.get_board_state()
	assert_that(state[0]).is_equal("X")
	assert_that(state[4]).is_equal("O")


func test_clicking_occupied_cell_does_nothing() -> void:
	await runner.await_idle_frame()

	var cell = runner.find_child("Cell0")
	var cell_center = cell.global_position + cell.size / 2

	# First click - X
	runner.set_mouse_position(cell_center)
	runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)
	await runner.await_input_processed()

	# Second click on same cell - should still be X
	runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)
	await runner.await_input_processed()

	var game = runner.scene()
	assert_that(game.get_board_state()[0]).is_equal("X")
	# Should still be O's turn since X's second click was invalid
	assert_that(game.get_current_player()).is_equal("O")


func test_restart_button_resets_game() -> void:
	await runner.await_idle_frame()

	# Make some moves
	var cell0 = runner.find_child("Cell0")
	runner.set_mouse_position(cell0.global_position + cell0.size / 2)
	runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)
	await runner.await_input_processed()

	var cell4 = runner.find_child("Cell4")
	runner.set_mouse_position(cell4.global_position + cell4.size / 2)
	runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)
	await runner.await_input_processed()

	# Click restart button
	var restart_btn = runner.find_child("RestartButton")
	runner.set_mouse_position(restart_btn.global_position + restart_btn.size / 2)
	runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)
	await runner.await_input_processed()

	# Verify game was reset
	var game = runner.scene()
	assert_that(game.is_game_active()).is_true()
	assert_that(game.get_current_player()).is_equal("X")

	var state = game.get_board_state()
	for cell_state in state:
		assert_that(cell_state).is_equal("")


func test_win_ends_game() -> void:
	await runner.await_idle_frame()

	# Play X winning in top row: 0, 1, 2
	# O plays: 3, 4
	var cells = ["Cell0", "Cell3", "Cell1", "Cell4", "Cell2"]

	for cell_name in cells:
		var cell = runner.find_child(cell_name)
		runner.set_mouse_position(cell.global_position + cell.size / 2)
		runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)
		await runner.await_input_processed()

	# Game should be over
	var game = runner.scene()
	assert_that(game.is_game_active()).is_false()


func test_status_label_updates() -> void:
	await runner.await_idle_frame()

	var status_label = runner.find_child("StatusLabel")
	assert_that(status_label).is_not_null()

	# Initial state should show X's turn
	assert_that(status_label.text).contains("X")

	# After X moves, should show O's turn
	var cell = runner.find_child("Cell0")
	runner.set_mouse_position(cell.global_position + cell.size / 2)
	runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)
	await runner.await_input_processed()

	assert_that(status_label.text).contains("O")
