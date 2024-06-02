create table user
(
    id         int auto_increment
        primary key,
    username   varchar(255)                        not null,
    preference json                                null,
    create_at  timestamp default CURRENT_TIMESTAMP not null,
    modify_at  timestamp                           null on update CURRENT_TIMESTAMP,
    constraint username
        unique (username)
);


