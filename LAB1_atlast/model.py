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


match_history = None


def init():
    global match_history
    match_history = ctr()
