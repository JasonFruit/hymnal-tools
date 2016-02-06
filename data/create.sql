create table meter (
    id integer not null primary key,
    description varchar(30) not null
);

create table author (
    id integer not null primary key,
    name varchar(100) not null
);

create table category (
    id integer not null primary key,
    name varchar(100) not null
);

create table hymn (
    id integer not null primary key,
    num integer null,
    meter_id integer not null,
    author_id integer not null,
    category_id integer not null,
    auth text,
    foreign key (meter_id) references meter(id),
    foreign key (author_id) references author(id),
    foreign key (category_id) references category(id)
);

create table line (
    id integer not null primary key,
    hymn_id integer not null,
    stanza_num integer not null,
    ordinal integer not null,
    content varchar(255),
    sortable text,
    foreign key (hymn_id) references hymn(id)
);
