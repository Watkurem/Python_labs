from View import *


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

choose_menu()
