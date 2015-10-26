#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    delete_matches = "DELETE FROM matches;"
    c.execute(delete_matches)
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    delete_players = "DELETE FROM players;"
    c.execute(delete_players)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    count_players = "SELECT count(id) as num_players FROM players;"
    c.execute(count_players)
    total_players = c.fetchall()
    db.close()

    return total_players[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()

    #Create new player, protect from SQL Injection attacks. 
    c.execute("INSERT into players (name) values (%s)", (name,))

    db.commit()
    db.close()



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
    db = connect()
    c = db.cursor()
    player_standings = "SELECT * from player_standings;"

    c.execute(player_standings)
    player_list = c.fetchall()
    db.close()
    return player_list

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    match_result = "INSERT INTO matches(winner, loser) \
                      values(%s, %s);" % (winner, loser,)
    
    """Increment the number of matches associated with each player"""
    track_match_number = "UPDATE players \
                          SET matches = matches + 1 \
                          WHERE %s = players.id \
                          OR %s = players.id;" % (winner, loser)  
                     
    c.execute(match_result)
    c.execute(track_match_number)

    db.commit()
    db.close()

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
    # Pull current rankings from DB sorted by amount of wins
    db = connect()
    c = db.cursor()
    rankings = "SELECT id, name FROM player_standings order by wins;"

    c.execute(rankings)
    rankings = c.fetchall()
    db.close()
    len(rankings)

    count = 0
    next_round = []
    #sort the wins into pairs of players, grouped by the number of wins so far.
    #there is a bit of back and forth getting the list indexing to work. 
    # each pairing is added to the next_round list as it is sliced.             

    while count < len(rankings) - 2:
        if count == 0:
            this_pair = rankings[count] + rankings[count + 1]
            count = count + 1
            next_round.append(this_pair)

        else:
            this_pair = rankings[count + 1] + rankings[count + 2]
            count = count + 1
            next_round.append(this_pair)

    return next_round






