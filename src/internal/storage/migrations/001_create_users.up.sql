create table users
(
    username varchar(30) primary key,
    password char(64)     not null,
    email    varchar(500) not null check ( email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$' ),
    name     varchar(200) not null
);

create index users_email_idx on users (email);

create unlogged table sessions
(
    id        uuid primary key     default gen_random_uuid(),
    username  varchar(30) not null references users (username) on delete cascade,
    issued_at timestamp   not null default now()
);

create index sessions_username on sessions (username);

create type settings_value_type as enum ('bool', 'str', 'int', 'float');

create table settings
(
    key         varchar(50) primary key,
    value_type  settings_value_type not null,

    value_bool  bool,
    value_str   varchar(500),
    value_int   int,
    value_float float8,

    check ( value_bool is not null or value_str is not null or value_int is not null or value_float is not null)
);
