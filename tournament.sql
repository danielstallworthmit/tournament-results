-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

-- Drop tournament DB if it already exists (make sure you don't have another DB called tournament first)
drop database tournament;

-- Create the tournament DB
create database tournament;

-- Switch to the tournament DB
\c tournament;

-- -- drop tables if they already exist so can create the tables properly
-- drop table players cascade;
-- drop table matches cascade;

-- Create table to house the players:
create table players (
	player_id serial primary key,
	player_name text
);

-- Create table to house the winners and losers of matches along with the match numbers
create table matches (
	match_id serial primary key,
	winner integer references players (player_id),
	loser integer references players (player_id)
);

-- Since need to get player standings, which change frequently, should have a view for easy access to the standings 
	-- via a view in the DB
create view standings_vw as 
	select * from (
		select p.player_id, p.player_name, COALESCE(w.wins,0) wins, COALESCE(w.wins,0) + COALESCE(l.losses,0) player_matches 
		from 
			players p
			left join (select winner, count(*) wins from matches group by winner) w
				on p.player_id = w.winner
			left join (select loser, count(*) losses from matches group by loser) l
				on p.player_id = l.loser
	) standings
	order by wins desc;



-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


