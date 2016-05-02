#!/bin/python
# -*- coding: utf-8 -*-

from view import *
import configparser
import sys


def choose_menu():
    """
    Choose menu function
    """
    choose = menu()
    if choose == 1:
        show()
    elif choose == 2:
        create()
    elif choose == 3:
        edit()
    elif choose == 4:
        delete()
    elif choose == 5:
        exit()
    else:
        print("Please, type a number from 1 to 5")
    choose_menu()


def main():
    config = configparser.ConfigParser()
    config.read(CONFIG)
    try:
        config['DEFAULT']['model']
    except KeyError:
        config['DEFAULT']['model'] = 'dummy'
        with open(CONFIG, 'w') as fil:
            config.write(fil)

    if config['DEFAULT']['model'] == 'sqlite':
        model.ctr = model.MatchSqliteDb
    elif config['DEFAULT']['model'] == 'mysql':
        model.ctr = model.MatchMysqlDb
    elif config['DEFAULT']['model'] == 'postgresql':
        model.ctr = model.MatchPostgresqlDb
    elif config['DEFAULT']['model'] == 'dummy':
        model.ctr = model.MatchList
    else:
        print('WARNING: Config is broken!')
        sys.exit(1)

    model.init()
    choose_menu()


if __name__ == '__main__':
    main()
