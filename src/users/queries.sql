-- name: GetUser :one
select *
from users
where username = $1;

-- name: CreateUser :one
insert into users(username, password, email, name)
values ($1, $2, $3, $4)
returning *;

-- name: GetSession :one
select *
from sessions
where id = $1;

-- name: GetUserSessions :many
select *
from sessions
where username = $1;

-- name: CreateSession :one
insert into sessions (username)
values ($1)
returning *;
