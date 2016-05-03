# -*- coding: utf-8 -*-

import sys
import warnings
import datetime
import sqlite3
import MySQLdb
import psycopg2
import psycopg2.extras


class ScoreError(Exception):
    """An exception to raise if score was wrong."""
    pass


class DateError(Exception):
    """An exception to raise if date was wrong."""
    pass


class Match:
    def __init__(self, team1, team2, score1, score2, tournament, dd, mm, yy):
        """
        >>> Match("Ukraine", "England", 2, 3, "World Cup", 20, 10, 2016)
        Match(Ukraine,England,2,3,World Cup,20,10,2016)
        """
        self.team1 = team1
        self.team2 = team2
        self.score1 = score1
        self.score2 = score2
        self.tournament = tournament
        self.dd = dd
        self.mm = mm
        self.yy = yy

    def __repr__(self):
        """
        >>> a = Match("Ukraine", "England", 2, 3, "World Cup", 20, 10, 2016)
        >>> print(a)
        Match(Ukraine,England,2,3,World Cup,20,10,2016)

        :return:
        """
        return "Match({},{},{},{},{},{},{},{})".format(self.team1, self.team2, self.score1, self.score2,
                                                       self.tournament, self.dd, self.mm, self.yy)

    def print_match(self):
        """
        >>> a = Match("Ukraine", "England", 2, 3, "World Cup", 20, 10, 2016)
        >>> a.print_match()
        <BLANKLINE>
        World Cup
        Ukraine-England
        2-3
        20.10.2016
        """
        print('\n' + self.tournament)
        print(self.team1 + '-' + self.team2)
        print(str(self.score1) + '-' + str(self.score2))
        print(str(self.dd) + '.' + str(self.mm) + '.' + str(self.yy))


class MatchList:
    """A pretty basic 'dummy' class that encapsulates a list of matches.

    Consider sublassing and extending it."""
    def __init__(self):
        """Init with hard-coded data, so the class is not very useful."""
        self.matches = [Match("Ukraine", "Russia", 2, 0,
                              "World Cup", 20, 10, 2016),
                        Match("England", "Germany", 1, 2,
                              "World Cup", 22, 10, 2016),
                        Match("Spain", "Italy", 2, 2,
                              "Euro2016", 5, 6, 2016)]

    def show(self):
        """Fetch matches.

        return: tuple of matches."""
        return tuple(self.matches)

    def create(self, team1, team2, score1, score2, tournament, dd, mm, yy):
        """Create and store a new match.

        team1: string - first team for Match constructor.
        team2: string - second team for Match constructor.
        score1: string - score of the first team for Match constructor.
        score1: string - score of the second team for Match constructor.
        tournament: string - name of the tournament.
        dd: string - day when match was held for Match constructor.
        mm: string - month when match was held for Match constructor.
        yy: string - year when match was held for Match constructor.

        return: Match that was successfully created or None if creation failed.
        """
        self.matches.append(Match(team1, team2, score1,
                                  score2, tournament, dd, mm, yy))
        return self.matches[-1]

    def edit(self, idx, team1, team2, score1, score2, tournament, dd, mm, yy):
        """Edit existing match.

        Or replace it with a new one.

        idx: match-to-edit position in tuple returned by show.
        team1: string - first team for Match constructor.
        team2: string - second team for Match constructor.
        score1: string - score of the first team for Match constructor.
        score1: string - score of the second team for Match constructor.
        tournament: string - name of the tournament.
        dd: string - day when match was held for Match constructor.
        mm: string - month when match was held for Match constructor.
        yy: string - year when match was held for Match constructor.

        return: Match that was successfully edited or None if edit failed.
        """
        try:
            self.matches[idx] = Match(team1, team2, score1, score2,
                                      tournament, dd, mm, yy)
            return self.matches[idx]
        except IndexError:
            return None

    def delete(self, idx):
        """Delete existing match.

        idx: match-to-delete position in tuple returned by show.

        return: Deleted match (pop functionality) or None if deletion failed.
        """
        try:
            return self.matches.pop(idx)
        except IndexError:
            return None


class MatchMysqlDb(MatchList):
    """A MatchList implementation using MySQL database."""
    create_table_query = ('CREATE TABLE IF NOT EXISTS matches '
                          '(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, '
                          'team1 VARCHAR(100) NOT NULL, '
                          'team2 VARCHAR(100) NOT NULL, '
                          'score1 SMALLINT NOT NULL, '
                          'score2 SMALLINT NOT NULL, '
                          'tournament VARCHAR(256), '
                          '"date" DATE NOT NULL)')
    select_query = ('SELECT * FROM matches')
    insert_query = ('INSERT INTO matches '
                    '(team1, team2, score1, score2, tournament, date) '
                    'VALUES'
                    '(%s, %s, %s, %s, %s, %s)')
    update_query = ('UPDATE matches SET '
                    'team1=%s, team2=%s, score1=%s, score2=%s, '
                    'tournament=%s, date=%s '
                    'WHERE team1 = %s AND team2 = %s '
                    'AND score1 = %s AND score2 = %s '
                    'AND tournament = %s AND date = %s')
    delete_query = ('DELETE FROM matches WHERE '
                    'team1 = %s AND team2 = %s '
                    'AND score1 = %s AND score2 = %s '
                    'AND tournament = %s AND date = %s')

    def __init__(self):
        """Open database connection.

        Database server is assumed to be accessible on localhost (127.0.0.1),
        database is assumed to be archlab, user is assumed to be archlab and
        user's password is assumed to be empty.
        """
        try:
            self.conn = MySQLdb.connect('127.0.0.1', 'archlab', '', 'archlab')
        except MySQLdb.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit()

    def __del__(self):
        """Close database connection."""
        self.conn.close()

    def _getcur(self):
        """A private method that makes it easier to reuse code."""
        return self.conn.cursor(MySQLdb.cursors.DictCursor)

    def show(self):
        cur = self._getcur()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            cur.execute(self.create_table_query)
            self.conn.commit()

        cur.execute("SELECT * FROM matches")
        matches = []
        for m in cur.fetchall():
            matches.append(Match(m["team1"],
                                 m["team2"],
                                 str(m["score1"]),
                                 str(m["score2"]),
                                 m["tournament"],
                                 str(m["date"].day),
                                 str(m["date"].month),
                                 str(m["date"].year)))
        return tuple(matches)

    def create(self, team1, team2, score1, score2, tournament, dd, mm, yy):
        try:
            score1, score2 = int(score1), int(score2)
        except ValueError:
            raise ValueError

        try:
            dd, mm, yy = int(dd), int(mm), int(yy)
        except ValueError:
            raise ValueError

        if not ((0 <= score1 <= 32767) and (0 <= score2 <= 32767)):
            raise ScoreError("Score overflow")
        if not ((1 <= dd <= 31) and (1 <= mm <= 12) and (1000 <= yy <= 9999)):
            raise DateError("Date can't be empty, less than 01-01-1000 " +
                            "or greater than 31-12-9999")

        cur = self._getcur()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            cur.execute(self.create_table_query)

        data = (team1, team2, score1, score2,
                tournament, datetime.date(yy, mm, dd))
        cur.execute(self.insert_query, data)
        self.conn.commit()
        return Match(team1, team2, str(score1), str(score2),
                     tournament, str(dd), str(mm), str(yy))

    def edit(self, idx, team1, team2, score1, score2, tournament, dd, mm, yy):
        try:
            score1, score2 = int(score1), int(score2)
        except ValueError:
            raise ValueError

        try:
            dd, mm, yy = int(dd), int(mm), int(yy)
        except ValueError:
            raise ValueError

        if not ((0 <= score1 <= 32767) and (0 <= score2 <= 32767)):
            raise ScoreError("Score overflow")
        if not ((1 <= dd <= 31) and (1 <= mm <= 12) and (1000 <= yy <= 9999)):
            raise DateError("Date can't be empty, less than 01-01-1000 " +
                            "or greater than 31-12-9999")

        try:
            old_match = self.show()[idx]
        except IndexError:
            return None

        cur = self._getcur()

        data = (team1, team2, score1, score2, tournament,
                datetime.date(yy, mm, dd), old_match.team1, old_match.team2,
                old_match.score1, old_match.score2, old_match.tournament,
                datetime.date(int(old_match.yy),
                              int(old_match.mm),
                              int(old_match.dd)))
        cur.execute(self.update_query, data)
        self.conn.commit()
        return Match(team1, team2, str(score1), str(score2),
                     tournament, str(dd), str(mm), str(yy))

    def delete(self, idx):
        try:
            match = self.show()[idx]
        except IndexError:
            return None

        cur = self._getcur()

        data = (match.team1, match.team2, match.score1, match.score2,
                match.tournament, datetime.date(int(match.yy),
                                                int(match.mm),
                                                int(match.dd)))
        cur.execute(self.delete_query, data)
        self.conn.commit()
        return match


class MatchSqliteDb(MatchMysqlDb):
    """A MatchMysqlDb implementation modified for SQLite database."""
    create_table_query = MatchMysqlDb.create_table_query.replace(
        'NOT NULL AUTO_INCREMENT ', '')
    select_query = MatchMysqlDb.select_query.replace('%s', '?')
    insert_query = MatchMysqlDb.insert_query.replace('%s', '?')
    update_query = MatchMysqlDb.update_query.replace('%s', '?')
    delete_query = MatchMysqlDb.delete_query.replace('%s', '?')

    def __init__(self):
        try:
            self.conn = sqlite3.connect('archlab.db')
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit()

    def _getcur(self):
        return self.conn.cursor()

    def show(self):
        cur = self._getcur()
        cur.execute(self.create_table_query)
        cur.execute(self.select_query)
        matches = []
        for m in cur.fetchall():
            matches.append(Match(m["team1"],
                                 m["team2"],
                                 m["score1"],
                                 m["score2"],
                                 m["tournament"],
                                 m["date"][8:10],
                                 m["date"][5:7],
                                 m["date"][:4]))
        return tuple(matches)


class MatchPostgresqlDb(MatchMysqlDb):
    """A MatchMysqlDb implementation modified for PostgreSQL database."""
    create_table_query = MatchMysqlDb.create_table_query.replace(
        'INT NOT NULL AUTO_INCREMENT', 'SERIAL')

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                database='archlab', user='archlab',
                cursor_factory=psycopg2.extras.DictCursor)
        except sqlite3.Error as e:
            print("Error %d: %s" % (e.args[0], e.args[1]))
            sys.exit()

    def _getcur(self):
        return self.conn.cursor()


match_history = None


def init(ctr):
    """A dirty hack for legacy code integration."""
    global match_history
    match_history = ctr()
