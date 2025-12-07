extends Node
## Input simulation for PlayGodot.
##
## Simulates mouse, keyboard, and touch input for automated testing.


## Simulate a click at coordinates.
func click(params: Dictionary) -> Dictionary:
	var x = params.get("x", 0.0)
	var y = params.get("y", 0.0)
	var button = params.get("button", "left")

	var button_index = _get_button_index(button)
	var pos = Vector2(x, y)

	# Move mouse
	_inject_mouse_motion(pos)
	await get_tree().process_frame

	# Click
	_inject_mouse_button(pos, button_index, true)
	await get_tree().process_frame
	_inject_mouse_button(pos, button_index, false)

	return {"result": {"clicked": true, "position": {"x": x, "y": y}}}


## Simulate a click on a node.
func click_node(params: Dictionary) -> Dictionary:
	var path = params.get("path", "")
	var button = params.get("button", "left")

	var node = get_tree().root.get_node_or_null(path)
	if node == null:
		return {"error": {"code": -32000, "message": "Node not found: " + path}}

	var pos = _get_node_center(node)
	if pos == null:
		return {"error": {"code": -32000, "message": "Cannot determine node position: " + path}}

	return await click({"x": pos.x, "y": pos.y, "button": button})


## Simulate a double-click at coordinates.
func double_click(params: Dictionary) -> Dictionary:
	var x = params.get("x", 0.0)
	var y = params.get("y", 0.0)

	await click({"x": x, "y": y})
	await get_tree().create_timer(0.1).timeout
	await click({"x": x, "y": y})

	return {"result": {"double_clicked": true}}


## Simulate a double-click on a node.
func double_click_node(params: Dictionary) -> Dictionary:
	var path = params.get("path", "")

	var node = get_tree().root.get_node_or_null(path)
	if node == null:
		return {"error": {"code": -32000, "message": "Node not found: " + path}}

	var pos = _get_node_center(node)
	if pos == null:
		return {"error": {"code": -32000, "message": "Cannot determine node position: " + path}}

	return await double_click({"x": pos.x, "y": pos.y})


## Move the mouse to coordinates.
func move_mouse(params: Dictionary) -> Dictionary:
	var x = params.get("x", 0.0)
	var y = params.get("y", 0.0)

	_inject_mouse_motion(Vector2(x, y))

	return {"result": {"position": {"x": x, "y": y}}}


## Simulate a drag operation.
func drag(params: Dictionary) -> Dictionary:
	var from_x = params.get("from_x", 0.0)
	var from_y = params.get("from_y", 0.0)
	var to_x = params.get("to_x", 0.0)
	var to_y = params.get("to_y", 0.0)
	var duration = params.get("duration", 0.5)

	var from_pos = Vector2(from_x, from_y)
	var to_pos = Vector2(to_x, to_y)
	var steps = max(10, int(duration * 60))

	# Move to start position
	_inject_mouse_motion(from_pos)
	await get_tree().process_frame

	# Press mouse button
	_inject_mouse_button(from_pos, MOUSE_BUTTON_LEFT, true)
	await get_tree().process_frame

	# Drag
	for i in range(steps):
		var t = float(i) / float(steps - 1)
		var pos = from_pos.lerp(to_pos, t)
		_inject_mouse_motion(pos)
		await get_tree().create_timer(duration / steps).timeout

	# Release mouse button
	_inject_mouse_button(to_pos, MOUSE_BUTTON_LEFT, false)

	return {"result": {"dragged": true}}


## Simulate a drag from one node to another.
func drag_node(params: Dictionary) -> Dictionary:
	var from_path = params.get("from_path", "")
	var to_path = params.get("to_path", "")
	var duration = params.get("duration", 0.5)

	var from_node = get_tree().root.get_node_or_null(from_path)
	var to_node = get_tree().root.get_node_or_null(to_path)

	if from_node == null:
		return {"error": {"code": -32000, "message": "From node not found: " + from_path}}
	if to_node == null:
		return {"error": {"code": -32000, "message": "To node not found: " + to_path}}

	var from_pos = _get_node_center(from_node)
	var to_pos = _get_node_center(to_node)

	if from_pos == null or to_pos == null:
		return {"error": {"code": -32000, "message": "Cannot determine node positions"}}

	return await drag({
		"from_x": from_pos.x,
		"from_y": from_pos.y,
		"to_x": to_pos.x,
		"to_y": to_pos.y,
		"duration": duration
	})


## Press a key.
func press_key(params: Dictionary) -> Dictionary:
	var key = params.get("key", "")
	var modifiers = params.get("modifiers", [])

	var keycode = _get_keycode(key)
	if keycode == KEY_NONE:
		return {"error": {"code": -32000, "message": "Unknown key: " + key}}

	# Press modifiers
	for mod in modifiers:
		var mod_keycode = _get_modifier_keycode(mod)
		if mod_keycode != KEY_NONE:
			_inject_key(mod_keycode, true)

	# Press and release key
	_inject_key(keycode, true)
	_inject_key(keycode, false)

	# Release modifiers
	for mod in modifiers:
		var mod_keycode = _get_modifier_keycode(mod)
		if mod_keycode != KEY_NONE:
			_inject_key(mod_keycode, false)

	return {"result": {"pressed": key}}


## Type a string of text.
func type_text(params: Dictionary) -> Dictionary:
	var text = params.get("text", "")
	var delay = params.get("delay", 0.05)

	for c in text:
		var event = InputEventKey.new()
		event.pressed = true
		event.unicode = c.unicode_at(0)
		Input.parse_input_event(event)

		event = InputEventKey.new()
		event.pressed = false
		event.unicode = c.unicode_at(0)
		Input.parse_input_event(event)

		await get_tree().create_timer(delay).timeout

	return {"result": {"typed": text}}


## Press an input action.
func press_action(params: Dictionary) -> Dictionary:
	var action = params.get("action", "")

	if not InputMap.has_action(action):
		return {"error": {"code": -32000, "message": "Action not found: " + action}}

	Input.action_press(action)
	await get_tree().process_frame
	Input.action_release(action)

	return {"result": {"pressed": action}}


## Hold an input action for a duration.
func hold_action(params: Dictionary) -> Dictionary:
	var action = params.get("action", "")
	var duration = params.get("duration", 0.0)

	if not InputMap.has_action(action):
		return {"error": {"code": -32000, "message": "Action not found: " + action}}

	Input.action_press(action)
	await get_tree().create_timer(duration).timeout
	Input.action_release(action)

	return {"result": {"held": action, "duration": duration}}


## Release an input action.
func release_action(params: Dictionary) -> Dictionary:
	var action = params.get("action", "")

	if not InputMap.has_action(action):
		return {"error": {"code": -32000, "message": "Action not found: " + action}}

	Input.action_release(action)

	return {"result": {"released": action}}


## Simulate a touch tap.
func tap(params: Dictionary) -> Dictionary:
	var x = params.get("x", 0.0)
	var y = params.get("y", 0.0)

	var pos = Vector2(x, y)

	var event = InputEventScreenTouch.new()
	event.position = pos
	event.pressed = true
	event.index = 0
	Input.parse_input_event(event)

	event = InputEventScreenTouch.new()
	event.position = pos
	event.pressed = false
	event.index = 0
	Input.parse_input_event(event)

	return {"result": {"tapped": true, "position": {"x": x, "y": y}}}


## Simulate a swipe gesture.
func swipe(params: Dictionary) -> Dictionary:
	var from_x = params.get("from_x", 0.0)
	var from_y = params.get("from_y", 0.0)
	var to_x = params.get("to_x", 0.0)
	var to_y = params.get("to_y", 0.0)
	var duration = params.get("duration", 0.3)

	var from_pos = Vector2(from_x, from_y)
	var to_pos = Vector2(to_x, to_y)
	var steps = max(10, int(duration * 60))

	# Touch start
	var event = InputEventScreenTouch.new()
	event.position = from_pos
	event.pressed = true
	event.index = 0
	Input.parse_input_event(event)

	# Drag
	for i in range(steps):
		var t = float(i) / float(steps - 1)
		var pos = from_pos.lerp(to_pos, t)

		var drag_event = InputEventScreenDrag.new()
		drag_event.position = pos
		drag_event.index = 0
		Input.parse_input_event(drag_event)

		await get_tree().create_timer(duration / steps).timeout

	# Touch end
	event = InputEventScreenTouch.new()
	event.position = to_pos
	event.pressed = false
	event.index = 0
	Input.parse_input_event(event)

	return {"result": {"swiped": true}}


## Simulate a pinch gesture.
func pinch(params: Dictionary) -> Dictionary:
	var center_x = params.get("center_x", 0.0)
	var center_y = params.get("center_y", 0.0)
	var scale = params.get("scale", 1.0)
	var duration = params.get("duration", 0.3)

	var center = Vector2(center_x, center_y)
	var initial_distance = 100.0
	var final_distance = initial_distance * scale
	var steps = max(10, int(duration * 60))

	# Start two touch points
	var pos1_start = center + Vector2(-initial_distance / 2, 0)
	var pos2_start = center + Vector2(initial_distance / 2, 0)
	var pos1_end = center + Vector2(-final_distance / 2, 0)
	var pos2_end = center + Vector2(final_distance / 2, 0)

	# Touch start
	for i in [0, 1]:
		var event = InputEventScreenTouch.new()
		event.position = pos1_start if i == 0 else pos2_start
		event.pressed = true
		event.index = i
		Input.parse_input_event(event)

	# Animate
	for step in range(steps):
		var t = float(step) / float(steps - 1)
		var pos1 = pos1_start.lerp(pos1_end, t)
		var pos2 = pos2_start.lerp(pos2_end, t)

		for i in [0, 1]:
			var drag_event = InputEventScreenDrag.new()
			drag_event.position = pos1 if i == 0 else pos2
			drag_event.index = i
			Input.parse_input_event(drag_event)

		await get_tree().create_timer(duration / steps).timeout

	# Touch end
	for i in [0, 1]:
		var event = InputEventScreenTouch.new()
		event.position = pos1_end if i == 0 else pos2_end
		event.pressed = false
		event.index = i
		Input.parse_input_event(event)

	return {"result": {"pinched": true, "scale": scale}}


# Helper functions

func _get_node_center(node: Node) -> Variant:
	if node is Control:
		# Use global_position + size/2 which works reliably in headless mode
		# get_global_rect() can return zeros before layout is calculated
		var pos = node.global_position
		var sz = node.size
		return pos + sz / 2.0
	elif node is CanvasItem:
		# For sprites and other 2D nodes
		if node.has_method("get_global_transform"):
			return node.get_global_transform().origin
	return null


func _get_button_index(button: String) -> MouseButton:
	match button.to_lower():
		"left":
			return MOUSE_BUTTON_LEFT
		"right":
			return MOUSE_BUTTON_RIGHT
		"middle":
			return MOUSE_BUTTON_MIDDLE
		_:
			return MOUSE_BUTTON_LEFT


func _inject_mouse_motion(pos: Vector2) -> void:
	var event = InputEventMouseMotion.new()
	event.position = pos
	event.global_position = pos
	Input.parse_input_event(event)


func _inject_mouse_button(pos: Vector2, button: MouseButton, pressed: bool) -> void:
	var event = InputEventMouseButton.new()
	event.position = pos
	event.global_position = pos
	event.button_index = button
	event.pressed = pressed
	Input.parse_input_event(event)


func _inject_key(keycode: Key, pressed: bool) -> void:
	var event = InputEventKey.new()
	event.keycode = keycode
	event.pressed = pressed
	Input.parse_input_event(event)


func _get_keycode(key: String) -> Key:
	match key.to_lower():
		"space", " ":
			return KEY_SPACE
		"enter", "return":
			return KEY_ENTER
		"escape", "esc":
			return KEY_ESCAPE
		"tab":
			return KEY_TAB
		"backspace":
			return KEY_BACKSPACE
		"delete":
			return KEY_DELETE
		"up":
			return KEY_UP
		"down":
			return KEY_DOWN
		"left":
			return KEY_LEFT
		"right":
			return KEY_RIGHT
		"home":
			return KEY_HOME
		"end":
			return KEY_END
		"pageup":
			return KEY_PAGEUP
		"pagedown":
			return KEY_PAGEDOWN
		"f1":
			return KEY_F1
		"f2":
			return KEY_F2
		"f3":
			return KEY_F3
		"f4":
			return KEY_F4
		"f5":
			return KEY_F5
		"f6":
			return KEY_F6
		"f7":
			return KEY_F7
		"f8":
			return KEY_F8
		"f9":
			return KEY_F9
		"f10":
			return KEY_F10
		"f11":
			return KEY_F11
		"f12":
			return KEY_F12
		_:
			# Single character
			if key.length() == 1:
				var code = key.to_upper().unicode_at(0)
				if code >= 65 and code <= 90:  # A-Z
					return code
				if code >= 48 and code <= 57:  # 0-9
					return code
			return KEY_NONE


func _get_modifier_keycode(mod: String) -> Key:
	match mod.to_lower():
		"ctrl", "control":
			return KEY_CTRL
		"shift":
			return KEY_SHIFT
		"alt":
			return KEY_ALT
		"meta", "cmd", "command":
			return KEY_META
		_:
			return KEY_NONE
