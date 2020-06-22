create table if not exists stat (
    url varchar(500) primary key not null,
    n int not null
);

create unique index stat_url_idx on stat(url) using btree;
