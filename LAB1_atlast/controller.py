#!/bin/python
# -*- coding: utf-8 -*-

import configparser
import sys
import model
import view

CONFIG = 'config.ini'


def choose_menu():
    """
    Choose menu function
    """
    choose = view.menu()
    if choose == 1:
        view.show()
    elif choose == 2:
        view.create()
    elif choose == 3:
        view.edit()
    elif choose == 4:
        view.delete()
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
        ctr = model.MatchSqliteDb
    elif config['DEFAULT']['model'] == 'mysql':
        ctr = model.MatchMysqlDb
    elif config['DEFAULT']['model'] == 'postgresql':
        ctr = model.MatchPostgresqlDb
    elif config['DEFAULT']['model'] == 'dummy':
        ctr = model.MatchList
    else:
        print('WARNING: Config is broken!')
        sys.exit(1)

    model.init(ctr)
    choose_menu()


if __name__ == '__main__':
    main()
