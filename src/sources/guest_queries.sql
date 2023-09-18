-- name: ListTables :many
select table_schema, table_name
from information_schema.tables
where table_schema not in ('information_schema', 'pg_catalog');

-- name: ListTableColumns :many
select collation_name, data_type, column_default, is_nullable
from information_schema.columns
where table_schema = $1
  and table_name = $2;
