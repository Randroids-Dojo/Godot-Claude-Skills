extends Node
## WebSocket server for PlayGodot automation.
##
## Handles incoming connections and dispatches commands to the appropriate handlers.

const Commands = preload("res://addons/playgodot/commands.gd")
const DEFAULT_PORT = 9999

var _server: TCPServer = null
var _peers: Array[WebSocketPeer] = []
var _commands: Commands = null
var _port: int = DEFAULT_PORT


func _ready() -> void:
	_commands = Commands.new(self)
	add_child(_commands)

	# In headless mode, set viewport size from project settings
	# This ensures UI layout is calculated correctly
	_setup_headless_viewport()

	# Check for custom port from command line or environment
	_port = _get_port()

	_start_server()


func _setup_headless_viewport() -> void:
	if not DisplayServer.get_name() == "headless":
		return

	# Get window size from project settings
	var width = ProjectSettings.get_setting("display/window/size/viewport_width", 1152)
	var height = ProjectSettings.get_setting("display/window/size/viewport_height", 648)

	# Set the root viewport size
	get_tree().root.size = Vector2i(width, height)
	print("[PlayGodot] Set headless viewport size to %dx%d" % [width, height])


func _get_port() -> int:
	# Check command line arguments
	var args = OS.get_cmdline_args()
	for i in range(args.size() - 1):
		if args[i] == "--playgodot-port":
			return int(args[i + 1])

	# Check environment variable
	var env_port = OS.get_environment("PLAYGODOT_PORT")
	if env_port != "":
		return int(env_port)

	return DEFAULT_PORT


func _start_server() -> void:
	_server = TCPServer.new()
	var err = _server.listen(_port)
	if err != OK:
		push_error("[PlayGodot] Failed to start server on port %d: %s" % [_port, error_string(err)])
		return

	print("[PlayGodot] Server listening on ws://localhost:%d" % _port)


func _process(_delta: float) -> void:
	if _server == null:
		return

	# Accept new connections
	while _server.is_connection_available():
		var connection = _server.take_connection()
		var peer = WebSocketPeer.new()
		peer.accept_stream(connection)
		_peers.append(peer)
		print("[PlayGodot] Client connected")

	# Process existing peers
	var disconnected: Array[int] = []

	for i in range(_peers.size()):
		var peer = _peers[i]
		peer.poll()

		var state = peer.get_ready_state()

		if state == WebSocketPeer.STATE_OPEN:
			while peer.get_available_packet_count() > 0:
				var packet = peer.get_packet()
				_handle_message(peer, packet.get_string_from_utf8())
		elif state == WebSocketPeer.STATE_CLOSING:
			pass  # Wait for close
		elif state == WebSocketPeer.STATE_CLOSED:
			disconnected.append(i)
			print("[PlayGodot] Client disconnected")

	# Remove disconnected peers (in reverse order)
	for i in range(disconnected.size() - 1, -1, -1):
		_peers.remove_at(disconnected[i])


func _handle_message(peer: WebSocketPeer, message: String) -> void:
	var json = JSON.new()
	var err = json.parse(message)
	if err != OK:
		_send_error(peer, null, -32700, "Parse error")
		return

	var request = json.data

	if not request is Dictionary:
		_send_error(peer, null, -32600, "Invalid Request")
		return

	var id = request.get("id")
	var method = request.get("method", "")
	var params = request.get("params", {})

	if method == "":
		_send_error(peer, id, -32600, "Invalid Request: missing method")
		return

	# Execute command
	var result = await _commands.execute(method, params)

	if result.has("error"):
		_send_error(peer, id, result.error.code, result.error.message)
	else:
		_send_result(peer, id, result.get("result", null))


func _send_result(peer: WebSocketPeer, id: Variant, result: Variant) -> void:
	var response = {
		"jsonrpc": "2.0",
		"id": id,
		"result": result
	}
	peer.send_text(JSON.stringify(response))


func _send_error(peer: WebSocketPeer, id: Variant, code: int, message: String) -> void:
	var response = {
		"jsonrpc": "2.0",
		"id": id,
		"error": {
			"code": code,
			"message": message
		}
	}
	peer.send_text(JSON.stringify(response))


func _exit_tree() -> void:
	for peer in _peers:
		peer.close()
	_peers.clear()

	if _server:
		_server.stop()
		_server = null
