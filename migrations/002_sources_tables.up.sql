create table sources
(
    id          serial primary key,
    owner       varchar(30)   not null references users (username) on delete restrict,

    conn_string varchar(4000) not null check ( conn_string ~* '^postgresql:\/\/.+\/.+$' ),

    created_at  timestamp     not null default now()
);

create table forms
(
    id         bigserial primary key,
    owner      varchar(30) not null references users (username) on delete restrict,

    source     int         not null references sources (id) not null,

    created_at timestamp   not null default now()
);

create type widgets as enum('text', 'checkbox', 'select');

create table form_fields
(
    id          bigserial primary key,
    form        bigint      not null references forms (id) on delete cascade,

    table_name  varchar(64) not null check ( length(table_name) > 0 ),
    field_name  varchar(64) not null check ( length(field_name) > 0 ),
    weight      int         not null default 1,

    widget      widgets     not null,
    widget_data jsonb       not null
);
