-- name: ListSources :many
select *
from sources
where owner = $1;

-- name: GetSource :one
select *
from sources
where id = $1;

-- name: CreateSource :one
insert into sources(owner, conn_string)
values ($1, $2)
returning *;

-- name: UpdateSource :one
update sources
set conn_string=$2
where id = $1
returning *;

-- name: DeleteSource :one
delete
from sources
where id = $1
returning id;
