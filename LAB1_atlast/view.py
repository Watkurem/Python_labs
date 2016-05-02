import model


def menu():
    """
    Shows menu
    :return:
    """
    print("\n1.Show")
    print("2.Add")
    print("3.Edit")
    print("4.Delete")
    print("5.Exit")
    a = int(input())
    return a


def show():
    """
    Shows all matches
    >>> show()
    <BLANKLINE>
    World Cup
    Ukraine-Russia
    2-0
    20.10.2016
    <BLANKLINE>
    World Cup
    England-Germany
    1-2
    22.10.2016
    <BLANKLINE>
    Euro2016
    Spain-Italy
    2-2
    5.6.2016
    """
    for match in model.match_history.show():
            print()
            print(match.tournament)
            print("{}-{}".format(match.team1, match.team2))
            print("{}-{}".format(match.score1, match.score2))
            print("{}.{}.{}".format(match.dd, match.mm, match.yy))


def create():
    """
    Creates match in the list
    :not_test:
    :return:
    """
    team1 = input(" Team 1: ")
    team2 = input(" Team 2: ")
    score1 = input(" Score1: ")
    score2 = input(" Score2: ")
    tournament = input(" Tournament name: ")
    dd = input(" Enter day :")
    mm = input(" Enter month :")
    yy = input(" Enter year :")
    model.match_history.create(team1, team2, score1, score2, tournament, dd, mm, yy)


def edit():
    """
    Edit match in the list
    :return:
    """
    show()
    op_ch = " Enter number of operation what you want to change:"
    op_id = int(input(op_ch))
    team1 = input(" Team1: ")
    team2 = input(" Team2: ")
    score1 = input(" Score1: ")
    score2 = input(" Score2: ")
    tournament = input(" Tournament: ")
    dd = input(" Day: ")
    mm = input(" Month: ")
    yy = input(" Year: ")
    model.match_history.edit(op_id-1, team1, team2, score1, score2, tournament, dd, mm, yy)


def delete():
    """
    delete a match from the list
    """
    show()
    op_ch = " Enter number of operation what you want to delete:"
    op_id = int(input(op_ch))
    model.match_history.delete(op_id-1)
