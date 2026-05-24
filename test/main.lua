local ipc = require("ipc")

ipc.init()

local tracking = {}

local positions_l = {
    { -0.2,  1,    0.35 },
    { -0.25, 1.25, 0.33 },
    { -0.3, 1.2, 0.33 },
    { -0.4, 1.5, 0.5 },
    { -0.25, 1.35, 0.4 }
}

local positions_r = {
    { 0.2,  1,    0.35 },
    { 0.25, 1.25, 0.33 },
    { 0.3, 1.2, 0.33 },
    { 0.4, 1.5, 0.5 },
    { 0.25, 1.35, 0.4 }
}

-- TODO: 5 euclidean vectors that kinda make sense
local directions = {
    { 0.2, 0.8 }
}

local tracking_idx = 0
for i = 1, 10, 1 do
    local pos_l = positions_l[i % 5]
    local dir_l = directions[i % 5]
    local pos_r = positions_r[i % 5]
    local dir_r = directions[(i + 3) % 5]
    local time = i
    tracking[tracking_idx] = {
        left = {
            timestamp = time,
            pos = pos_l,
            direction = dir_l,
            quat = { 0, 0, 0, 0 },
            tip = { pos_l[0] + dir_l[0], pos_l[1] + dir_l[1], pos_l[2] + dir_l[2] },
            buttons = {},
        },
        right = {
            timestamp = time,
            pos = pos_r,
            direction = dir_r,
            quat = { 0, 0, 0, 0 },
            tip = { pos_r[0] + dir_r[0], pos_r[1] + dir_r[1], pos_r[2] + dir_r[2] },
            buttons = {},
        },
        head = {
            timestamp = time,
            pos = { 0, 2, 0 },
            direction = { 0, 0, 0 },
            quat = { 0, 0, 0, 0 },
            tip = { 0, 0, 0 },
            buttons = {},
        },
    }
    tracking = tracking + 1
end

ipc.send_json(tracking)
