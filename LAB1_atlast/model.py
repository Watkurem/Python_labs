# -*- coding: utf-8 -*-

import sys
import warnings
import MySQLdb

class ScoreError(Exception):
    pass

class DateError(Exception):
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
    def __init__(self, *matches):
        self.matches = [Match("Ukraine", "Russia", 2, 0,
                              "World Cup", 20, 10, 2016),
                        Match("England", "Germany", 1, 2,
                              "World Cup", 22, 10, 2016),
                        Match("Spain", "Italy", 2, 2,
                              "Euro2016", 5, 6, 2016)]

    def show(self):
        return tuple(self.matches)

    def create(self, team1, team2, score1, score2, tournament, dd, mm, yy):
        self.matches.append(Match(team1, team2, score1, score2, tournament, dd, mm, yy))
        return self.matches[-1]

    def edit(self, idx, team1, team2, score1, score2, tournament, dd, mm, yy):
        try:
            self.matches[idx] = Match(team1, team2, score1, score2, tournament, dd, mm, yy)
            return self.matches[idx]
        except IndexError:
            return None

    def delete(self, idx):
        try:
            return self.matches.pop(idx)
        except IndexError:
            return None


class MatchMysqlDb(MatchList):
    def __init__(self):
        try:
            self.conn = MySQLdb.connect('127.0.0.1', 'archlab', '', 'archlab')
        except MySQLdb.Error as e:
            print("Error %d: %s" % (e.args[0],e.args[1]))
            sys.exit()

    def __del__(self):
        self.conn.close()

    def show(self):
        cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            cur.execute('CREATE TABLE IF NOT EXISTS matches ' +
                        '(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, ' +
                        'team1 VARCHAR(100) NOT NULL, ' +
                        'team2 VARCHAR(100) NOT NULL, ' +
                        'score1 SMALLINT NOT NULL, ' +
                        'score2 SMALLINT NOT NULL, ' +
                        'tournament VARCHAR(256), ' +
                        '`date` DATE NOT NULL)')
        cur.execute("SELECT * FROM matches")
        matches = []
        for m in cur.fetchall():
            matches.append(Match(m["team1"],
                                 m["team2"],
                                 m["score1"],
                                 m["score2"],
                                 m["tournament"],
                                 m["date"].day,
                                 m["date"].month,
                                 m["date"].year))
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

        cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('INSERT INTO matches ' +
                    '(team1, team2, score1, score2, tournament, date) ' +
                    'VALUES' +
                    '("{}", "{}", {}, {}, "{}", "{}-{}-{}")'.format(
                        team1, team2, score1, score2, tournament, yy, mm, dd
                    ))
        return Match(team1, team2, score1, score2, tournament, dd, mm, yy)

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

        cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('UPDATE matches SET ' +
                    'team1="{}", team2="{}", score1={}, score2={}, '.format(
                        team1, team2, score1, score2) +
                    'tournament="{}", date="{}-{}-{}" '.format(
                        tournament, yy, mm, dd) +
                    'WHERE team1 = "{}" AND team2 = "{}" '.format(
                        old_match.team1, old_match.team2) +
                    'AND score1 = {} AND score2 = {} '.format(
                        old_match.score1, old_match.score2) +
                    'AND tournament = "{}" AND date = "{}-{}-{}"'.format(
                        old_match.tournament, old_match.yy,
                        old_match.mm, old_match.dd))
        return Match(team1, team2, score1, score2, tournament, dd, mm, yy)

    def delete(self, idx):
        try:
            match = self.show()[idx]
        except IndexError:
            return None
        cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('DELETE FROM matches WHERE ' +
                    'team1 = "{}" AND team2 = "{}" '.format(
                        match.team1, match.team2) +
                    'AND score1 = {} AND score2 = {} '.format(
                        match.score1, match.score2) +
                    'AND tournament = "{}" AND date = "{}-{}-{}"'.format(
                        match.tournament, match.yy,
                        match.mm, match.dd))
        return match


match_history = None


def init():
    global match_history
    match_history = ctr()
