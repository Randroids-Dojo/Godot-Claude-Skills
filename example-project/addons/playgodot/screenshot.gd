extends Node
## Screenshot capture for PlayGodot.
##
## Captures screenshots and returns them as base64-encoded PNG data.


## Capture a screenshot.
func capture(params: Dictionary) -> Dictionary:
	var node_path = params.get("node", "")

	# Get the viewport
	var viewport = get_viewport()
	if viewport == null:
		return {"error": {"code": -32000, "message": "No viewport available"}}

	# Wait for the next frame to ensure rendering is complete
	await RenderingServer.frame_post_draw

	# Get the texture
	var texture = viewport.get_texture()
	if texture == null:
		return {"error": {"code": -32000, "message": "Failed to get viewport texture"}}

	# Get the image
	var image = texture.get_image()
	if image == null:
		return {"error": {"code": -32000, "message": "Failed to get image from texture"}}

	# If a specific node is requested, crop to that node's rect
	if node_path != "":
		var node = get_tree().root.get_node_or_null(node_path)
		if node == null:
			return {"error": {"code": -32000, "message": "Node not found: " + node_path}}

		var rect = _get_node_rect(node)
		if rect != null:
			# Ensure rect is within image bounds
			var img_rect = Rect2i(Vector2i.ZERO, image.get_size())
			rect = rect.intersection(img_rect)
			if rect.size.x > 0 and rect.size.y > 0:
				image = image.get_region(rect)

	# Convert to PNG
	var png_data = image.save_png_to_buffer()

	# Encode as base64
	var base64_data = Marshalls.raw_to_base64(png_data)

	return {
		"result": {
			"data": base64_data,
			"width": image.get_width(),
			"height": image.get_height(),
			"format": "png"
		}
	}


## Get the screen rect of a node.
func _get_node_rect(node: Node) -> Variant:
	if node is Control:
		var rect = node.get_global_rect()
		return Rect2i(
			int(rect.position.x),
			int(rect.position.y),
			int(rect.size.x),
			int(rect.size.y)
		)
	elif node is CanvasItem:
		# For 2D nodes, try to get transform and estimate size
		if node.has_method("get_global_transform"):
			var pos = node.get_global_transform().origin
			# Default size for 2D nodes without explicit size
			var size = Vector2(64, 64)

			# Try to get actual size from texture
			if node is Sprite2D and node.texture:
				size = node.texture.get_size() * node.scale

			return Rect2i(
				int(pos.x - size.x / 2),
				int(pos.y - size.y / 2),
				int(size.x),
				int(size.y)
			)

	return null
