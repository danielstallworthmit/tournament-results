#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("select count(*) from players;")
    player_count = c.fetchall()[0][0]    # Return just the count of players from the DB
    DB.close()
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into players (player_name) values (%s)", (bleach.clean(name),) )
    # If the player enters their name, make sure it doesn't have malicious content
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("select * from standings_vw;") # All of the standings are already sorted in the view standings_vw by number of wins
    player_standings = [(row[0], # 'player_id'
                        str(row[1]), # 'player_name'
                        row[2], # 'wins'
                        row[3]) # 'player_matches'
                        for row in c.fetchall()] # For each row in the standings, get the proper information
    DB.close()
    return player_standings



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into matches (winner, loser) values (%s,%s)", (winner,loser) )
    # Once a match is over, enter the result of the match winner and loser in the DB 
    DB.commit()
    DB.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    c = DB.cursor()
    c.execute("select * from standings_vw;") # Get sorted standings
    standings = c.fetchall() 
    swiss_pairs = [] # Instantiate list of Swiss pairings
    for x in range(1,len(standings)):  # Use x to pair every odd rank to the next rank
        if x % 2 != 0:                 # For each odd rank, append each pairing to the swiss_pairs list
            swiss_pairs.append(
                (standings[x-1][0], standings[x-1][1], standings[x][0], standings[x][1])
              # (id1, name1, id2, name2)
                # Since x starts at 1, have to subtract 1 to get first entry at index 0, etc.
            )
    DB.close()
    return swiss_pairs



