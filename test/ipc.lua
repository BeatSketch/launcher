-- Abstraction for inter-process communication with the python-based launcher, which also does the processing
local json = require("json")

--- IPC abstraction utilities
--- Can be used to communicate with the launcher
local M = {}
local init_done = false

function M.init()
	if init_done then
		return false
	end
	init_done = true
	print("[BeatSketch] IPC INIT COMPLETE")
end

--- Send JSON data to the parent process
--- @param data table The table to send
function M.send_json(data)
	if not init_done then
		return false
	end

	print("json:" .. json.encode(data))
	io.flush()
end

--- Send text to the parent process
---@param data string The string to send
function M.send_text(data)
	M.send_plain("str:" .. data)
end

function M.send_plain(data)
	if not init_done then
		return false
	end

	print(data)
	io.flush()
end

return M
