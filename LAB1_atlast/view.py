from model import *


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
    i = 0
    while i < len(match_history):
        match_history[i].print_match()
        i += 1


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
    match = Match(team1, team2, score1, score2, tournament, dd, mm, yy)
    return match_history.append(match)


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
    match_history[op_id-1] = Match(team1, team2, score1, score2, tournament, dd, mm, yy)


def delete():
    """
    delete a match from the list
    """
    show()
    op_ch = " Enter number of operation what you want to delete:"
    op_id = int(input(op_ch))
    match_history.pop(op_id-1)
