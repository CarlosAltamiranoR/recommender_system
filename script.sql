create table akas
(
    tconst varchar (15) not null,
    ordering int null,
    title varchar (255) null,
    region varchar (2) null,
    language varchar (2) null,
    types varchar (20) null,
    attributes varchar (255) null,
    isOriginalTitle tinyint (1) null
);

create table list_tittlelist
(
    id int auto_increment
    primary key,
    id_list varchar (30) not null,
    id_tittlelist varchar (30) not null
);

create table lists
(
    id int auto_increment
    primary key,
    name varchar (255) null,
    link varchar (100) not null,
    metadata varchar (255) not null,
    idImdb varchar (30) not null
)
comment 'información relevante de las listas';

create table name_basics
(
    nconst varchar (15) not null
    primary key,
    primaryName varchar (255) null,
    birthYear int null,
    deathYear int null,
    primaryProfession varchar (255) null,
    knownForTitles varchar (255) null
);

create table principals
(
    tconst varchar (15) not null
    primary key,
    ordering int null,
    nconst varchar (70) null,
    category varchar (70) null,
    job varchar (255) null,
    characters varchar (255) null
);

create table ratings
(
    tconst varchar (15) not null
    primary key,
    averageRating double null,
    numVotes int null
);

create table tittle_basics
(
    tconst varchar (15) null,
    titleType varchar (255) null,
    primaryTitle varchar (255) null,
    originalTitle varchar (255) null,
    isAdult tinyint (1) null,
    startYear int null,
    endYear text null,
    runtimeMinutes int null,
    genres varchar (255) null
);

create table tittle_list
(
    id int auto_increment
    primary key,
    tconst varchar (30) not null,
    f_created date null,
    f_modified date null,
    description varchar (255) null,
    name_tittle varchar (255) null,
    url varchar (255) null,
    tittle_type varchar (255) null,
    imdb_rating float (2,1) null,
    runtime_mins int null,
    year int null,
    release_date date null
)
comment 'tabla de peliculas descargadas desde las listas de IMDB';


