create table users
(
    username varchar(30) primary key,
    password varchar(64)  not null check ( password ~* '^\$2b\$\d+\$.{53}$' ),
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
