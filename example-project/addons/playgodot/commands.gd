extends Node
## Command handlers for PlayGodot automation.
##
## Implements the JSON-RPC methods that can be called from external clients.

const InputSimulator = preload("res://addons/playgodot/input_simulator.gd")
const Screenshot = preload("res://addons/playgodot/screenshot.gd")

var _server: Node = null
var _input_simulator: InputSimulator = null
var _screenshot: Screenshot = null


func _init(server: Node) -> void:
	_server = server


func _ready() -> void:
	_input_simulator = InputSimulator.new()
	add_child(_input_simulator)

	_screenshot = Screenshot.new()
	add_child(_screenshot)


## Execute a command and return the result.
func execute(method: String, params: Dictionary) -> Dictionary:
	match method:
		# Node operations
		"get_node":
			return _get_node(params)
		"get_property":
			return _get_property(params)
		"set_property":
			return _set_property(params)
		"call_method":
			return _call_method(params)
		"node_exists":
			return _node_exists(params)
		"query_nodes":
			return _query_nodes(params)
		"count_nodes":
			return _count_nodes(params)
		"get_children":
			return _get_children(params)

		# Input operations
		"click":
			return await _input_simulator.click(params)
		"click_node":
			return await _input_simulator.click_node(params)
		"double_click":
			return await _input_simulator.double_click(params)
		"double_click_node":
			return await _input_simulator.double_click_node(params)
		"move_mouse":
			return _input_simulator.move_mouse(params)
		"drag":
			return await _input_simulator.drag(params)
		"drag_node":
			return await _input_simulator.drag_node(params)
		"press_key":
			return _input_simulator.press_key(params)
		"type_text":
			return await _input_simulator.type_text(params)
		"press_action":
			return await _input_simulator.press_action(params)
		"hold_action":
			return await _input_simulator.hold_action(params)
		"release_action":
			return _input_simulator.release_action(params)
		"tap":
			return _input_simulator.tap(params)
		"swipe":
			return await _input_simulator.swipe(params)
		"pinch":
			return await _input_simulator.pinch(params)

		# Screenshot operations
		"screenshot":
			return await _screenshot.capture(params)

		# Waiting operations
		"wait_signal":
			return await _wait_signal(params)
		"wait_frames":
			return await _wait_frames(params)
		"wait_seconds":
			return await _wait_seconds(params)

		# Scene operations
		"get_current_scene":
			return _get_current_scene()
		"change_scene":
			return _change_scene(params)
		"reload_scene":
			return _reload_scene()
		"get_tree":
			return _get_tree_structure()

		# Game state
		"pause":
			return _pause()
		"unpause":
			return _unpause()
		"set_time_scale":
			return _set_time_scale(params)

		_:
			return {"error": {"code": -32601, "message": "Method not found: " + method}}


# Node operations

func _get_node(params: Dictionary) -> Dictionary:
	var path = params.get("path", "")
	var node = get_tree().root.get_node_or_null(path)

	if node == null:
		return {"error": {"code": -32000, "message": "Node not found: " + path}}

	return {"result": _serialize_node(node)}


func _serialize_node(node: Node) -> Dictionary:
	var data = {
		"path": str(node.get_path()),
		"name": node.name,
		"class": node.get_class(),
	}

	# Add common properties
	if node is Node2D:
		data["position"] = {"x": node.position.x, "y": node.position.y}
		data["rotation"] = node.rotation
		data["scale"] = {"x": node.scale.x, "y": node.scale.y}
		data["visible"] = node.visible
	elif node is Control:
		data["position"] = {"x": node.position.x, "y": node.position.y}
		data["size"] = {"x": node.size.x, "y": node.size.y}
		data["visible"] = node.visible
	elif node is Node3D:
		data["position"] = {"x": node.position.x, "y": node.position.y, "z": node.position.z}
		data["visible"] = node.visible

	return data


func _get_property(params: Dictionary) -> Dictionary:
	var path = params.get("path", "")
	var property = params.get("property", "")

	var node = get_tree().root.get_node_or_null(path)
	if node == null:
		return {"error": {"code": -32000, "message": "Node not found: " + path}}

	var value = node.get(property)
	return {"result": {"value": _serialize_value(value)}}


func _serialize_value(value: Variant) -> Variant:
	if value is Vector2:
		return {"x": value.x, "y": value.y}
	elif value is Vector3:
		return {"x": value.x, "y": value.y, "z": value.z}
	elif value is Color:
		return {"r": value.r, "g": value.g, "b": value.b, "a": value.a}
	elif value is Object:
		if value.has_method("get_path"):
			return str(value.get_path())
		return str(value)
	else:
		return value


func _set_property(params: Dictionary) -> Dictionary:
	var path = params.get("path", "")
	var property = params.get("property", "")
	var value = params.get("value")

	var node = get_tree().root.get_node_or_null(path)
	if node == null:
		return {"error": {"code": -32000, "message": "Node not found: " + path}}

	# Deserialize special types
	value = _deserialize_value(value, node.get(property))

	node.set(property, value)
	return {"result": {"success": true}}


func _deserialize_value(value: Variant, current: Variant) -> Variant:
	if current is Vector2 and value is Dictionary:
		return Vector2(value.get("x", 0), value.get("y", 0))
	elif current is Vector3 and value is Dictionary:
		return Vector3(value.get("x", 0), value.get("y", 0), value.get("z", 0))
	elif current is Color and value is Dictionary:
		return Color(value.get("r", 0), value.get("g", 0), value.get("b", 0), value.get("a", 1))
	return value


func _call_method(params: Dictionary) -> Dictionary:
	var path = params.get("path", "")
	var method = params.get("method", "")
	var args = params.get("args", [])

	var node = get_tree().root.get_node_or_null(path)
	if node == null:
		return {"error": {"code": -32000, "message": "Node not found: " + path}}

	if not node.has_method(method):
		return {"error": {"code": -32000, "message": "Method not found: " + method}}

	var result = node.callv(method, args)
	return {"result": {"value": _serialize_value(result)}}


func _node_exists(params: Dictionary) -> Dictionary:
	var path = params.get("path", "")
	var node = get_tree().root.get_node_or_null(path)
	return {"result": {"exists": node != null}}


func _query_nodes(params: Dictionary) -> Dictionary:
	var pattern = params.get("pattern", "")
	var nodes: Array[Dictionary] = []

	# Simple wildcard matching - find parent and match children
	if "*" in pattern:
		var parts = pattern.rsplit("/", false, 1)
		if parts.size() == 2:
			var parent_path = parts[0]
			var parent = get_tree().root.get_node_or_null(parent_path)
			if parent:
				for child in parent.get_children():
					nodes.append(_serialize_node(child))
	else:
		var node = get_tree().root.get_node_or_null(pattern)
		if node:
			nodes.append(_serialize_node(node))

	return {"result": {"nodes": nodes}}


func _count_nodes(params: Dictionary) -> Dictionary:
	var result = _query_nodes(params)
	var nodes = result.get("result", {}).get("nodes", [])
	return {"result": {"count": nodes.size()}}


func _get_children(params: Dictionary) -> Dictionary:
	var path = params.get("path", "")
	var node = get_tree().root.get_node_or_null(path)

	if node == null:
		return {"error": {"code": -32000, "message": "Node not found: " + path}}

	var children: Array[Dictionary] = []
	for child in node.get_children():
		children.append(_serialize_node(child))

	return {"result": {"children": children}}


# Waiting operations

func _wait_signal(params: Dictionary) -> Dictionary:
	var signal_name = params.get("signal", "")
	var source_path = params.get("source", "")
	var timeout_ms = params.get("timeout", 30000)

	var source: Node = null
	if source_path != "":
		source = get_tree().root.get_node_or_null(source_path)
		if source == null:
			return {"error": {"code": -32000, "message": "Source node not found: " + source_path}}
	else:
		source = get_tree().root

	if not source.has_signal(signal_name):
		return {"error": {"code": -32000, "message": "Signal not found: " + signal_name}}

	# Simple implementation: just await the signal
	# TODO: Implement proper timeout handling
	var result = await source.get(signal_name)

	return {"result": {"signal": signal_name, "args": result if result is Array else []}}


func _wait_frames(params: Dictionary) -> Dictionary:
	var count = params.get("count", 1)

	for i in range(count):
		await get_tree().process_frame

	return {"result": {"frames": count}}


func _wait_seconds(params: Dictionary) -> Dictionary:
	var seconds = params.get("seconds", 0.0)

	await get_tree().create_timer(seconds).timeout

	return {"result": {"seconds": seconds}}


# Scene operations

func _get_current_scene() -> Dictionary:
	var scene = get_tree().current_scene
	if scene == null:
		return {"result": {"path": ""}}
	return {"result": {"path": scene.scene_file_path}}


func _change_scene(params: Dictionary) -> Dictionary:
	var path = params.get("path", "")

	var err = get_tree().change_scene_to_file(path)
	if err != OK:
		return {"error": {"code": -32000, "message": "Failed to change scene: " + error_string(err)}}

	return {"result": {"success": true}}


func _reload_scene() -> Dictionary:
	var err = get_tree().reload_current_scene()
	if err != OK:
		return {"error": {"code": -32000, "message": "Failed to reload scene: " + error_string(err)}}

	return {"result": {"success": true}}


func _get_tree_structure() -> Dictionary:
	var root = get_tree().root
	return {"result": _serialize_tree(root)}


func _serialize_tree(node: Node) -> Dictionary:
	var data = _serialize_node(node)
	data["children"] = []

	for child in node.get_children():
		data["children"].append(_serialize_tree(child))

	return data


# Game state

func _pause() -> Dictionary:
	get_tree().paused = true
	return {"result": {"paused": true}}


func _unpause() -> Dictionary:
	get_tree().paused = false
	return {"result": {"paused": false}}


func _set_time_scale(params: Dictionary) -> Dictionary:
	var scale = params.get("scale", 1.0)
	Engine.time_scale = scale
	return {"result": {"time_scale": scale}}
