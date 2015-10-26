-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

\c vagrant
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players(
    id serial primary key,
    name text,
    matches integer DEFAULT 0
    );

CREATE TABLE matches(
    match_id serial primary key,
    winner integer REFERENCES players(id),
    loser integer REFERENCES players(id)
    );

CREATE VIEW winner_totals AS
    SELECT players.id, players.name, count(players.name) 
    AS win_count , players.matches as match_count 
    FROM players, matches 
    WHERE players.id=matches.winner 
    GROUP BY players.id;

CREATE VIEW player_standings AS
    SELECT players.id, players.name, 
    COALESCE(winner_totals.win_count, 0) AS wins, 
    COALESCE(players.matches, 0) AS match_count
    FROM winner_totals 
    FULL OUTER JOIN players ON players.id=winner_totals.id;