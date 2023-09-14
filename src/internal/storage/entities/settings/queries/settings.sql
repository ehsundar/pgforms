-- name: GetBoolSetting :one
select value_bool
from settings
where key = $1;

-- name: GetStrSetting :one
select value_str
from settings
where key = $1;

-- name: GetIntSetting :one
select value_int
from settings
where key = $1;

-- name: GetFloatSetting :one
select value_float
from settings
where key = $1;
